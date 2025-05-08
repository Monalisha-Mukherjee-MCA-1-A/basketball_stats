from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from stats.models import Team, Player, Match
from django.utils import timezone
import datetime


class TeamModelTests(TestCase):
    """Tests for the Team model."""
    
    def test_team_creation(self):
        """Test creating a team."""
        team = Team.objects.create(
            name='Lakers',
            abbreviation='LAL',
            city='Los Angeles',
            conference='Western',
            division='Pacific'
        )
        self.assertEqual(team.name, 'Lakers')
        self.assertEqual(team.abbreviation, 'LAL')
        self.assertEqual(team.city, 'Los Angeles')
        self.assertEqual(team.conference, 'Western')
        self.assertEqual(team.division, 'Pacific')
        self.assertEqual(str(team), 'Los Angeles Lakers')


class PlayerModelTests(TestCase):
    """Tests for the Player model."""
    
    def setUp(self):
        """Set up test data."""
        self.team = Team.objects.create(
            name='Lakers',
            abbreviation='LAL',
            city='Los Angeles',
            conference='Western',
            division='Pacific'
        )
    
    def test_player_creation(self):
        """Test creating a player."""
        player = Player.objects.create(
            first_name='LeBron',
            last_name='James',
            jersey_number=23,
            position='SF',
            height=2.06,
            weight=113.4,
            date_of_birth=datetime.date(1984, 12, 30),
            team=self.team
        )
        self.assertEqual(player.first_name, 'LeBron')
        self.assertEqual(player.last_name, 'James')
        self.assertEqual(player.jersey_number, 23)
        self.assertEqual(player.position, 'SF')
        self.assertEqual(player.height, 2.06)
        self.assertEqual(player.weight, 113.4)
        self.assertEqual(player.date_of_birth, datetime.date(1984, 12, 30))
        self.assertEqual(player.team, self.team)
        self.assertEqual(str(player), 'LeBron James')
        self.assertEqual(player.full_name, 'LeBron James')


class MatchModelTests(TestCase):
    """Tests for the Match model."""
    
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
    
    def test_match_creation(self):
        """Test creating a match."""
        match_date = timezone.now()
        match = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            date=match_date,
            season='2023-24',
            home_score=105,
            away_score=102,
            is_playoff=False,
            is_completed=True
        )
        self.assertEqual(match.home_team, self.team1)
        self.assertEqual(match.away_team, self.team2)
        self.assertEqual(match.date, match_date)
        self.assertEqual(match.season, '2023-24')
        self.assertEqual(match.home_score, 105)
        self.assertEqual(match.away_score, 102)
        self.assertEqual(match.is_playoff, False)
        self.assertEqual(match.is_completed, True)
        self.assertEqual(str(match), f"Los Angeles Lakers vs Boston Celtics ({match_date.strftime('%Y-%m-%d')})")


class APITests(TestCase):
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
        
        # Create match
        self.match = Match.objects.create(
            home_team=self.team1,
            away_team=self.team2,
            date=timezone.now(),
            season='2023-24',
            home_score=105,
            away_score=102,
            is_playoff=False,
            is_completed=True
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
        self.assertEqual(len(response.data['results']), 1)
    
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
