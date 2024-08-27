import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_yoyo_rising_scores(team_history_data):
    """
    Calculates the Yo-Yo score and Rising score based on a team's historical performance.

    The Yo-Yo score is a measure of the variability in the team's ranks over time, while
    the Rising score indicates the trend of the team's performance over the years. A negative
    slope in the linear regression (Rising score) indicates an improvement in rank over time.

    Parameters
    ----------
    team_history_data : dict
        A dictionary containing the team's historical performance data, with key 'past' holding
        a list of dictionaries where each dictionary corresponds to a season's data.

    Returns
    -------
    yoyo_score : float
        The Yo-Yo score, representing the average absolute difference in rank positions between consecutive seasons.
    rising_score : float
        The Rising score, representing the slope of the linear regression line fitted to the ranks over time.
        A negative value indicates improvement, while a positive value indicates a decline in performance.
    """
    past_data = team_history_data["past"]
    past_data_df = pd.DataFrame(past_data)
    past_data_df["year"] = past_data_df["season_name"].apply(
        lambda x: int(x.split("/")[0])
    )

    # Sort by year
    past_data_df = past_data_df.sort_values("year")

    positions = past_data_df["rank"].values
    years = past_data_df["year"].values

    seasons_played = len(years)

    # Reshape for sklearn
    positions_reshaped = positions.reshape(-1, 1)
    years_reshaped = years.reshape(-1, 1)

    yoyo_score = np.sum(np.abs(np.diff(positions))) / seasons_played

    model = LinearRegression()
    model.fit(years_reshaped, positions_reshaped)
    slope = model.coef_[0]

    rising_score = -slope[0]  # Negative slope indicates improvement

    # Round numbers
    yoyo_score = round(yoyo_score, 3)
    rising_score = round(rising_score, 3)

    return yoyo_score, rising_score
