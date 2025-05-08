from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    TeamViewSet,
    PlayerViewSet,
    MatchViewSet,
    PredictionViewSet,
    PlayerStatsViewSet,
    TeamStatsViewSet
)
from api.auth import (
    UserRegistrationView,
    CustomAuthToken,
    UserDetailView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'predictions', PredictionViewSet)
router.register(r'player-stats', PlayerStatsViewSet)
router.register(r'team-stats', TeamStatsViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/token/', CustomAuthToken.as_view(), name='token'),
    path('auth/user/', UserDetailView.as_view(), name='user-detail'),
]
