from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from stats.models import Team, Player, Match, PlayerStats, TeamStats
from ml_models.models import MLModel, Prediction, ModelFeature
from ml_models.services import ModelService
from api.serializers import (
    TeamSerializer, 
    PlayerSerializer, 
    MatchSerializer, 
    PlayerStatsSerializer, 
    TeamStatsSerializer,
    MLModelSerializer,
    ModelFeatureSerializer,
    PredictionSerializer,
    PlayerPerformancePredictionSerializer,
    MatchOutcomePredictionSerializer,
    PlayerComparisonSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conference', 'division']
    
    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        """
        Return a list of all players for a specific team.
        """
        team = self.get_object()
        players = Player.objects.filter(team=team)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """
        Return a list of all matches for a specific team.
        """
        team = self.get_object()
        matches = Match.objects.filter(home_team=team) | Match.objects.filter(away_team=team)
        matches = matches.order_by('-date')
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Return a list of all stats for a specific team.
        """
        team = self.get_object()
        stats = TeamStats.objects.filter(team=team).order_by('-match__date')
        serializer = TeamStatsSerializer(stats, many=True)
        return Response(serializer.data)


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all().order_by('last_name', 'first_name')
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'position', 'is_active']
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Return a list of all stats for a specific player.
        """
        player = self.get_object()
        stats = PlayerStats.objects.filter(player=player).order_by('-match__date')
        serializer = PlayerStatsSerializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """
        Return a list of all matches for a specific player.
        """
        player = self.get_object()
        player_stats = PlayerStats.objects.filter(player=player)
        matches = Match.objects.filter(player_stats__in=player_stats).order_by('-date')
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict_performance(self, request, pk=None):
        """
        Predict performance for a specific player.
        """
        player = self.get_object()
        serializer = PlayerPerformancePredictionSerializer(data=request.data)
        
        if serializer.is_valid():
            match_id = serializer.validated_data.get('match_id')
            model_version = serializer.validated_data.get('model_version')
            
            match = None
            if match_id:
                match = get_object_or_404(Match, pk=match_id)
            
            try:
                prediction = ModelService.predict_player_performance(
                    player, match, model_version
                )
                prediction_serializer = PredictionSerializer(prediction)
                return Response(prediction_serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows matches to be viewed or edited.
    """
    queryset = Match.objects.all().order_by('-date')
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['home_team', 'away_team', 'season', 'is_playoff', 'is_completed']
    
    @action(detail=True, methods=['get'])
    def player_stats(self, request, pk=None):
        """
        Return a list of all player stats for a specific match.
        """
        match = self.get_object()
        stats = PlayerStats.objects.filter(match=match)
        serializer = PlayerStatsSerializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def team_stats(self, request, pk=None):
        """
        Return a list of all team stats for a specific match.
        """
        match = self.get_object()
        stats = TeamStats.objects.filter(match=match)
        serializer = TeamStatsSerializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict_outcome(self, request, pk=None):
        """
        Predict outcome for a specific match.
        """
        match = self.get_object()
        serializer = MatchOutcomePredictionSerializer(data=request.data)
        
        if serializer.is_valid():
            model_version = serializer.validated_data.get('model_version')
            
            try:
                prediction = ModelService.predict_match_outcome(
                    match, model_version
                )
                prediction_serializer = PredictionSerializer(prediction)
                return Response(prediction_serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows player stats to be viewed or edited.
    """
    queryset = PlayerStats.objects.all().order_by('-match__date')
    serializer_class = PlayerStatsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['player', 'match']


class TeamStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows team stats to be viewed or edited.
    """
    queryset = TeamStats.objects.all().order_by('-match__date')
    serializer_class = TeamStatsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'match']


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows predictions to be viewed.
    """
    queryset = Prediction.objects.all().order_by('-created_at')
    serializer_class = PredictionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prediction_type', 'match', 'player', 'team', 'model']
    
    @action(detail=False, methods=['post'])
    def compare_players(self, request):
        """
        Compare two players.
        """
        serializer = PlayerComparisonSerializer(data=request.data)
        
        if serializer.is_valid():
            player1_id = serializer.validated_data.get('player1_id')
            player2_id = serializer.validated_data.get('player2_id')
            model_version = serializer.validated_data.get('model_version')
            
            player1 = get_object_or_404(Player, pk=player1_id)
            player2 = get_object_or_404(Player, pk=player2_id)
            
            # Get the ML model
            model_instance = ModelService.get_model('PLAYER_COMPARISON', model_version)
            if not model_instance:
                return Response(
                    {'error': 'No active player comparison model found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Prepare features for both players
                features1 = ModelService.prepare_player_features(player1)
                features2 = ModelService.prepare_player_features(player2)
                
                if not features1 or not features2:
                    return Response(
                        {'error': 'Not enough data to make a comparison'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Compare players (simplified for example)
                comparison_data = {
                    'player1': {
                        'id': player1.id,
                        'name': player1.full_name,
                        'avg_points': features1['avg_points'],
                        'avg_assists': features1['avg_assists'],
                        'avg_rebounds': features1['avg_rebounds'],
                    },
                    'player2': {
                        'id': player2.id,
                        'name': player2.full_name,
                        'avg_points': features2['avg_points'],
                        'avg_assists': features2['avg_assists'],
                        'avg_rebounds': features2['avg_rebounds'],
                    },
                    'comparison': {
                        'points_diff': features1['avg_points'] - features2['avg_points'],
                        'assists_diff': features1['avg_assists'] - features2['avg_assists'],
                        'rebounds_diff': features1['avg_rebounds'] - features2['avg_rebounds'],
                    }
                }
                
                # Create prediction object
                prediction = Prediction.objects.create(
                    model=model_instance,
                    prediction_type='PLAYER_COMPARISON',
                    player=player1,  # Reference to first player
                    prediction_data=comparison_data,
                    confidence=0.9  # Placeholder
                )
                
                prediction_serializer = PredictionSerializer(prediction)
                return Response(prediction_serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
