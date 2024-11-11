# Import necessary modules
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier


@st.cache_data()
def load_data():
    """This function returns the preprocessed data"""

    # Load the dataset into DataFrame.
    df = pd.read_csv('C:/Users/User/PycharmProjects/Python_Tutorial/cardio.csv')

    # Drop the id column
    df.drop('id', axis=1, inplace=True)

    df['age'] = np.floor_divide(df['age'], 365)

    # Split the dataset into features and target
    X = df.drop('cardio', axis=1)
    y = df['cardio']

    return df, X, y


@st.cache_data()
def train_model(X, y):
    # Set the best hyperparameters
    best_hyperparameters = {'max_depth': 10, 'min_samples_leaf': 1, 'n_estimators': 400}

    # Create the RandomForestClassifier model with the best hyperparameters
    model = RandomForestClassifier(random_state=42, **best_hyperparameters)

    # Fit the data on model
    model.fit(X, y)

    # Return the values
    return model


def predict(X, y, features):
    # Get model and model score
    rf_best = train_model(X, y)

    # Predict the value
    prediction = rf_best.predict(np.array(features).reshape(1, -1))

    return prediction
