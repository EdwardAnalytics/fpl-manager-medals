import streamlit as st
import base64

from src.data_prep.load_data import (
    get_boostrap_data,
    get_current_season_year,
)
import json
from src.scoring import get_league_medals, get_leagues_competing_in
import pandas as pd
from src.app_tools.yaml_loader import load_yaml_file

# Get medal details
yaml_file_path = "conf/medal_details/medal_details_numeric.yaml"
medal_details_numeric = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_categorical.yaml"
medal_details_categorical = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_binary.yaml"
medal_details_binary = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_special.yaml"
medal_details_special = load_yaml_file(yaml_file_path)

# Combine medals
medals_dict = {
    **medal_details_numeric,
    **medal_details_categorical,
    **medal_details_binary,
    **medal_details_special,
}


# Get gameweek scored
file_path = "data/training_meta.json"
with open(file_path, "r") as file:
    training_meta = json.load(file)

# Pre processing
# Get boostrap data
bootstrap_data = get_boostrap_data()

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

# Page config
st.set_page_config(
    page_title="FPL Manager Medals: League",
    page_icon=":soccer:",
)


# Hide deploy button
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    try:
        st.title("FPL Manager Medals: League")

        # Add github link and logo
        LOGO_IMAGE = "assets//pwt.png"

        st.markdown(
            """
            <style>
            .container {
                display: flex;
            }
            .logo-text {
                font-weight: 0 !important;
                font-size: 15px !important;
                padding-top: 0px !important;
                margin-left: 0px;
                font-style: italic; 
            }
            .logo-img {
                float:right;
                width: 28px;
                height: 28px;
                margin-right: 8px; 
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="container">
                <img class="logo-img" src="data:assets//pwt.png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
                <p class="logo-text"><a href="https://github.com/edward-farragher/fpl-manager-segmentation">GitHub Repo</a></p>
            </div>
            """,
            unsafe_allow_html=True,
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
                # st.markdown(f"*Data up to Gameweek {training_meta['training_data_gameweek']}*")

                st.header(f"{league_name} Medals", divider="grey")

                medal_list = list(league_medals["Medal Name"].unique())
                number_of_medals = len(medal_list)

                # Replace medal names
                league_medals["Medal"] = league_medals["Medal"].replace(
                    {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
                )
                st.text("")
                index = 0
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")
                index += 1
                if index < number_of_medals:
                    medal_name = medal_list[index]
                    st.subheader(medal_name)
                    league_medals_filtered = league_medals[
                        league_medals["Medal Name"] == medal_name
                    ]
                    st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
                    st.dataframe(
                        league_medals_filtered[["Manager", "Team", "Medal"]],
                        hide_index=True,
                    )
                    st.text("")

    except Exception as e:
        st.error(
            """:lion_face: Unable to get team data. Team ID is located in the team points URL: `https://fantasy.premierleague.com/entry/XXXXXX/event/1`"""
        )


if __name__ == "__main__":
    main()
