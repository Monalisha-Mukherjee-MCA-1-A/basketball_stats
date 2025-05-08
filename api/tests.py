from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from stats.models import Team, Player, Match, PlayerStats, TeamStats
from ml_models.models import MLModel, Prediction
from django.utils import timezone
import datetime
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


class APIEndpointTests(TestCase):
    """Tests for the API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
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
        self.player1 = Player.objects.create(
            first_name='LeBron',
            last_name='James',
            jersey_number=23,
            position='SF',
            height=2.06,
            weight=113.4,
            date_of_birth=datetime.date(1984, 12, 30),
            team=self.team1
        )
        self.player2 = Player.objects.create(
            first_name='Jayson',
            last_name='Tatum',
            jersey_number=0,
            position='SF',
            height=2.03,
            weight=95.3,
            date_of_birth=datetime.date(1998, 3, 3),
            team=self.team2
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
            player=self.player1,
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
            player=self.player1,
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
    
    def test_get_teams(self):
        """Test getting teams."""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_players(self):
        """Test getting players."""
        url = reverse('player-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_matches(self):
        """Test getting matches."""
        url = reverse('match-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_get_player_stats(self):
        """Test getting player stats."""
        url = reverse('playerstats-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_team_stats(self):
        """Test getting team stats."""
        url = reverse('teamstats-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_teams_by_conference(self):
        """Test filtering teams by conference."""
        url = reverse('team-list')
        response = self.client.get(url, {'conference': 'Western'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Lakers')
    
    def test_filter_players_by_team(self):
        """Test filtering players by team."""
        url = reverse('player-list')
        response = self.client.get(url, {'team': self.team1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['last_name'], 'James')
    
    def test_filter_matches_by_team(self):
        """Test filtering matches by team."""
        url = reverse('match-list')
        response = self.client.get(url, {'home_team': self.team1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_team_players_action(self):
        """Test team players action."""
        url = reverse('team-players', args=[self.team1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['last_name'], 'James')
    
    def test_team_matches_action(self):
        """Test team matches action."""
        url = reverse('team-matches', args=[self.team1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_player_stats_action(self):
        """Test player stats action."""
        url = reverse('player-stats', args=[self.player1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_match_player_stats_action(self):
        """Test match player stats action."""
        url = reverse('match-player-stats', args=[self.match1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['points'], 28)
    
    def test_match_team_stats_action(self):
        """Test match team stats action."""
        url = reverse('match-team-stats', args=[self.match1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['points'] + response.data[1]['points'], 207)  # 105 + 102
