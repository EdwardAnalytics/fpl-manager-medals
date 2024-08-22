import requests


def get_league_data_season_started(league_id, page_limit):
    """
    Retrieves league standings data for a given league ID when the season has started.

    Parameters:
    ----------
    league_id : int
        The ID of the league for which standings data is to be fetched.

    Returns:
    ----------
    league_data : dict
        League data retrieved from the first URL.
    team_data : list
        Team data extracted from all fetched URLs.
    """
    urls = []
    page = 1
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
    urls.append(url)

    league_data = requests.get(url).json()
    all_results = [league_data]

    while league_data["standings"]["has_next"] == True:
        page += 1

        if page > page_limit:
            break

        url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
        league_data = requests.get(url).json()
        urls.append(url)
        all_results.append(league_data)

    team_data = []
    for item in all_results:
        if "standings" in item and "results" in item["standings"]:
            team_data.extend(item["standings"]["results"])

    return all_results[0], team_data


def get_league_data_season_not_started(league_id, page_limit):
    """
    Retrieves league new entries data for a given league ID when the season has not started.

    Parameters:
    ----------
    league_id : int
        The ID of the league for which new entries data is to be fetched.

    Returns:
    ----------
    league_data : dict
        League data retrieved from the first URL.
    team_data : list
        Team data extracted from all fetched URLs.
    """
    urls = []
    page = 1
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_new_entries={page}"
    urls.append(url)

    league_data = requests.get(url).json()
    all_results = [league_data]

    while league_data["new_entries"]["has_next"] == True:
        page += 1

        if page > page_limit:
            break

        url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_new_entries={page}"
        league_data = requests.get(url).json()
        urls.append(url)
        all_results.append(league_data)

    team_data = []
    for item in all_results:
        if "new_entries" in item and "results" in item["new_entries"]:
            team_data.extend(item["new_entries"]["results"])

    for team in team_data:
        team["player_name"] = (
            f"{team.pop('player_first_name')} {team.pop('player_last_name')}"
        )

    return all_results[0], team_data


def get_league_data(league_id, current_gameweek, page_limit):
    """
    Retrieves league data and team data for a given league ID.

    Parameters:
    ----------
    league_id : int
        The ID of the league for which data is to be fetched.

    Returns:
    ----------
    league_data : dict
        League data retrieved from the first URL.
    team_data : list
        Team data extracted from all fetched URLs.
    """

    if current_gameweek != "Season Not Started":
        return get_league_data_season_started(league_id, page_limit)
    else:
        return get_league_data_season_not_started(league_id, page_limit)
