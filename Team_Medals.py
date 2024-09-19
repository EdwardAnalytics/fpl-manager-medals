import streamlit as st

from src.data_prep.load_data import (
    get_boostrap_data,
    get_current_season_year,
)
from src.streamlit_components.get_medals import create_medal_scoring
from src.scoring import get_team_medals
import pandas as pd
from src.app_tools.json_loader import load_json_file
from src.app_tools.streamlit_csv_loader import load_csv_with_error_handling
from src.streamlit_components.page_configuration import (
    hide_streamlit_deploy_button,
    create_streamlit_header_with_logo,
)

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
title = "FPL Manager Medals: Team"
st.set_page_config(page_title=title, page_icon=":soccer:")


# Hide deploy button
hide_streamlit_deploy_button()


def main():
    try:
        st.title(title)
        if st.button(":twisted_rightwards_arrows: Switch to League Medals"):
            st.switch_page("pages/1_League_Medals.py")

        # Add github link and logo
        create_streamlit_header_with_logo(
            github_url="https://github.com/EdwardAnalytics/fpl-manager-medals",
            logo_image_path="assets/pwt.png",
        )

        # Input number
        id = st.number_input(
            "Enter Team",
            step=1,
            format="%d",
            value=None,
            help="Team ID is located in the team points URL: `https://fantasy.premierleague.com/entry/XXXXXX/event/1`",
        )
        # Button to trigger function execution
        if st.button(label="Get Medals :soccer:"):
            # Call your function with the input numbers

            with st.spinner(text="Getting medal data..."):
                team_name, medals_df = get_team_medals(
                    team_id=id,
                    bootstrap_data=bootstrap_data,
                    current_gameweek=current_gameweek,
                    player_data=player_data,
                )
            # st.markdown(f"*Data up to Gameweek {training_meta['training_data_gameweek']}*")

            st.header(f"{team_name} Medals", divider="grey")

            # Get number of medals
            number_of_medals = len(medals_df)
            # Replace medal names
            medals_df["Medal"] = medals_df["Medal"].replace(
                {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
            )

            # Convert to lists of dictionaries
            medals_dict = medals_df.T.to_dict()
            medals_dict = list(medals_dict.values())

            all_medals, summary = st.tabs(["All Medals", "Overview"])
            with summary:
                st.dataframe(medals_df[["Medal Name", "Medal"]], hide_index=True)

            with all_medals:
                index = 0
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
                    medals_dict=medals_dict,
                )

                index += 1
                create_medal_scoring(
                    index=index,
                    number_of_medals=number_of_medals,
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
