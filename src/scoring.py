from src.app_tools.yaml_loader import load_yaml_file
from src.data_prep.all_team_data import get_all_team_data
from src.profiling.get_medals import get_all_medals
import pandas as pd
from src.data_prep.load_data import get_current_season_year, get_team_data
from src.data_prep.load_data_league import get_league_data
import json


def get_team_medals(team_id, bootstrap_data, current_gameweek, player_data):
    """
    Retrieve medals for a specific team based on its ID and related data.

    Parameters
    ----------
    team_id : int
        The unique identifier for the team.
    bootstrap_data : dict
        Bootstrap data containing season and gameweek information.
    current_gameweek : int
        The current gameweek in the season.
    player_data : pd.DataFrame or str
        Player data as a DataFrame or a string indicating if the season has not started.

    Returns
    -------
    team_name : str
        The name of the team.
    medals : pd.DataFrame
        A DataFrame with medal details for the team.
    """
    # Get player data
    current_season_year = get_current_season_year(bootstrap_data=bootstrap_data)

    # Load metadata
    file_path = "data/training_meta.json"
    with open(file_path, "r") as file:
        training_meta = json.load(file)
    current_gameweek = training_meta["training_data_gameweek"]

    # Load player data
    try:  # i.e. season has started
        file_path = f"data/vaastav-data/player_data_{current_season_year}.csv"
        player_data = pd.read_csv(file_path)
    except:
        player_data = "Season Not Started"

    lookup_table_numeric = pd.read_csv(
        "data/variable_lookup_tables/numeric_columns.csv"
    )
    lookup_table_categorical = pd.read_csv(
        "data/variable_lookup_tables/categorical_columns.csv"
    )

    team_name, team_data = get_all_team_data(
        team_id=team_id,
        bootstrap_data=bootstrap_data,
        current_gameweek=current_gameweek,
        player_data=player_data,
    )

    # Get null imputing values
    yaml_file_path = "conf/impute_nulls.yaml"
    impute_nulls = load_yaml_file(yaml_file_path)

    # Update team_data with impute_nulls values for None entries
    for key, value in team_data.items():
        if value is None and key in impute_nulls:
            team_data[key] = impute_nulls[key]

    # Get medal details
    yaml_file_path = "conf/medal_details/medal_details_numeric.yaml"
    medal_details_numeric = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_categorical.yaml"
    medal_details_categorical = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_binary.yaml"
    medal_details_binary = load_yaml_file(yaml_file_path)

    yaml_file_path = "conf/medal_details/medal_details_special.yaml"
    medal_details_special = load_yaml_file(yaml_file_path)

    medals = get_all_medals(
        medal_details_numeric=medal_details_numeric,
        lookup_table_numeric=lookup_table_numeric,
        medal_details_categorical=medal_details_categorical,
        lookup_table_categorical=lookup_table_categorical,
        medal_details_binary=medal_details_binary,
        medal_details_special=medal_details_special,
        team_data=team_data,
    )

    return team_name, medals


def get_leagues_competing_in(team_id, max_league_size=300):
    """
    Get leagues that a specific team is competing in, filtered by league size.

    Parameters
    ----------
    team_id : int
        The unique identifier for the team.
    max_league_size : int, optional
        The maximum size of the leagues to include. Default is 300.

    Returns
    -------
    classic_leagues : dict
        A dictionary where keys are league names and values are league IDs.
    """
    # Get leagues competing in
    team_data, team_history_data = get_team_data(team_id)

    classic_leagues = team_data["leagues"]["classic"]
    # Extract the list of dictionaries

    # Create the new dictionary with name as key and id as value
    classic_leagues = {
        team["name"]: team["id"]
        for team in classic_leagues
        if team.get("rank_count") is not None and team["rank_count"] < max_league_size
    }
    return classic_leagues


def get_league_medals(
    league_id, page_limit, bootstrap_data, current_gameweek, player_data
):
    """
    Retrieve medal information for all teams in a specified league.

    Parameters
    ----------
    league_id : int
        The unique identifier for the league.
    page_limit : int
        The maximum number of pages of league data to retrieve.
    bootstrap_data : dict
        Bootstrap data containing season and gameweek information.
    current_gameweek : int
        The current gameweek in the season.
    player_data : pd.DataFrame or str
        Player data as a DataFrame or a string indicating if the season has not started.

    Returns
    -------
    league_name : str
        The name of the league.
    league_medals : pd.DataFrame
        A DataFrame with medal details for each team in the league.
    """
    league_details, league_data = get_league_data(
        league_id=league_id, current_gameweek=current_gameweek, page_limit=page_limit
    )
    league_name = league_details["league"]["name"]

    columns = ["Manager", "Team", "Medal Name", "Medal"]
    league_medals = pd.DataFrame(columns=columns)

    for team in league_data:
        team_id = team["entry"]
        team_name, medals_stage = get_team_medals(
            team_id, bootstrap_data, current_gameweek, player_data
        )
        medals_stage["Manager"] = team["player_name"]
        medals_stage["Team"] = team["entry_name"]

        medals_stage = medals_stage[["Manager", "Team", "Medal Name", "Medal"]]

        league_medals = pd.concat([league_medals, medals_stage], ignore_index=True)

    # Define the order of the categories
    medal_order = pd.Categorical(
        league_medals["Medal"], categories=["Gold", "Silver", "Bronze"], ordered=True
    )

    # Assign the categorical data type to the 'medal' column
    league_medals["Medal"] = medal_order

    # Sort the DataFrame by the 'medal' column
    league_medals = league_medals.sort_values(by="Medal")

    return league_name, league_medals
