import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings
from django.core.cache import cache
from ml_models.models import MLModel, Prediction
from stats.models import Player, Team, Match, PlayerStats, TeamStats


class ModelService:
    """
    Service for loading and using ML models.
    """
    CACHE_TIMEOUT = 3600  # 1 hour

    @staticmethod
    def get_model(model_type, version=None):
        """
        Get the ML model instance from the database.
        If version is not specified, get the latest active model.
        """
        if version:
            model = MLModel.objects.filter(
                model_type=model_type,
                version=version,
                is_active=True
            ).first()
        else:
            model = MLModel.objects.filter(
                model_type=model_type,
                is_active=True
            ).order_by('-created_at').first()
        
        return model

    @staticmethod
    def load_model(model_instance):
        """
        Load the ML model from the file system.
        Use caching to avoid loading the model multiple times.
        """
        cache_key = f"ml_model_{model_instance.id}"
        model = cache.get(cache_key)
        
        if model is None:
            file_path = model_instance.file_path
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Model file not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                model = pickle.load(f)
            
            cache.set(cache_key, model, ModelService.CACHE_TIMEOUT)
        
        return model

    @staticmethod
    def prepare_player_features(player, match=None, recent_matches=5):
        """
        Prepare features for player performance prediction.
        """
        # Get player's recent stats
        if match:
            recent_stats = PlayerStats.objects.filter(
                player=player,
                match__date__lt=match.date
            ).order_by('-match__date')[:recent_matches]
        else:
            recent_stats = PlayerStats.objects.filter(
                player=player
            ).order_by('-match__date')[:recent_matches]
        
        if not recent_stats:
            return None
        
        # Calculate average stats
        avg_points = sum(stat.points for stat in recent_stats) / len(recent_stats)
        avg_assists = sum(stat.assists for stat in recent_stats) / len(recent_stats)
        avg_rebounds = sum(stat.rebounds for stat in recent_stats) / len(recent_stats)
        avg_steals = sum(stat.steals for stat in recent_stats) / len(recent_stats)
        avg_blocks = sum(stat.blocks for stat in recent_stats) / len(recent_stats)
        avg_minutes = sum(stat.minutes_played for stat in recent_stats) / len(recent_stats)
        
        # Create feature dictionary
        features = {
            'player_id': player.id,
            'position': player.position,
            'height': player.height,
            'weight': player.weight,
            'age': player.age,
            'avg_points': avg_points,
            'avg_assists': avg_assists,
            'avg_rebounds': avg_rebounds,
            'avg_steals': avg_steals,
            'avg_blocks': avg_blocks,
            'avg_minutes': avg_minutes,
        }
        
        # Add opponent team features if match is provided
        if match:
            if player.team == match.home_team:
                opponent_team = match.away_team
            else:
                opponent_team = match.home_team
            
            # Get opponent team's defensive stats
            opponent_stats = TeamStats.objects.filter(
                team=opponent_team
            ).order_by('-match__date')[:recent_matches]
            
            if opponent_stats:
                avg_opp_points_allowed = sum(stat.points for stat in opponent_stats) / len(opponent_stats)
                features['avg_opp_points_allowed'] = avg_opp_points_allowed
        
        return features

    @staticmethod
    def prepare_match_features(match):
        """
        Prepare features for match outcome prediction.
        """
        home_team = match.home_team
        away_team = match.away_team
        recent_matches = 10
        
        # Get recent home team stats
        home_stats = TeamStats.objects.filter(
            team=home_team
        ).order_by('-match__date')[:recent_matches]
        
        # Get recent away team stats
        away_stats = TeamStats.objects.filter(
            team=away_team
        ).order_by('-match__date')[:recent_matches]
        
        if not home_stats or not away_stats:
            return None
        
        # Calculate average stats for home team
        home_avg_points = sum(stat.points for stat in home_stats) / len(home_stats)
        home_avg_rebounds = sum(stat.rebounds for stat in home_stats) / len(home_stats)
        home_avg_assists = sum(stat.assists for stat in home_stats) / len(home_stats)
        home_avg_steals = sum(stat.steals for stat in home_stats) / len(home_stats)
        home_avg_blocks = sum(stat.blocks for stat in home_stats) / len(home_stats)
        
        # Calculate average stats for away team
        away_avg_points = sum(stat.points for stat in away_stats) / len(away_stats)
        away_avg_rebounds = sum(stat.rebounds for stat in away_stats) / len(away_stats)
        away_avg_assists = sum(stat.assists for stat in away_stats) / len(away_stats)
        away_avg_steals = sum(stat.steals for stat in away_stats) / len(away_stats)
        away_avg_blocks = sum(stat.blocks for stat in away_stats) / len(away_stats)
        
        # Create feature dictionary
        features = {
            'home_team_id': home_team.id,
            'away_team_id': away_team.id,
            'home_avg_points': home_avg_points,
            'home_avg_rebounds': home_avg_rebounds,
            'home_avg_assists': home_avg_assists,
            'home_avg_steals': home_avg_steals,
            'home_avg_blocks': home_avg_blocks,
            'away_avg_points': away_avg_points,
            'away_avg_rebounds': away_avg_rebounds,
            'away_avg_assists': away_avg_assists,
            'away_avg_steals': away_avg_steals,
            'away_avg_blocks': away_avg_blocks,
        }
        
        return features

    @staticmethod
    def predict_player_performance(player, match=None, model_version=None):
        """
        Predict player performance for a match.
        """
        # Get the ML model
        model_instance = ModelService.get_model('PLAYER_PERFORMANCE', model_version)
        if not model_instance:
            raise ValueError("No active player performance prediction model found")
        
        # Prepare features
        features = ModelService.prepare_player_features(player, match)
        if not features:
            raise ValueError("Not enough data to make a prediction")
        
        # Load the model
        model = ModelService.load_model(model_instance)
        
        # Make prediction
        features_df = pd.DataFrame([features])
        prediction = model.predict(features_df)[0]
        confidence = 0.8  # Placeholder for confidence score
        
        # Create prediction object
        prediction_obj = Prediction.objects.create(
            model=model_instance,
            prediction_type='PLAYER_STATS',
            match=match,
            player=player,
            prediction_data={
                'points': float(prediction[0]),
                'assists': float(prediction[1]),
                'rebounds': float(prediction[2]),
                'steals': float(prediction[3]),
                'blocks': float(prediction[4]),
            },
            confidence=confidence
        )
        
        return prediction_obj

    @staticmethod
    def predict_match_outcome(match, model_version=None):
        """
        Predict the outcome of a match.
        """
        # Get the ML model
        model_instance = ModelService.get_model('MATCH_OUTCOME', model_version)
        if not model_instance:
            raise ValueError("No active match outcome prediction model found")
        
        # Prepare features
        features = ModelService.prepare_match_features(match)
        if not features:
            raise ValueError("Not enough data to make a prediction")
        
        # Load the model
        model = ModelService.load_model(model_instance)
        
        # Make prediction
        features_df = pd.DataFrame([features])
        prediction = model.predict(features_df)[0]
        confidence = model.predict_proba(features_df)[0].max()
        
        # Determine winner
        if prediction == 1:
            winner = match.home_team
        else:
            winner = match.away_team
        
        # Create prediction object
        prediction_obj = Prediction.objects.create(
            model=model_instance,
            prediction_type='MATCH_WINNER',
            match=match,
            team=winner,
            prediction_data={
                'winner_id': winner.id,
                'winner_name': str(winner),
                'home_win_probability': float(confidence if prediction == 1 else 1 - confidence),
                'away_win_probability': float(confidence if prediction == 0 else 1 - confidence),
            },
            confidence=float(confidence)
        )
        
        return prediction_obj
