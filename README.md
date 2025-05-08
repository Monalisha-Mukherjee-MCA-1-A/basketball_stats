# Basketball Statistics API

A Django REST Framework API for basketball statistics and predictions.

## Features

- RESTful API endpoints for basketball statistics
- Authentication and authorization mechanisms
- Efficient database models for storing basketball data
- ML model integration for predictions
- Comprehensive API documentation with Swagger/OpenAPI

## Database Models

- Teams: Information about basketball teams
- Players: Information about basketball players
- Matches: Information about basketball matches
- PlayerStats: Statistics for players in specific matches
- TeamStats: Statistics for teams in specific matches
- ML Models: Machine learning models for predictions
- Predictions: Predictions made by ML models

## API Endpoints

- `/api/teams/`: CRUD operations for teams
- `/api/players/`: CRUD operations for players
- `/api/matches/`: CRUD operations for matches
- `/api/player-stats/`: CRUD operations for player statistics
- `/api/team-stats/`: CRUD operations for team statistics
- `/api/predictions/`: View predictions

## ML Model Integration

- Player performance prediction
- Match outcome prediction
- Player comparison

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Running the Application

### Running the Backend (Django Server)

```
# Activate the virtual environment
.\venv\Scripts\activate

# Start the Django server
python manage.py runserver
```

The backend server will be available at http://127.0.0.1:8000/

### Running the Frontend

```
# Navigate to the frontend directory
cd frontend

# Start a simple HTTP server
python -m http.server 8080
```

The frontend will be available at http://127.0.0.1:8080/

## API Documentation

API documentation is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Authentication

The API uses token-based authentication. To get a token:

1. Create a user account
2. Make a POST request to `/api-token-auth/` with your username and password
3. Use the token in the Authorization header: `Authorization: Token <your-token>`
