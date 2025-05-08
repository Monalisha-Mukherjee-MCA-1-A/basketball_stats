from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from stats.models import Team, Player, Match, PlayerStats, TeamStats
from ml_models.models import MLModel, Prediction
from ml_models.services import ModelService
from django.utils import timezone
import datetime
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


class MLModelTests(TestCase):
    """Tests for the MLModel model."""
    
    def test_ml_model_creation(self):
        """Test creating an ML model."""
        model = MLModel.objects.create(
            name='Player Performance Predictor',
            version='1.0',
            model_type='PLAYER_PERFORMANCE',
            description='Predicts player performance based on historical data',
            file_path='ml_models/models/player_performance_model_v1.pkl',
            is_active=True,
            accuracy=0.85
        )
        self.assertEqual(model.name, 'Player Performance Predictor')
        self.assertEqual(model.version, '1.0')
        self.assertEqual(model.model_type, 'PLAYER_PERFORMANCE')
        self.assertEqual(model.description, 'Predicts player performance based on historical data')
        self.assertEqual(model.file_path, 'ml_models/models/player_performance_model_v1.pkl')
        self.assertEqual(model.is_active, True)
        self.assertEqual(model.accuracy, 0.85)
        self.assertEqual(str(model), 'Player Performance Predictor v1.0')


class PredictionTests(TestCase):
    """Tests for the Prediction model."""
    
    def setUp(self):
        """Set up test data."""
        self.team1 = Team.objects.create(
            name='Lakers',
            abbreviation='LAL',
            city='Los Angeles',
            conference='Western',
            division='Pacific'
        )
        self.team2 = Team.objects.create(
            name='Celtics',
            abbreviation='BOS',
            city='Boston',
            conference='Eastern',
            division='Atlantic'
        )
        self.player = Player.objects.create(
            first_name='LeBron',
            last_name='James',
            jersey_number=23,
            position='SF',
            height=2.06,
            weight=113.4,
            date_of_birth=datetime.date(1984, 12, 30),
            team=self.team1
        )
        self.match = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            date=timezone.now(),
            season='2023-24',
            is_playoff=False,
            is_completed=False
        )
        self.model = MLModel.objects.create(
            name='Player Performance Predictor',
            version='1.0',
            model_type='PLAYER_PERFORMANCE',
            description='Predicts player performance based on historical data',
            file_path='ml_models/models/player_performance_model_v1.pkl',
            is_active=True,
            accuracy=0.85
        )
    
    def test_prediction_creation(self):
        """Test creating a prediction."""
        prediction = Prediction.objects.create(
            model=self.model,
            prediction_type='PLAYER_STATS',
            match=self.match,
            player=self.player,
            prediction_data={
                'points': 25.5,
                'assists': 7.2,
                'rebounds': 8.1,
                'steals': 1.3,
                'blocks': 0.8
            },
            confidence=0.85
        )
        self.assertEqual(prediction.model, self.model)
        self.assertEqual(prediction.prediction_type, 'PLAYER_STATS')
        self.assertEqual(prediction.match, self.match)
        self.assertEqual(prediction.player, self.player)
        self.assertEqual(prediction.prediction_data['points'], 25.5)
        self.assertEqual(prediction.prediction_data['assists'], 7.2)
        self.assertEqual(prediction.prediction_data['rebounds'], 8.1)
        self.assertEqual(prediction.prediction_data['steals'], 1.3)
        self.assertEqual(prediction.prediction_data['blocks'], 0.8)
        self.assertEqual(prediction.confidence, 0.85)
        self.assertEqual(str(prediction), f"PLAYER_STATS prediction for {self.player}")


