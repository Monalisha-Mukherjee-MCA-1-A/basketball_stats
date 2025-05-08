# Basketball Statistics API Documentation

## Overview

This API provides access to basketball statistics and predictions. It allows you to retrieve information about teams, players, matches, and statistics, as well as make predictions using machine learning models.

## Authentication

The API uses token-based authentication. To get a token:

1. Create a user account
2. Make a POST request to `/api-token-auth/` with your username and password
3. Use the token in the Authorization header: `Authorization: Token <your-token>`

## Endpoints

### Teams

- `GET /api/teams/`: List all teams
- `GET /api/teams/{id}/`: Get a specific team
- `POST /api/teams/`: Create a new team
- `PUT /api/teams/{id}/`: Update a team
- `DELETE /api/teams/{id}/`: Delete a team
- `GET /api/teams/{id}/players/`: Get all players for a team
- `GET /api/teams/{id}/matches/`: Get all matches for a team
- `GET /api/teams/{id}/stats/`: Get all stats for a team

### Players

- `GET /api/players/`: List all players
- `GET /api/players/{id}/`: Get a specific player
- `POST /api/players/`: Create a new player
- `PUT /api/players/{id}/`: Update a player
- `DELETE /api/players/{id}/`: Delete a player
- `GET /api/players/{id}/stats/`: Get all stats for a player
- `GET /api/players/{id}/matches/`: Get all matches for a player
- `POST /api/players/{id}/predict_performance/`: Predict performance for a player

### Matches

- `GET /api/matches/`: List all matches
- `GET /api/matches/{id}/`: Get a specific match
- `POST /api/matches/`: Create a new match
- `PUT /api/matches/{id}/`: Update a match
- `DELETE /api/matches/{id}/`: Delete a match
- `GET /api/matches/{id}/player_stats/`: Get all player stats for a match
- `GET /api/matches/{id}/team_stats/`: Get all team stats for a match
- `POST /api/matches/{id}/predict_outcome/`: Predict outcome for a match

### Player Stats

- `GET /api/player-stats/`: List all player stats
- `GET /api/player-stats/{id}/`: Get specific player stats
- `POST /api/player-stats/`: Create new player stats
- `PUT /api/player-stats/{id}/`: Update player stats
- `DELETE /api/player-stats/{id}/`: Delete player stats

### Team Stats

- `GET /api/team-stats/`: List all team stats
- `GET /api/team-stats/{id}/`: Get specific team stats
- `POST /api/team-stats/`: Create new team stats
- `PUT /api/team-stats/{id}/`: Update team stats
- `DELETE /api/team-stats/{id}/`: Delete team stats

### Predictions

- `GET /api/predictions/`: List all predictions
- `GET /api/predictions/{id}/`: Get a specific prediction
- `POST /api/predictions/compare_players/`: Compare two players

## Filtering

Most endpoints support filtering. For example:

- `GET /api/teams/?conference=Western`: Get all teams in the Western conference
- `GET /api/players/?team=1&position=SF`: Get all small forwards on team with ID 1
- `GET /api/matches/?season=2023-24&is_playoff=true`: Get all playoff matches from the 2023-24 season

## Pagination

The API uses pagination with 20 items per page by default. You can navigate through pages using the `next` and `previous` links in the response.

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses include a message explaining what went wrong.
