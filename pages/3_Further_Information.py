import streamlit as st

st.set_page_config(
    page_title="Further Information",
    page_icon=":soccer:",
)

st.title("Further Information")
st.subheader("Other Dashboards", divider="grey")
st.markdown(
    """
    * [FPL League History](https://fpl-league-history.streamlit.app/)  
      *Get the past winners and records for individual mini-leagues.*
    
    * [Complementing Fixtures](https://fpltool.farragher.uk/)  
      *Identify which teams have 'complementing fixtures'. This means when one has a difficult opponent, the other has an easy opponent. If you have one player from each of two teams with complementing fixtures, you can rotate each week, starting whoever has the easier fixture.*
    """
)
st.text("")
st.subheader("Methodology (Manager Medals)", divider="grey")
st.markdown("""
    1. **Sample Selection:** A random sample of 100 Fantasy Premier League (FPL) managers is selected for analysis.
    
    2. **Data Collection:** Data is collected from the FPL API to capture each manager's past season history, current season statistics, and current team selection.
    
    3. **Player Details:** Detailed player information for the current season is appended using the [Fantasy-Premier-League repository](https://github.com/vaastav/Fantasy-Premier-League).
    
    4. **Variable Analysis:** 
        - **Numeric Variables:** For each numeric variable, the percentage of values above and below each observed value in the sample is calculated.
        - **Categorical Variables:** For categorical variables, the proportion of managers with each value is calculated, and categories are ranked by the volume of players.
    
    5. **Threshold Estimation:** Numeric values are estimated at specific clean thresholds (5%, 10%, 15%, etc.) using [linear interpolation](https://en.wikipedia.org/wiki/Linear_interpolation).
    
    6. **Comparison:** Inputted team IDs are compared against this reference data to determine their index.
    
    7. **Medal Allocation:** Teams are evaluated against predefined thresholds for gold, silver, and bronze medals. Teams meeting the threshold are awarded the corresponding medal.

    *For further details, please refer to the repository [here](https://github.com/edward-farragher/fpl-manager-medals).*
    """)
