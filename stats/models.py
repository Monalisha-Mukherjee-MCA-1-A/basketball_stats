from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Team(models.Model):
    """
    Model representing a basketball team.
    """
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    conference = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    logo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['conference', 'division']),
        ]

    def __str__(self):
        return f"{self.city} {self.name}"


class Player(models.Model):
    """
    Model representing a basketball player.
    """
    POSITION_CHOICES = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    jersey_number = models.IntegerField()
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    height = models.FloatField(help_text="Height in meters")
    weight = models.FloatField(help_text="Weight in kilograms")
    date_of_birth = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['team', 'position']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Match(models.Model):
    """
    Model representing a basketball match between two teams.
    """
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateTimeField()
    season = models.CharField(max_length=10)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    is_playoff = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['season']),
            models.Index(fields=['home_team', 'away_team']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['is_playoff']),
        ]
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date.strftime('%Y-%m-%d')})"


class PlayerStats(models.Model):
    """
    Model representing a player's statistics in a specific match.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_stats')
    minutes_played = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    personal_fouls = models.IntegerField()
    field_goals_made = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    plus_minus = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['player', 'match']),
            models.Index(fields=['match']),
            models.Index(fields=['player']),
        ]
        verbose_name_plural = 'Player Stats'
        unique_together = ('player', 'match')

    def __str__(self):
        return f"{self.player} stats for {self.match}"

    @property
    def field_goal_percentage(self):
        if self.field_goals_attempted == 0:
            return 0
        return round(self.field_goals_made / self.field_goals_attempted * 100, 1)

    @property
    def three_point_percentage(self):
        if self.three_pointers_attempted == 0:
            return 0
        return round(self.three_pointers_made / self.three_pointers_attempted * 100, 1)

    @property
    def free_throw_percentage(self):
        if self.free_throws_attempted == 0:
            return 0
        return round(self.free_throws_made / self.free_throws_attempted * 100, 1)


class TeamStats(models.Model):
    """
    Model representing a team's statistics in a specific match.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='team_stats')
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    personal_fouls = models.IntegerField()
    field_goals_made = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['team', 'match']),
            models.Index(fields=['match']),
            models.Index(fields=['team']),
        ]
        verbose_name_plural = 'Team Stats'
        unique_together = ('team', 'match')

    def __str__(self):
        return f"{self.team} stats for {self.match}"

    @property
    def field_goal_percentage(self):
        if self.field_goals_attempted == 0:
            return 0
        return round(self.field_goals_made / self.field_goals_attempted * 100, 1)

    @property
    def three_point_percentage(self):
        if self.three_pointers_attempted == 0:
            return 0
        return round(self.three_pointers_made / self.three_pointers_attempted * 100, 1)

    @property
    def free_throw_percentage(self):
        if self.free_throws_attempted == 0:
            return 0
        return round(self.free_throws_made / self.free_throws_attempted * 100, 1)