class ModelServiceTests(TestCase):
    """Tests for the ModelService."""
    
    def setUp(self):
        """Set up test data."""
        # Create teams
        self.team1 = Team.objects.create(
            name='Lakers',
            abbreviation='LAL',
            city='Los Angeles',
            conference='Western',
            division='Pacific'
        )
        self.team2 = Team.objects.create(
            name='Celtics',
            abbreviation='BOS',
            city='Boston',
            conference='Eastern',
            division='Atlantic'
        )
        
        # Create players
        self.player = Player.objects.create(
            first_name='LeBron',
            last_name='James',
            jersey_number=23,
            position='SF',
            height=2.06,
            weight=113.4,
            date_of_birth=datetime.date(1984, 12, 30),
            team=self.team1
        )
        
        # Create matches
        self.match1 = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            date=timezone.now() - datetime.timedelta(days=10),
            season='2023-24',
            home_score=105,
            away_score=102,
            is_playoff=False,
            is_completed=True
        )
        self.match2 = Match.objects.create(
            home_team=self.team2,
            away_team=self.team1,
            date=timezone.now() - datetime.timedelta(days=5),
            season='2023-24',
            home_score=98,
            away_score=110,
            is_playoff=False,
            is_completed=True
        )
        self.match3 = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            date=timezone.now() + datetime.timedelta(days=5),
            season='2023-24',
            is_playoff=False,
            is_completed=False
        )
        
        # Create player stats
        self.player_stats1 = PlayerStats.objects.create(
            player=self.player,
            match=self.match1,
            minutes_played=38,
            points=28,
            assists=8,
            rebounds=10,
            offensive_rebounds=2,
            defensive_rebounds=8,
            steals=2,
            blocks=1,
            turnovers=3,
            personal_fouls=2,
            field_goals_made=10,
            field_goals_attempted=20,
            three_pointers_made=2,
            three_pointers_attempted=6,
            free_throws_made=6,
            free_throws_attempted=8,
            plus_minus=12
        )
        self.player_stats2 = PlayerStats.objects.create(
            player=self.player,
            match=self.match2,
            minutes_played=36,
            points=32,
            assists=11,
            rebounds=7,
            offensive_rebounds=1,
            defensive_rebounds=6,
            steals=1,
            blocks=0,
            turnovers=2,
            personal_fouls=3,
            field_goals_made=12,
            field_goals_attempted=22,
            three_pointers_made=3,
            three_pointers_attempted=8,
            free_throws_made=5,
            free_throws_attempted=6,
            plus_minus=8
        )
        
        # Create team stats
        self.team_stats1 = TeamStats.objects.create(
            team=self.team1,
            match=self.match1,
            points=105,
            assists=25,
            rebounds=45,
            offensive_rebounds=10,
            defensive_rebounds=35,
            steals=8,
            blocks=5,
            turnovers=12,
            personal_fouls=18,
            field_goals_made=40,
            field_goals_attempted=85,
            three_pointers_made=10,
            three_pointers_attempted=30,
            free_throws_made=15,
            free_throws_attempted=20
        )
        self.team_stats2 = TeamStats.objects.create(
            team=self.team2,
            match=self.match1,
            points=102,
            assists=22,
            rebounds=40,
            offensive_rebounds=8,
            defensive_rebounds=32,
            steals=6,
            blocks=4,
            turnovers=14,
            personal_fouls=20,
            field_goals_made=38,
            field_goals_attempted=82,
            three_pointers_made=12,
            three_pointers_attempted=35,
            free_throws_made=14,
            free_throws_attempted=18
        )
        self.team_stats3 = TeamStats.objects.create(
            team=self.team1,
            match=self.match2,
            points=110,
            assists=28,
            rebounds=42,
            offensive_rebounds=9,
            defensive_rebounds=33,
            steals=7,
            blocks=6,
            turnovers=10,
            personal_fouls=16,
            field_goals_made=42,
            field_goals_attempted=88,
            three_pointers_made=8,
            three_pointers_attempted=25,
            free_throws_made=18,
            free_throws_attempted=22
        )
        self.team_stats4 = TeamStats.objects.create(
            team=self.team2,
            match=self.match2,
            points=98,
            assists=20,
            rebounds=38,
            offensive_rebounds=7,
            defensive_rebounds=31,
            steals=5,
            blocks=3,
            turnovers=15,
            personal_fouls=22,
            field_goals_made=36,
            field_goals_attempted=80,
            three_pointers_made=10,
            three_pointers_attempted=28,
            free_throws_made=16,
            free_throws_attempted=20
        )
        
        # Create ML models
        os.makedirs('ml_models/models', exist_ok=True)
        
        # Create a simple player performance model
        player_model = RandomForestRegressor(n_estimators=10, random_state=42)
        player_model.fit(
            np.array([[2.06, 113.4, 30, 28, 8, 10, 2, 1]]),
            np.array([[30, 9, 8, 2, 1]])
        )
        with open('ml_models/models/player_performance_model_v1.pkl', 'wb') as f:
            pickle.dump(player_model, f)
        
        # Create a simple match outcome model
        match_model = RandomForestClassifier(n_estimators=10, random_state=42)
        match_model.fit(
            np.array([[105, 45, 25, 8, 5, 102, 40, 22, 6, 4]]),
            np.array([1])  # 1 for home win
        )
        with open('ml_models/models/match_outcome_model_v1.pkl', 'wb') as f:
            pickle.dump(match_model, f)
        
        self.player_model = MLModel.objects.create(
            name='Player Performance Predictor',
            version='1.0',
            model_type='PLAYER_PERFORMANCE',
            description='Predicts player performance based on historical data',
            file_path='ml_models/models/player_performance_model_v1.pkl',
            is_active=True,
            accuracy=0.85
        )
        self.match_model = MLModel.objects.create(
            name='Match Outcome Predictor',
            version='1.0',
            model_type='MATCH_OUTCOME',
            description='Predicts match outcomes based on team statistics',
            file_path='ml_models/models/match_outcome_model_v1.pkl',
            is_active=True,
            accuracy=0.72
        )
    
    def test_prepare_player_features(self):
        """Test preparing player features."""
        features = ModelService.prepare_player_features(self.player)
        self.assertIsNotNone(features)
        self.assertEqual(features['player_id'], self.player.id)
        self.assertEqual(features['position'], self.player.position)
        self.assertEqual(features['height'], self.player.height)
        self.assertEqual(features['weight'], self.player.weight)
        self.assertEqual(features['age'], self.player.age)
        self.assertEqual(features['avg_points'], 30)  # (28 + 32) / 2
        self.assertEqual(features['avg_assists'], 9.5)  # (8 + 11) / 2
        self.assertEqual(features['avg_rebounds'], 8.5)  # (10 + 7) / 2
        self.assertEqual(features['avg_steals'], 1.5)  # (2 + 1) / 2
        self.assertEqual(features['avg_blocks'], 0.5)  # (1 + 0) / 2
        self.assertEqual(features['avg_minutes'], 37)  # (38 + 36) / 2
    
    def test_prepare_match_features(self):
        """Test preparing match features."""
        features = ModelService.prepare_match_features(self.match3)
        self.assertIsNotNone(features)
        self.assertEqual(features['home_team_id'], self.team1.id)
        self.assertEqual(features['away_team_id'], self.team2.id)
        self.assertEqual(features['home_avg_points'], 107.5)  # (105 + 110) / 2
        self.assertEqual(features['home_avg_rebounds'], 43.5)  # (45 + 42) / 2
        self.assertEqual(features['home_avg_assists'], 26.5)  # (25 + 28) / 2
        self.assertEqual(features['home_avg_steals'], 7.5)  # (8 + 7) / 2
        self.assertEqual(features['home_avg_blocks'], 5.5)  # (5 + 6) / 2
        self.assertEqual(features['away_avg_points'], 100)  # (102 + 98) / 2
        self.assertEqual(features['away_avg_rebounds'], 39)  # (40 + 38) / 2
        self.assertEqual(features['away_avg_assists'], 21)  # (22 + 20) / 2
        self.assertEqual(features['away_avg_steals'], 5.5)  # (6 + 5) / 2
        self.assertEqual(features['away_avg_blocks'], 3.5)  # (4 + 3) / 2
