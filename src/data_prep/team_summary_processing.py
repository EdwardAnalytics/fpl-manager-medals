import pandas as pd
import numpy as np

from src.data_prep.load_data import get_team_data
from src.data_prep.team_summary.kit import get_kit_information
from src.data_prep.team_summary.yoyo_rising_score import calculate_yoyo_rising_scores


def process_team_history(team_history_data):
    if len(team_history_data["past"]) == 0:
        min_rank_history = None
        max_rank_history = None
        max_total_points_history = None
        earliest_season_year_history = None
        career_break_history = None
        seasons_played_in = None
        yoyo_score = None
        rising_score = None
    else:
        # Convert to DataFrame and extract the start year as an integer
        team_history_data_df = pd.DataFrame(team_history_data["past"])
        team_history_data_df["start_year"] = team_history_data_df["season_name"].apply(
            lambda x: int(x.split("/")[0])
        )

        # Calculate the differences between consecutive years
        team_history_data_df["year_diff"] = team_history_data_df["start_year"].diff()

        # Get metrics
        min_rank_history = team_history_data_df["rank"].min()
        max_rank_history = team_history_data_df["rank"].max()
        max_total_points_history = team_history_data_df["total_points"].max()
        earliest_season_year_history = team_history_data_df["start_year"].min()
        career_break_history = team_history_data_df["year_diff"].max()
        seasons_played_in = len(team_history_data_df["season_name"])

        if seasons_played_in > 1:
            yoyo_score, rising_score = calculate_yoyo_rising_scores(team_history_data)
        else:
            yoyo_score = None
            rising_score = None

    # Handle NaN by replacing it with None
    variables = [career_break_history, yoyo_score, rising_score]

    # Apply the logic using map and list comprehension
    variables = [None if pd.isna(var) else var for var in variables]

    # Create summary dictionary
    team_summary_history_data = {
        "min_rank_history": min_rank_history,
        "max_rank_history": max_rank_history,
        "max_total_points_history": max_total_points_history,
        "earliest_season_year_history": earliest_season_year_history,
        "career_break_history": career_break_history,
        "seasons_played_in": seasons_played_in,
        "yoyo_score": yoyo_score,
        "rising_score": rising_score,
    }

    return team_summary_history_data


def aggregate_team_data(team_data, kit_summary_data, team_summary_history_data):
    # Create the team_summary_data dictionary
    team_summary_data = {
        "id": team_data["id"],
        "name": team_data["name"],
        "player_region_iso_code_long": team_data["player_region_name"],
        "years_active": team_data["years_active"],
        "joined_time": team_data["joined_time"][:10],
        "classic_leagues_competed_in": len(team_data["leagues"]["classic"]),
        "h2h_leagues_competed_in": len(team_data["leagues"]["h2h"]),
        "last_deadline_bank": team_data["last_deadline_bank"],
        "last_deadline_value": team_data["last_deadline_value"],
        "last_deadline_total_transfers": team_data["last_deadline_total_transfers"],
        "summary_overall_points": team_data["summary_overall_points"],
        "summary_overall_rank": team_data["summary_overall_rank"],
        "name_change_blocked": team_data["name_change_blocked"],
        "leagues_admin": sum(
            1
            for league in team_data["leagues"]["classic"]
            if league.get("entry_can_admin", False)
        ),
        "kit": kit_summary_data["kit"],
        "kit_shirt_type": kit_summary_data["kit_shirt_type"],
        "kit_shirt_logo": kit_summary_data["kit_shirt_logo"],
        "kit_socks_type": kit_summary_data["kit_socks_type"],
        "kit_shorts": kit_summary_data["kit_shorts"],
        "kit_full": kit_summary_data["kit_full"],
        "min_rank_history": team_summary_history_data["min_rank_history"],
        "max_rank_history": team_summary_history_data["max_rank_history"],
        "max_total_points_history": team_summary_history_data[
            "max_total_points_history"
        ],
        "earliest_season_year_history": team_summary_history_data[
            "earliest_season_year_history"
        ],
        "career_break_history": team_summary_history_data["career_break_history"],
        "seasons_played_in": team_summary_history_data["seasons_played_in"],
        "yoyo_score": team_summary_history_data["yoyo_score"],
        "rising_score": team_summary_history_data["rising_score"],
    }

    return team_summary_data


def get_team_summary(team_data, team_history_data):
    # Get kit information
    kit_summary_data = get_kit_information(team_data)

    # Process team history
    team_summary_history_data = process_team_history(
        team_history_data=team_history_data
    )

    # Create team summary
    team_summary_data = aggregate_team_data(
        team_data,
        kit_summary_data=kit_summary_data,
        team_summary_history_data=team_summary_history_data,
    )

    return team_summary_data
