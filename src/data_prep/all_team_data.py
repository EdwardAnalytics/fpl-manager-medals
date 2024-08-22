from src.data_prep.team_summary_processing import get_team_summary
from src.data_prep.load_data import get_team_data
from src.app_tools.yaml_loader import load_yaml_file
from src.data_prep.load_data import (
    get_team_gw_data,
    get_favourite_team,
)
from src.data_prep.team_gameweek_processing import (
    get_player_gameweek_totals,
    get_season_gameweek_overview,
)

# Get config
yaml_file_path = "conf/rival_teams.yaml"
rival_teams = load_yaml_file(yaml_file_path)


def get_all_team_data(team_id, bootstrap_data, current_gameweek, player_data):
    # Load all team data
    team_data, team_history_data = get_team_data(team_id=team_id)
    team_name = team_data["name"]
    favourite_team = get_favourite_team(
        bootstrap_data=bootstrap_data, team_data=team_data
    )
    team_gw_picks = get_team_gw_data(
        team_id=team_id,
        team_history_data=team_history_data,
        current_gameweek=current_gameweek,
    )

    # Get team summary
    team_summary_data = get_team_summary(
        team_data=team_data, team_history_data=team_history_data
    )

    try:
        # Get gameweek player data
        player_gameweek_totals = get_player_gameweek_totals(
            player_data=player_data,
            team_gw_picks=team_gw_picks,
            favourite_team=favourite_team,
            rival_teams=rival_teams,
        )

        # Get gameweek summary data
        current_season_overview_output = get_season_gameweek_overview(
            team_history_data=team_history_data, current_gameweek=current_gameweek
        )
    except:  # team has not appeared in previous gameweeks
        player_gameweek_totals = {
            "assists": 0,
            "bonus": 0,
            "bps": 0,
            "clean_sheets": 0,
            "goals_conceded": 0,
            "goals_scored": 0,
            "own_goals": 0,
            "penalties_missed": 0,
            "penalties_saved": 0,
            "red_cards": 0,
            "yellow_cards": 0,
            "saves": 0,
            "rival_team_player": 0,
            "total_players_starters": 0,
            "total_players_all": 0,
            "rival_team_player_categorical": "No historical GW Data",
        }
        current_season_overview_output = {
            "points_on_bench_total": 0,
            "event_transfers_total": 0,
            "event_transfers_cost_total": 0,
            "bank_mean": 0,
            "bank_latest": 0,
            "value_latest": 0,
            "total_points_latest": 0,
            "points_on_bench_percentage": 0,
        }

    # Combine data
    all_team_data = {
        **team_summary_data,
        **player_gameweek_totals,
        **current_season_overview_output,
    }

    all_team_data["favourite_team"] = favourite_team
    print(all_team_data)

    return team_name, all_team_data
