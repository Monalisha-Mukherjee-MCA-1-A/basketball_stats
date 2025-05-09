# Generated by Django 5.2 on 2025-05-06 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('conference', models.CharField(max_length=50)),
                ('division', models.CharField(max_length=50)),
                ('logo', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='stats_team_name_068737_idx'), models.Index(fields=['conference', 'division'], name='stats_team_confere_85f222_idx')],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('jersey_number', models.IntegerField()),
                ('position', models.CharField(choices=[('PG', 'Point Guard'), ('SG', 'Shooting Guard'), ('SF', 'Small Forward'), ('PF', 'Power Forward'), ('C', 'Center')], max_length=2)),
                ('height', models.FloatField(help_text='Height in meters')),
                ('weight', models.FloatField(help_text='Weight in kilograms')),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='stats.team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('season', models.CharField(max_length=10)),
                ('home_score', models.IntegerField(blank=True, null=True)),
                ('away_score', models.IntegerField(blank=True, null=True)),
                ('is_playoff', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='stats.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='stats.team')),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('rebounds', models.IntegerField()),
                ('offensive_rebounds', models.IntegerField()),
                ('defensive_rebounds', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('personal_fouls', models.IntegerField()),
                ('field_goals_made', models.IntegerField()),
                ('field_goals_attempted', models.IntegerField()),
                ('three_pointers_made', models.IntegerField()),
                ('three_pointers_attempted', models.IntegerField()),
                ('free_throws_made', models.IntegerField()),
                ('free_throws_attempted', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_stats', to='stats.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='stats.team')),
            ],
            options={
                'verbose_name_plural': 'Team Stats',
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes_played', models.IntegerField()),
                ('points', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('rebounds', models.IntegerField()),
                ('offensive_rebounds', models.IntegerField()),
                ('defensive_rebounds', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('personal_fouls', models.IntegerField()),
                ('field_goals_made', models.IntegerField()),
                ('field_goals_attempted', models.IntegerField()),
                ('three_pointers_made', models.IntegerField()),
                ('three_pointers_attempted', models.IntegerField()),
                ('free_throws_made', models.IntegerField()),
                ('free_throws_attempted', models.IntegerField()),
                ('plus_minus', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_stats', to='stats.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='stats.player')),
            ],
            options={
                'verbose_name_plural': 'Player Stats',
                'indexes': [models.Index(fields=['player', 'match'], name='stats_playe_player__ba8899_idx'), models.Index(fields=['match'], name='stats_playe_match_i_8cc6f2_idx'), models.Index(fields=['player'], name='stats_playe_player__fef5b8_idx')],
                'unique_together': {('player', 'match')},
            },
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['last_name', 'first_name'], name='stats_playe_last_na_7211ef_idx'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['team', 'position'], name='stats_playe_team_id_4770d9_idx'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['is_active'], name='stats_playe_is_acti_1df883_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['date'], name='stats_match_date_64392d_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['season'], name='stats_match_season_9411dd_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['home_team', 'away_team'], name='stats_match_home_te_2556fe_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['is_completed'], name='stats_match_is_comp_ff74f7_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['is_playoff'], name='stats_match_is_play_5539bd_idx'),
        ),
        migrations.AddIndex(
            model_name='teamstats',
            index=models.Index(fields=['team', 'match'], name='stats_teams_team_id_6c210d_idx'),
        ),
        migrations.AddIndex(
            model_name='teamstats',
            index=models.Index(fields=['match'], name='stats_teams_match_i_b9090e_idx'),
        ),
        migrations.AddIndex(
            model_name='teamstats',
            index=models.Index(fields=['team'], name='stats_teams_team_id_9f372f_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='teamstats',
            unique_together={('team', 'match')},
        ),
    ]
