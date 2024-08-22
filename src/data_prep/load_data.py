import requests
import concurrent.futures
import pandas as pd


def fetch_url(url):
    """
    Fetches data from a given URL using the requests library.

    Parameters:
    ----------
    url : str
        The URL to fetch data from.

    Returns:
    ----------
    data : dict or None
        The JSON data retrieved from the URL if the request is successful, otherwise None.
    """
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data
    else:
        return None


# Function to fetch URLs concurrently
def fetch_urls_concurrently(urls):
    """
    Fetches multiple URLs concurrently using ThreadPoolExecutor.

    Parameters:
    ----------
    urls : list
        A list of URLs to fetch.

    Returns:
    ----------
    results : list:
        A list containing the fetched results from the URLs.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(fetch_url, url) for url in urls]

        # Retrieve results as they become available
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results


def get_boostrap_data():
    """
    This gets the bootstrap static data from the Fantasy Premier League API.

    Returns
    -------
    dict
        A dictionary containing the bootstrap static data from the Fantasy Premier League API. This data typically includes information about teams, players, and other game-related metadata.

    Notes
    -----
    The data is fetched from the URL:
    'https://fantasy.premierleague.com/api/bootstrap-static/'
    """
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    bootstrap_data = fetch_url(url)
    return bootstrap_data


def get_team_data(team_id):
    """
    This gets the team data for a given team ID from the Fantasy Premier League API.

    Parameters
    ----------
    team_id : int
        The unique identifier for the team whose data is to be fetched.

    Returns
    -------
    dict
        A dictionary containing the team data from the Fantasy Premier League API. This data includes details about the team's players, performance, and other related information.

    Notes
    -----
    The data is fetched from the URL:
    'https://fantasy.premierleague.com/api/entry/{team_id}/', where `{team_id}` is replaced with the provided team ID.
    """
    team_url = f"https://fantasy.premierleague.com/api/entry/{team_id}/"
    team_data = fetch_url(team_url)

    team_history_url = f"https://fantasy.premierleague.com/api/entry/{team_id}/history/"
    team_history_data = fetch_url(team_history_url)

    return team_data, team_history_data


def get_team_gw_data(team_id, team_history_data, current_gameweek):
    if current_gameweek == "Season Not Started":
        return "Season Not Started"
    else:
        current_gameweek = int(current_gameweek)

    bboost_gw = get_bboost_gw(team_history_data)
    team_gw_picks = pd.DataFrame(
        columns=[
            "element",
            "position",
            "multiplier",
            "is_captain",
            "is_vice_captain",
            "GW",
            "bboost",
        ]
    )
    for gw in range(1, current_gameweek + 1):
        team_event_url = (
            f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{gw}/picks/"
        )
        team_gw_data_stage = fetch_url(team_event_url)

        if team_gw_data_stage is not None:
            team_gw_picks_stage = team_gw_data_stage["picks"]

            team_gw_picks_stage_df = pd.DataFrame(team_gw_data_stage["picks"])

            team_gw_picks_stage_df["GW"] = gw

            if gw == bboost_gw:
                team_gw_picks_stage_df["bboost"] = 1

            else:
                team_gw_picks_stage_df["bboost"] = 0

            team_gw_picks = pd.concat(
                [team_gw_picks, team_gw_picks_stage_df], ignore_index=True
            )

        else:
            continue
    return team_gw_picks


def get_favourite_team(bootstrap_data, team_data):
    try:
        team_ids = pd.DataFrame(bootstrap_data["teams"])[["id", "name"]]
        favourite_team = team_ids[team_ids["id"] == team_data["favourite_team"]][
            "name"
        ].iloc[0]
    except:
        favourite_team = "Not Specified"
    return favourite_team


def get_bboost_gw(team_history_data):
    chips = team_history_data["chips"]
    if chips:  # Check if data is not None or empty
        for item in chips:
            if item["name"] == "bboost":
                return item["event"]
    return None


def get_current_season_year(bootstrap_data):
    year_start = bootstrap_data["events"][0]["deadline_time"][0:4]
    current_season_year = f"{year_start}-{str(int(year_start) + 1)[2:4]}"
    return current_season_year


def get_player_data(current_season_year):
    try:
        vaastav_url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{current_season_year}/gws/merged_gw.csv"

        # Read the CSV file into a pandas DataFrame
        player_data = pd.read_csv(vaastav_url)

        # Get latest GW in data
        current_gameweek = max(player_data["GW"])

    except:
        player_data = "Season Not Started"
        current_gameweek = "Season Not Started"

    return player_data, current_gameweek
