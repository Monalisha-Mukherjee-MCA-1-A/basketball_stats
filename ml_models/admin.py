from django.contrib import admin
from ml_models.models import MLModel, Prediction, ModelFeature


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_type', 'is_active', 'accuracy')
    list_filter = ('model_type', 'is_active')
    search_fields = ('name', 'description')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('prediction_type', 'model', 'match', 'player', 'team', 'confidence', 'was_correct')
    list_filter = ('prediction_type', 'model', 'was_correct')
    search_fields = ('match__home_team__name', 'match__away_team__name', 'player__first_name', 'player__last_name')


@admin.register(ModelFeature)
class ModelFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'importance')
    list_filter = ('model',)
    search_fields = ('name', 'description')
