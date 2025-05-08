from rest_framework import serializers
from stats.models import Team, Player, Match, PlayerStats, TeamStats
from ml_models.models import MLModel, Prediction, ModelFeature


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model.
    """
    team_name = serializers.ReadOnlyField(source='team.name')
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Player
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer for the Match model.
    """
    home_team_name = serializers.ReadOnlyField(source='home_team.name')
    away_team_name = serializers.ReadOnlyField(source='away_team.name')
    
    class Meta:
        model = Match
        fields = '__all__'


class PlayerStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for the PlayerStats model.
    """
    player_name = serializers.ReadOnlyField(source='player.full_name')
    match_info = serializers.ReadOnlyField(source='match.__str__')
    field_goal_percentage = serializers.ReadOnlyField()
    three_point_percentage = serializers.ReadOnlyField()
    free_throw_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = PlayerStats
        fields = '__all__'


class TeamStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for the TeamStats model.
    """
    team_name = serializers.ReadOnlyField(source='team.name')
    match_info = serializers.ReadOnlyField(source='match.__str__')
    field_goal_percentage = serializers.ReadOnlyField()
    three_point_percentage = serializers.ReadOnlyField()
    free_throw_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = TeamStats
        fields = '__all__'


class MLModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the MLModel model.
    """
    class Meta:
        model = MLModel
        fields = '__all__'


class ModelFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the ModelFeature model.
    """
    model_name = serializers.ReadOnlyField(source='model.name')
    
    class Meta:
        model = ModelFeature
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Prediction model.
    """
    model_name = serializers.ReadOnlyField(source='model.name')
    model_version = serializers.ReadOnlyField(source='model.version')
    
    class Meta:
        model = Prediction
        fields = '__all__'


class PlayerPerformancePredictionSerializer(serializers.Serializer):
    """
    Serializer for player performance prediction requests.
    """
    player_id = serializers.IntegerField()
    match_id = serializers.IntegerField(required=False)
    model_version = serializers.CharField(required=False)


class MatchOutcomePredictionSerializer(serializers.Serializer):
    """
    Serializer for match outcome prediction requests.
    """
    match_id = serializers.IntegerField()
    model_version = serializers.CharField(required=False)


class PlayerComparisonSerializer(serializers.Serializer):
    """
    Serializer for player comparison requests.
    """
    player1_id = serializers.IntegerField()
    player2_id = serializers.IntegerField()
    model_version = serializers.CharField(required=False)
