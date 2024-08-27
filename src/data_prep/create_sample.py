from src.data_prep.load_data import get_boostrap_data
from src.app_tools.yaml_loader import load_yaml_file
from src.data_prep.all_team_data import get_all_team_data
import pandas as pd
import random
import time

# Get config
yaml_file_path = "conf/parameters.yaml"
config = load_yaml_file(yaml_file_path)


training_sample_size = config["training_sample_size"]
random_seed = config["random_seed"]


def get_sample_ids(training_sample_size, random_seed):
    """
    Generates a random sample of team IDs for training based on the total number of players.

    Parameters
    ----------
    training_sample_size : int
        The number of team IDs to sample.
    random_seed : int
        The seed for the random number generator to ensure reproducibility.

    Returns
    -------
    sample_ids : list of int
        A list containing randomly sampled team IDs.
    """
    bootstrap_data = get_boostrap_data()
    total_players = bootstrap_data["total_players"]
    random.seed(random_seed)
    sample_ids = random.sample(range(1, total_players + 1), training_sample_size)

    return sample_ids


def get_all_data_sample(bootstrap_data, current_gameweek, player_data):
    """
    Retrieves data for a random sample of teams based on the provided bootstrap data, current gameweek, and player data.

    Parameters
    ----------
    bootstrap_data : dict
        A dictionary containing the bootstrap static data from the Fantasy Premier League API.
    current_gameweek : int
        The current gameweek number.
    player_data : pd.DataFrame
        A DataFrame containing player data for the current season.

    Returns
    -------
    all_data : list of dict
        A list containing data for each sampled team.
    """
    # Get random sample of ids
    sample_ids = get_sample_ids(
        training_sample_size=training_sample_size, random_seed=random_seed
    )

    # Get data for each sample
    all_data = []
    counter = 0
    for team_id in sample_ids:
        try:
            team_name, team_data = get_all_team_data(
                team_id=team_id,
                bootstrap_data=bootstrap_data,
                current_gameweek=current_gameweek,
                player_data=player_data,
            )
            all_data.append(team_data)
            counter += 1
            print(f"Log: Team {counter} completed")
            # Add a 0.2-second sleep every 50 iterations
            if counter % 50 == 0:
                time.sleep(0.2)
        except TypeError as e:
            print(f"Error processing team {team_id}: {e}")
            continue  # Skip to the next iteration if an error occurs

    return all_data
