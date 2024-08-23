import streamlit as st
import base64

from src.data_prep.load_data import (
    get_boostrap_data,
    get_current_season_year,
)
import json
from src.scoring import get_team_medals, get_league_medals
import pandas as pd

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
    page_title="FPL Manager Medals",
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
    st.title(
        "FPL Manager Medals",
        help="Note: The sidebar is hidden on mobile devices. Tap the > icon at the top left to access it. This includes getting medals for leagues and further information.",
    )

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
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])

            index += 1
            if index < number_of_medals:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(
                            f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                        )
                        st.markdown(
                            f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.image(image=medals_dict[index]["image_path"])


if __name__ == "__main__":
    main()
