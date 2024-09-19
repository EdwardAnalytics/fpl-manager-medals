import streamlit as st

from src.data_prep.load_data import (
    get_boostrap_data,
    get_current_season_year,
)
from src.scoring import get_league_medals, get_leagues_competing_in
import pandas as pd
from src.streamlit_components.get_medals import get_league_medal_scoring
from src.app_tools.yaml_loader import load_multiple_yaml_files_combined
from src.app_tools.json_loader import load_json_file
from src.app_tools.streamlit_csv_loader import load_csv_with_error_handling
from src.streamlit_components.page_configuration import (
    hide_streamlit_deploy_button,
    create_streamlit_header_with_logo,
)

# Get medal details
file_paths = [
    "conf/medal_details/medal_details_numeric.yaml",
    "conf/medal_details/medal_details_categorical.yaml",
    "conf/medal_details/medal_details_binary.yaml",
    "conf/medal_details/medal_details_special.yaml",
]
medals_dict = load_multiple_yaml_files_combined(file_paths)


# Pre processing
# Get boostrap data
bootstrap_data = get_boostrap_data()

# Get player data
current_season_year = get_current_season_year(bootstrap_data=bootstrap_data)

# Load metadata
file_path = "data/training_meta.json"
training_meta = load_json_file(file_path)

current_gameweek = training_meta["training_data_gameweek"]

# Load player data
file_path = f"data/vaastav-data/player_data_{current_season_year}.csv"
player_data = load_csv_with_error_handling(file_path)

# Page config
title = "FPL Manager Medals: League"
st.set_page_config(page_title=title, page_icon=":soccer:")


# Hide deploy button
hide_streamlit_deploy_button()


def main():
    try:
        st.title(title)
        if st.button(":twisted_rightwards_arrows: Switch to Team Medals"):
            st.switch_page("Team_Medals.py")

        # Add github link and logo
        create_streamlit_header_with_logo(
            github_url="https://github.com/EdwardAnalytics/fpl-manager-medals",
            logo_image_path="assets/pwt.png",
        )

        # Input number
        id = st.number_input(
            "Enter Team ID to find the Leagues you are in",
            step=1,
            format="%d",
            value=None,
            help="Team ID is located in the team points URL: `https://fantasy.premierleague.com/entry/XXXXXX/event/1`",
        )

        if id is None:
            # Fetch the leagues only after an ID is entered
            league_name = st.selectbox(
                "Select League", options=(("Enter Team ID First", ""))
            )

            if st.button("Get Medals :soccer:"):
                st.text("")

        if id is not None:
            # Fetch the leagues only after an ID is entered
            classic_leagues = get_leagues_competing_in(team_id=id, max_league_size=300)

            league_name = st.selectbox(
                "Select League", options=(tuple(classic_leagues.keys()))
            )

            # Button to trigger function execution
            if st.button("Get Medals :soccer:"):
                # Call your function with the input numbers

                with st.spinner(text="Getting medal data..."):
                    league_name, league_medals = get_league_medals(
                        league_id=classic_leagues[league_name],
                        page_limit=6,
                        bootstrap_data=bootstrap_data,
                        current_gameweek=current_gameweek,
                        player_data=player_data,
                    )

                st.header(f"{league_name} Medals", divider="grey")

                medal_list = list(league_medals["Medal Name"].unique())
                number_of_medals = len(medal_list)

                # Replace medal names
                league_medals["Medal"] = league_medals["Medal"].replace(
                    {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
                )
                st.text("")
                index = 0
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                get_league_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medal_list=medal_list,
                    league_medals=league_medals,
                    medals_dict=medals_dict,
                )

                st.markdown(
                    f"*Data up to Gameweek {training_meta['training_data_gameweek']}*"
                )

    except Exception as e:
        st.error(
            """:lion_face: Unable to get team data. Team ID is located in the team points URL: `https://fantasy.premierleague.com/entry/XXXXXX/event/1`"""
        )


if __name__ == "__main__":
    main()
