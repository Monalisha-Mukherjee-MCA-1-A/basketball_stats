"""
Sample script to train and save a machine learning model.
This is for demonstration purposes only.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Sample data for player performance prediction
def generate_player_performance_data():
    """Generate sample data for player performance prediction."""
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    player_ids = np.random.randint(1, 101, n_samples)
    positions = np.random.choice(['PG', 'SG', 'SF', 'PF', 'C'], n_samples)
    heights = np.random.normal(2.0, 0.1, n_samples)  # in meters
    weights = np.random.normal(90, 10, n_samples)    # in kg
    ages = np.random.randint(19, 40, n_samples)
    avg_points = np.random.normal(15, 5, n_samples)
    avg_assists = np.random.normal(3, 2, n_samples)
    avg_rebounds = np.random.normal(5, 3, n_samples)
    avg_steals = np.random.normal(1, 0.5, n_samples)
    avg_blocks = np.random.normal(0.5, 0.3, n_samples)
    avg_minutes = np.random.normal(25, 5, n_samples)
    
    # Target variables
    points = avg_points + np.random.normal(0, 3, n_samples)
    assists = avg_assists + np.random.normal(0, 1, n_samples)
    rebounds = avg_rebounds + np.random.normal(0, 2, n_samples)
    steals = avg_steals + np.random.normal(0, 0.3, n_samples)
    blocks = avg_blocks + np.random.normal(0, 0.2, n_samples)
    
    # Create DataFrame
    data = pd.DataFrame({
        'player_id': player_ids,
        'position': positions,
        'height': heights,
        'weight': weights,
        'age': ages,
        'avg_points': avg_points,
        'avg_assists': avg_assists,
        'avg_rebounds': avg_rebounds,
        'avg_steals': avg_steals,
        'avg_blocks': avg_blocks,
        'avg_minutes': avg_minutes,
        'points': points,
        'assists': assists,
        'rebounds': rebounds,
        'steals': steals,
        'blocks': blocks
    })
    
    # Convert categorical variables to one-hot encoding
    data = pd.get_dummies(data, columns=['position'])
    
    return data

# Sample data for match outcome prediction
def generate_match_outcome_data():
    """Generate sample data for match outcome prediction."""
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    home_team_ids = np.random.randint(1, 31, n_samples)
    away_team_ids = np.random.randint(1, 31, n_samples)
    home_avg_points = np.random.normal(105, 5, n_samples)
    home_avg_rebounds = np.random.normal(45, 3, n_samples)
    home_avg_assists = np.random.normal(25, 2, n_samples)
    home_avg_steals = np.random.normal(8, 1, n_samples)
    home_avg_blocks = np.random.normal(5, 1, n_samples)
    away_avg_points = np.random.normal(102, 5, n_samples)
    away_avg_rebounds = np.random.normal(43, 3, n_samples)
    away_avg_assists = np.random.normal(24, 2, n_samples)
    away_avg_steals = np.random.normal(7, 1, n_samples)
    away_avg_blocks = np.random.normal(4, 1, n_samples)
    
    # Target variable (1 for home win, 0 for away win)
    # Home team has a slight advantage
    home_win_prob = 0.55 + 0.01 * (home_avg_points - away_avg_points)
    home_win = np.random.binomial(1, home_win_prob, n_samples)
    
    # Create DataFrame
    data = pd.DataFrame({
        'home_team_id': home_team_ids,
        'away_team_id': away_team_ids,
        'home_avg_points': home_avg_points,
        'home_avg_rebounds': home_avg_rebounds,
        'home_avg_assists': home_avg_assists,
        'home_avg_steals': home_avg_steals,
        'home_avg_blocks': home_avg_blocks,
        'away_avg_points': away_avg_points,
        'away_avg_rebounds': away_avg_rebounds,
        'away_avg_assists': away_avg_assists,
        'away_avg_steals': away_avg_steals,
        'away_avg_blocks': away_avg_blocks,
        'home_win': home_win
    })
    
    return data

# Train and save player performance prediction model
def train_player_performance_model():
    """Train and save a model for player performance prediction."""
    data = generate_player_performance_data()
    
    # Split features and target
    X = data.drop(['points', 'assists', 'rebounds', 'steals', 'blocks'], axis=1)
    y = data[['points', 'assists', 'rebounds', 'steals', 'blocks']]
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Player Performance Model MSE: {mse}")
    
    # Save model
    with open('models/player_performance_model_v1.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Player performance model saved to models/player_performance_model_v1.pkl")

# Train and save match outcome prediction model
def train_match_outcome_model():
    """Train and save a model for match outcome prediction."""
    data = generate_match_outcome_data()
    
    # Split features and target
    X = data.drop('home_win', axis=1)
    y = data['home_win']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Match Outcome Model Accuracy: {accuracy}")
    
    # Save model
    with open('models/match_outcome_model_v1.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Match outcome model saved to models/match_outcome_model_v1.pkl")

if __name__ == "__main__":
    train_player_performance_model()
    train_match_outcome_model()
