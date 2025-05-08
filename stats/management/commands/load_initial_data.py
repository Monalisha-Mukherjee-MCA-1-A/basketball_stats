"""
Management command to load initial data for the basketball stats app.
"""

import os
import datetime
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from stats.models import Team, Player, Match, PlayerStats, TeamStats
from ml_models.models import MLModel


class Command(BaseCommand):
    help = 'Load initial data for the basketball stats app'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create teams
        self.create_teams()
        
        # Create players
        self.create_players()
        
        # Create matches
        self.create_matches()
        
        # Create player stats
        self.create_player_stats()
        
        # Create team stats
        self.create_team_stats()
        
        # Create ML models
        self.create_ml_models()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))

    def create_teams(self):
        """Create sample teams."""
        if Team.objects.exists():
            self.stdout.write('Teams already exist, skipping...')
            return
        
        teams_data = [
            {'name': 'Lakers', 'abbreviation': 'LAL', 'city': 'Los Angeles', 'conference': 'Western', 'division': 'Pacific'},
            {'name': 'Celtics', 'abbreviation': 'BOS', 'city': 'Boston', 'conference': 'Eastern', 'division': 'Atlantic'},
            {'name': 'Warriors', 'abbreviation': 'GSW', 'city': 'Golden State', 'conference': 'Western', 'division': 'Pacific'},
            {'name': 'Bucks', 'abbreviation': 'MIL', 'city': 'Milwaukee', 'conference': 'Eastern', 'division': 'Central'},
            {'name': 'Heat', 'abbreviation': 'MIA', 'city': 'Miami', 'conference': 'Eastern', 'division': 'Southeast'},
            {'name': 'Nuggets', 'abbreviation': 'DEN', 'city': 'Denver', 'conference': 'Western', 'division': 'Northwest'},
            {'name': 'Mavericks', 'abbreviation': 'DAL', 'city': 'Dallas', 'conference': 'Western', 'division': 'Southwest'},
            {'name': '76ers', 'abbreviation': 'PHI', 'city': 'Philadelphia', 'conference': 'Eastern', 'division': 'Atlantic'},
        ]
        
        for team_data in teams_data:
            Team.objects.create(**team_data)
        
        self.stdout.write(f'Created {len(teams_data)} teams')

    def create_players(self):
        """Create sample players."""
        if Player.objects.exists():
            self.stdout.write('Players already exist, skipping...')
            return
        
        teams = Team.objects.all()
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        
        players_data = []
        for team in teams:
            for i in range(12):  # 12 players per team
                position = positions[i % 5]
                jersey_number = i + 1
                height = round(random.uniform(1.80, 2.20), 2)
                weight = round(random.uniform(75, 120), 1)
                dob = timezone.now().date() - datetime.timedelta(days=random.randint(8000, 12000))
                
                player_data = {
                    'first_name': f'Player{i+1}',
                    'last_name': f'{team.name}{i+1}',
                    'jersey_number': jersey_number,
                    'position': position,
                    'height': height,
                    'weight': weight,
                    'date_of_birth': dob,
                    'team': team,
                }
                players_data.append(player_data)
        
        for player_data in players_data:
            Player.objects.create(**player_data)
        
        self.stdout.write(f'Created {len(players_data)} players')

    def create_matches(self):
        """Create sample matches."""
        if Match.objects.exists():
            self.stdout.write('Matches already exist, skipping...')
            return
        
        teams = list(Team.objects.all())
        matches_data = []
        
        # Create matches for the current season
        season = '2023-24'
        start_date = timezone.now().date() - datetime.timedelta(days=180)
        
        for i in range(50):  # 50 matches
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t != home_team])
            date = start_date + datetime.timedelta(days=i)
            is_completed = date < timezone.now().date()
            
            if is_completed:
                home_score = random.randint(85, 130)
                away_score = random.randint(85, 130)
            else:
                home_score = None
                away_score = None
            
            match_data = {
                'home_team': home_team,
                'away_team': away_team,
                'date': timezone.make_aware(datetime.datetime.combine(date, datetime.time(19, 0))),
                'season': season,
                'home_score': home_score,
                'away_score': away_score,
                'is_playoff': False,
                'is_completed': is_completed,
            }
            matches_data.append(match_data)
        
        for match_data in matches_data:
            Match.objects.create(**match_data)
        
        self.stdout.write(f'Created {len(matches_data)} matches')

    def create_player_stats(self):
        """Create sample player stats."""
        if PlayerStats.objects.exists():
            self.stdout.write('Player stats already exist, skipping...')
            return
        
        completed_matches = Match.objects.filter(is_completed=True)
        player_stats_data = []
        
        for match in completed_matches:
            # Get players from both teams
            home_players = Player.objects.filter(team=match.home_team)
            away_players = Player.objects.filter(team=match.away_team)
            
            # Create stats for home team players
            for player in home_players:
                minutes_played = random.randint(10, 40)
                field_goals_attempted = random.randint(5, 25)
                field_goals_made = random.randint(0, field_goals_attempted)
                three_pointers_attempted = random.randint(0, 15)
                three_pointers_made = random.randint(0, min(three_pointers_attempted, field_goals_made))
                free_throws_attempted = random.randint(0, 15)
                free_throws_made = random.randint(0, free_throws_attempted)
                
                points = (field_goals_made - three_pointers_made) * 2 + three_pointers_made * 3 + free_throws_made
                
                player_stat_data = {
                    'player': player,
                    'match': match,
                    'minutes_played': minutes_played,
                    'points': points,
                    'assists': random.randint(0, 15),
                    'rebounds': random.randint(0, 15),
                    'offensive_rebounds': random.randint(0, 5),
                    'defensive_rebounds': random.randint(0, 10),
                    'steals': random.randint(0, 5),
                    'blocks': random.randint(0, 5),
                    'turnovers': random.randint(0, 5),
                    'personal_fouls': random.randint(0, 6),
                    'field_goals_made': field_goals_made,
                    'field_goals_attempted': field_goals_attempted,
                    'three_pointers_made': three_pointers_made,
                    'three_pointers_attempted': three_pointers_attempted,
                    'free_throws_made': free_throws_made,
                    'free_throws_attempted': free_throws_attempted,
                    'plus_minus': random.randint(-20, 20),
                }
                player_stats_data.append(player_stat_data)
            
            # Create stats for away team players
            for player in away_players:
                minutes_played = random.randint(10, 40)
                field_goals_attempted = random.randint(5, 25)
                field_goals_made = random.randint(0, field_goals_attempted)
                three_pointers_attempted = random.randint(0, 15)
                three_pointers_made = random.randint(0, min(three_pointers_attempted, field_goals_made))
                free_throws_attempted = random.randint(0, 15)
                free_throws_made = random.randint(0, free_throws_attempted)
                
                points = (field_goals_made - three_pointers_made) * 2 + three_pointers_made * 3 + free_throws_made
                
                player_stat_data = {
                    'player': player,
                    'match': match,
                    'minutes_played': minutes_played,
                    'points': points,
                    'assists': random.randint(0, 15),
                    'rebounds': random.randint(0, 15),
                    'offensive_rebounds': random.randint(0, 5),
                    'defensive_rebounds': random.randint(0, 10),
                    'steals': random.randint(0, 5),
                    'blocks': random.randint(0, 5),
                    'turnovers': random.randint(0, 5),
                    'personal_fouls': random.randint(0, 6),
                    'field_goals_made': field_goals_made,
                    'field_goals_attempted': field_goals_attempted,
                    'three_pointers_made': three_pointers_made,
                    'three_pointers_attempted': three_pointers_attempted,
                    'free_throws_made': free_throws_made,
                    'free_throws_attempted': free_throws_attempted,
                    'plus_minus': random.randint(-20, 20),
                }
                player_stats_data.append(player_stat_data)
        
        for player_stat_data in player_stats_data:
            PlayerStats.objects.create(**player_stat_data)
        
        self.stdout.write(f'Created {len(player_stats_data)} player stats')

    def create_team_stats(self):
        """Create sample team stats."""
        if TeamStats.objects.exists():
            self.stdout.write('Team stats already exist, skipping...')
            return
        
        completed_matches = Match.objects.filter(is_completed=True)
        team_stats_data = []
        
        for match in completed_matches:
            # Create stats for home team
            home_player_stats = PlayerStats.objects.filter(match=match, player__team=match.home_team)
            
            if home_player_stats.exists():
                home_points = sum(stat.points for stat in home_player_stats)
                home_assists = sum(stat.assists for stat in home_player_stats)
                home_rebounds = sum(stat.rebounds for stat in home_player_stats)
                home_offensive_rebounds = sum(stat.offensive_rebounds for stat in home_player_stats)
                home_defensive_rebounds = sum(stat.defensive_rebounds for stat in home_player_stats)
                home_steals = sum(stat.steals for stat in home_player_stats)
                home_blocks = sum(stat.blocks for stat in home_player_stats)
                home_turnovers = sum(stat.turnovers for stat in home_player_stats)
                home_personal_fouls = sum(stat.personal_fouls for stat in home_player_stats)
                home_field_goals_made = sum(stat.field_goals_made for stat in home_player_stats)
                home_field_goals_attempted = sum(stat.field_goals_attempted for stat in home_player_stats)
                home_three_pointers_made = sum(stat.three_pointers_made for stat in home_player_stats)
                home_three_pointers_attempted = sum(stat.three_pointers_attempted for stat in home_player_stats)
                home_free_throws_made = sum(stat.free_throws_made for stat in home_player_stats)
                home_free_throws_attempted = sum(stat.free_throws_attempted for stat in home_player_stats)
                
                team_stat_data = {
                    'team': match.home_team,
                    'match': match,
                    'points': home_points,
                    'assists': home_assists,
                    'rebounds': home_rebounds,
                    'offensive_rebounds': home_offensive_rebounds,
                    'defensive_rebounds': home_defensive_rebounds,
                    'steals': home_steals,
                    'blocks': home_blocks,
                    'turnovers': home_turnovers,
                    'personal_fouls': home_personal_fouls,
                    'field_goals_made': home_field_goals_made,
                    'field_goals_attempted': home_field_goals_attempted,
                    'three_pointers_made': home_three_pointers_made,
                    'three_pointers_attempted': home_three_pointers_attempted,
                    'free_throws_made': home_free_throws_made,
                    'free_throws_attempted': home_free_throws_attempted,
                }
                team_stats_data.append(team_stat_data)
            
            # Create stats for away team
            away_player_stats = PlayerStats.objects.filter(match=match, player__team=match.away_team)
            
            if away_player_stats.exists():
                away_points = sum(stat.points for stat in away_player_stats)
                away_assists = sum(stat.assists for stat in away_player_stats)
                away_rebounds = sum(stat.rebounds for stat in away_player_stats)
                away_offensive_rebounds = sum(stat.offensive_rebounds for stat in away_player_stats)
                away_defensive_rebounds = sum(stat.defensive_rebounds for stat in away_player_stats)
                away_steals = sum(stat.steals for stat in away_player_stats)
                away_blocks = sum(stat.blocks for stat in away_player_stats)
                away_turnovers = sum(stat.turnovers for stat in away_player_stats)
                away_personal_fouls = sum(stat.personal_fouls for stat in away_player_stats)
                away_field_goals_made = sum(stat.field_goals_made for stat in away_player_stats)
                away_field_goals_attempted = sum(stat.field_goals_attempted for stat in away_player_stats)
                away_three_pointers_made = sum(stat.three_pointers_made for stat in away_player_stats)
                away_three_pointers_attempted = sum(stat.three_pointers_attempted for stat in away_player_stats)
                away_free_throws_made = sum(stat.free_throws_made for stat in away_player_stats)
                away_free_throws_attempted = sum(stat.free_throws_attempted for stat in away_player_stats)
                
                team_stat_data = {
                    'team': match.away_team,
                    'match': match,
                    'points': away_points,
                    'assists': away_assists,
                    'rebounds': away_rebounds,
                    'offensive_rebounds': away_offensive_rebounds,
                    'defensive_rebounds': away_defensive_rebounds,
                    'steals': away_steals,
                    'blocks': away_blocks,
                    'turnovers': away_turnovers,
                    'personal_fouls': away_personal_fouls,
                    'field_goals_made': away_field_goals_made,
                    'field_goals_attempted': away_field_goals_attempted,
                    'three_pointers_made': away_three_pointers_made,
                    'three_pointers_attempted': away_three_pointers_attempted,
                    'free_throws_made': away_free_throws_made,
                    'free_throws_attempted': away_free_throws_attempted,
                }
                team_stats_data.append(team_stat_data)
        
        for team_stat_data in team_stats_data:
            TeamStats.objects.create(**team_stat_data)
        
        self.stdout.write(f'Created {len(team_stats_data)} team stats')

    def create_ml_models(self):
        """Create sample ML models."""
        if MLModel.objects.exists():
            self.stdout.write('ML models already exist, skipping...')
            return
        
        # Create models directory if it doesn't exist
        os.makedirs('ml_models/models', exist_ok=True)
        
        ml_models_data = [
            {
                'name': 'Player Performance Predictor',
                'version': '1.0',
                'model_type': 'PLAYER_PERFORMANCE',
                'description': 'Predicts player performance based on historical data',
                'file_path': 'ml_models/models/player_performance_model_v1.pkl',
                'is_active': True,
                'accuracy': 0.85,
            },
            {
                'name': 'Match Outcome Predictor',
                'version': '1.0',
                'model_type': 'MATCH_OUTCOME',
                'description': 'Predicts match outcomes based on team statistics',
                'file_path': 'ml_models/models/match_outcome_model_v1.pkl',
                'is_active': True,
                'accuracy': 0.72,
            },
            {
                'name': 'Player Comparison Model',
                'version': '1.0',
                'model_type': 'PLAYER_COMPARISON',
                'description': 'Compares players based on their statistics',
                'file_path': 'ml_models/models/player_comparison_model_v1.pkl',
                'is_active': True,
                'accuracy': 0.90,
            },
        ]
        
        for ml_model_data in ml_models_data:
            MLModel.objects.create(**ml_model_data)
        
        self.stdout.write(f'Created {len(ml_models_data)} ML models')
