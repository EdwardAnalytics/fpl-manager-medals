import pandas as pd
import inflect
from src.profiling.get_categorical_medals import team_medal_categorical


def get_medal_for_feature(value, gold_values):
    """
    Determine the medal (Gold or No Medal) based on the feature value and gold threshold.

    Parameters
    ----------
    value : any
        Value of the feature from the team data.
    gold_values : any
        Threshold value for awarding a gold medal.

    Returns
    -------
    medal : str
        'Gold' if the feature value matches the gold threshold, otherwise 'No Medal'.
    """
    if value == gold_values:
        return "Gold"
    return "No Medal"


def generate_overview_text(medal_details, percentage, rank_ascending, rank_descending):
    """
    Generate the overview text by replacing placeholders with actual values for percentage, rank_ascending, and rank_descending.

    Parameters
    ----------
    medal_details : dict
        Dictionary containing the medal details including the template for the overview text.
    percentage : float
        The percentage value to be inserted into the overview text.
    rank_ascending : int
        The ascending rank value to be inserted into the overview text.
    rank_descending : int
        The descending rank value to be inserted into the overview text.

    Returns
    -------
    overview : str
        The overview text with placeholders replaced by actual values.
    """
    p = inflect.engine()
    rank_ascending = p.ordinal(int(rank_ascending))
    rank_descending = p.ordinal(int(rank_descending))

    overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
    overview = overview.replace("<rank_ascending>", rank_ascending)
    overview = overview.replace("<rank_descending>", rank_descending)

    return overview


def process_binary_medal(
    medal_name, medal_details, team_data, lookup_table_categorical
):
    """
    Process a single binary medal, calculating its rank and generating a result row.

    Parameters
    ----------
    medal_name : str
        Name of the binary medal to process.
    medal_details : dict
        Dictionary with details of the binary medal.
    team_data : dict
        Dictionary containing the team's data for comparison.
    lookup_table_categorical : pd.DataFrame
        DataFrame containing lookup data for categorical features.

    Returns
    -------
    medal_entry : pd.DataFrame
        DataFrame containing a single row of processed medal information.
    """
    feature_name = medal_details["feature_name"]
    value = team_data[feature_name]

    # Retrieve percentage and ranks using team_medal_categorical
    percentage, rank_ascending, rank_descending = team_medal_categorical(
        lookup_table_categorical=lookup_table_categorical,
        feature_name=feature_name,
        value=value,
    )

    # Determine the medal type (Gold or No Medal)
    medal = get_medal_for_feature(value, medal_details["gold_values"])

    # Generate the overview text
    overview = generate_overview_text(
        medal_details, percentage, rank_ascending, rank_descending
    )

    # Create the result DataFrame entry
    medal_entry = pd.DataFrame(
        [
            {
                "Medal Name": medal_name,
                "Medal": medal,
                "Overview": overview,
                "image_path": medal_details["image_path"],
                "medal_background": medal_details["medal_background"],
            }
        ]
    )

    return medal_entry


def get_binary_medals(medal_details_binary, lookup_table_categorical, team_data):
    """
    Calculate medals for binary features based on thresholds and team data.

    Parameters
    ----------
    medal_details_binary : dict
        Dictionary with medal details for binary features including 'feature_name',
        'gold_values', 'text', 'image_path', and 'medal_background'.
    lookup_table_categorical : pd.DataFrame
        DataFrame with categorical lookup data.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    medals : pd.DataFrame
        DataFrame containing the results for all binary medals including columns for 'Medal Name',
        'Medal', 'Overview', 'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_binary.items():
        # Process each binary medal
        medal_entry = process_binary_medal(
            medal_name=medal_name,
            medal_details=medal_details,
            team_data=team_data,
            lookup_table_categorical=lookup_table_categorical,
        )
        # Append the medal entry to the medals DataFrame
        medals = pd.concat([medals, medal_entry], axis=0, ignore_index=True)

    return medals
