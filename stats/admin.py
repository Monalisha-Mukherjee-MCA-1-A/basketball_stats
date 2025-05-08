from django.contrib import admin
from stats.models import Team, Player, Match, PlayerStats, TeamStats


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'abbreviation', 'conference', 'division')
    list_filter = ('conference', 'division')
    search_fields = ('name', 'city')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position', 'jersey_number', 'is_active')
    list_filter = ('team', 'position', 'is_active')
    search_fields = ('first_name', 'last_name')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date', 'season', 'home_score', 'away_score', 'is_completed')
    list_filter = ('season', 'is_playoff', 'is_completed')
    search_fields = ('home_team__name', 'away_team__name')
    date_hierarchy = 'date'


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'points', 'rebounds', 'assists')
    list_filter = ('match', 'player__team')
    search_fields = ('player__first_name', 'player__last_name')


@admin.register(TeamStats)
class TeamStatsAdmin(admin.ModelAdmin):
    list_display = ('team', 'match', 'points', 'rebounds', 'assists')
    list_filter = ('match', 'team')
    search_fields = ('team__name',)
