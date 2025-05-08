from django.db import models
from stats.models import Team, Player, Match


class MLModel(models.Model):
    """
    Model representing a machine learning model.
    """
    MODEL_TYPES = [
        ('PLAYER_PERFORMANCE', 'Player Performance Prediction'),
        ('MATCH_OUTCOME', 'Match Outcome Prediction'),
        ('PLAYER_COMPARISON', 'Player Comparison'),
        ('TEAM_PERFORMANCE', 'Team Performance Prediction'),
    ]

    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    description = models.TextField()
    file_path = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['version']),
        ]
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} v{self.version}"


class Prediction(models.Model):
    """
    Model representing a prediction made by a machine learning model.
    """
    PREDICTION_TYPES = [
        ('PLAYER_STATS', 'Player Statistics'),
        ('MATCH_WINNER', 'Match Winner'),
        ('SCORE', 'Score Prediction'),
        ('PLAYER_COMPARISON', 'Player Comparison'),
    ]

    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='predictions')
    prediction_type = models.CharField(max_length=50, choices=PREDICTION_TYPES)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    prediction_data = models.JSONField()
    confidence = models.FloatField()
    was_correct = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['prediction_type']),
            models.Index(fields=['match']),
            models.Index(fields=['player']),
            models.Index(fields=['team']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        if self.match:
            return f"{self.prediction_type} prediction for {self.match}"
        elif self.player:
            return f"{self.prediction_type} prediction for {self.player}"
        elif self.team:
            return f"{self.prediction_type} prediction for {self.team}"
        return f"{self.prediction_type} prediction"


class ModelFeature(models.Model):
    """
    Model representing a feature used by a machine learning model.
    """
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    description = models.TextField()
    importance = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model']),
            models.Index(fields=['name']),
        ]
        unique_together = ('model', 'name')

    def __str__(self):
        return f"{self.name} (for {self.model})"
