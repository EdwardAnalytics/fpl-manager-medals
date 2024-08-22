import pandas as pd


def get_player_gameweek_totals(player_data, team_gw_picks, favourite_team, rival_teams):
    # Append player gameweek data
    player_data = pd.merge(
        team_gw_picks,
        player_data,
        on=["element", "GW"],
        how="inner",
        suffixes=("_team", "_player"),
    )

    # Get rival teams
    if favourite_team != "Not Specified":
        rivals = rival_teams[favourite_team]
    else:
        rivals = None

    # Create 'rival_team_player' column and initialize to 0
    player_data["rival_team_player"] = 0

    if rivals is not None:
        # Set 'rival_team_player' to 1 where 'player_data' is in the list of rivals
        player_data.loc[player_data["team"].isin(rivals), "rival_team_player"] = 1

    # Filter DataFrame where position_team >= 11
    player_data_starters = player_data[
        (player_data["position_team"] <= 11) | (player_data["bboost"] == 1)
    ]

    # Sum the specified columns
    columns_to_sum_starters = [
        "assists",
        "bonus",
        "bps",
        "clean_sheets",
        "goals_conceded",
        "goals_scored",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "red_cards",
        "yellow_cards",
        "saves",
    ]

    columns_to_sum_all = ["rival_team_player"]

    player_starter_totals = (
        player_data_starters[columns_to_sum_starters].sum().to_dict()
    )

    players_all_totals = player_data[columns_to_sum_all].sum().to_dict()

    player_gameweek_totals = {
        **player_starter_totals,
        **players_all_totals,
    }

    player_gameweek_totals["total_players_starters"] = len(player_data_starters)
    player_gameweek_totals["total_players_all"] = len(player_data)

    if rivals is not None and player_gameweek_totals["rival_team_player"] > 0:
        player_gameweek_totals["rival_team_player_categorical"] = "Picked Rivals"
    elif rivals is not None and player_gameweek_totals["rival_team_player"] == 0:
        player_gameweek_totals["rival_team_player_categorical"] = "Not Picked Rivals"
    else:
        player_gameweek_totals["rival_team_player_categorical"] = "No Rival Team"

    return player_gameweek_totals


def get_season_gameweek_overview(team_history_data, current_gameweek):
    current_season_overview = pd.DataFrame(team_history_data["current"])
    current_season_overview = current_season_overview[
        current_season_overview["event"] <= current_gameweek
    ]

    columns_to_sum_all_gws = [
        "points_on_bench",
        "event_transfers",
        "event_transfers_cost",
    ]

    columns_to_mean_all_gws = ["bank"]

    columns_lates_gw = ["bank", "value", "total_points"]

    season_totals = current_season_overview[columns_to_sum_all_gws].sum().to_dict()

    # Rename the keys by adding "_total" to each key
    season_totals = {f"{key}_total": value for key, value in season_totals.items()}

    season_means = current_season_overview[columns_to_mean_all_gws].mean().to_dict()

    # Rename the keys by adding "_mean" to each key
    season_means = {f"{key}_mean": value for key, value in season_means.items()}

    # Get latest gameweek
    max_event_row = current_season_overview[
        current_season_overview["event"] == current_season_overview["event"].max()
    ]

    # Get values
    season_latest = max_event_row[columns_lates_gw].iloc[0].to_dict()

    # Rename the keys by adding "_latest" to each key
    season_latest = {f"{key}_latest": value for key, value in season_latest.items()}

    current_season_overview_output = {
        **season_totals,
        **season_means,
        **season_latest,
    }

    # Calculate percentage of points on bench
    current_season_overview_output["points_on_bench_percentage"] = int(
        round(
            100
            * current_season_overview_output["points_on_bench_total"]
            / current_season_overview_output["total_points_latest"],
            0,
        )
    )

    # Round bank average
    current_season_overview_output["bank_mean"] = round(
        current_season_overview_output["bank_mean"], 1
    )

    return current_season_overview_output
