import pandas as pd
import inflect


def add_new_row_if_missing(filtered_df, lookup_table_categorical, feature_name, value):
    """
    Add a new row to the filtered DataFrame if the feature value did not appear in the training data.

    Parameters
    ----------
    filtered_df : pd.DataFrame
        The filtered DataFrame, which might be empty if the value is missing.
    lookup_table_categorical : pd.DataFrame
        The original lookup table to check for missing values.
    feature_name : str
        The feature name for which the row is being added.
    value : str
        The value that was not found in the lookup table.

    Returns
    -------
    filtered_df : pd.DataFrame
        The DataFrame with the new row added if the feature value was missing.
    """
    if len(filtered_df) == 0:
        # Get max rank ascending for the feature
        rank_ascending_max = lookup_table_categorical[
            lookup_table_categorical["column_name"] == feature_name
        ]["rank_ascending"].max()

        # Create a new row with default values
        new_row = pd.DataFrame(
            {
                "column_name": [feature_name],
                "value": str(value),
                "percentage_share": [0.01],
                "rank_ascending": [rank_ascending_max],
                "rank_descending": [1.0],
            }
        )
        filtered_df = pd.concat([filtered_df, new_row], ignore_index=True)

    return filtered_df


def extract_rank_and_percentage(filtered_df):
    """
    Extract percentage share, rank ascending, and rank descending from the filtered DataFrame.

    Parameters
    ----------
    filtered_df : pd.DataFrame
        The filtered DataFrame containing the relevant feature data.

    Returns
    -------
    percentage : int
        The percentage corresponding to the feature and value.
    rank_ascending : int
        The rank in ascending order.
    rank_descending : int
        The rank in descending order.
    """
    percentage = int(round(100 * filtered_df.iloc[0]["percentage_share"], 0))
    rank_ascending = filtered_df.iloc[0]["rank_ascending"]
    rank_descending = filtered_df.iloc[0]["rank_descending"]

    return percentage, rank_ascending, rank_descending


def team_medal_categorical(lookup_table_categorical, feature_name, value):
    """
    Determine the percentage threshold and assign a medal based on a categorical feature.

    Parameters
    ----------
    lookup_table_categorical : pd.DataFrame
        DataFrame containing categorical lookup data with columns 'column_name',
        'value', 'percentage_share', 'rank_ascending', and 'rank_descending'.
    feature_name : str
        The name of the feature to lookup.
    value : str
        The value to compare against the lookup table.

    Returns
    -------
    percentage : int
        The percentage corresponding to the feature and value.
    rank_ascending : int
        The rank in ascending order.
    rank_descending : int
        The rank in descending order.
    """
    # Filter the lookup table for the given feature and value
    filtered_df = lookup_table_categorical[
        (lookup_table_categorical["column_name"] == feature_name)
        & (lookup_table_categorical["value"] == str(value))
    ]

    # Add a new row if the value is missing in the lookup table
    filtered_df = add_new_row_if_missing(
        filtered_df, lookup_table_categorical, feature_name, value
    )

    # Extract percentage, rank ascending, and rank descending
    percentage, rank_ascending, rank_descending = extract_rank_and_percentage(
        filtered_df
    )

    return percentage, rank_ascending, rank_descending


def generate_categorical_overview(
    medal_details, percentage, rank_ascending, rank_descending, value
):
    """
    Generate the overview text for categorical medals by replacing placeholders with actual values.

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
    value : str
        The actual value of the feature being processed.

    Returns
    -------
    overview : str
        The overview text with placeholders replaced by actual values.
    """
    p = inflect.engine()
    rank_ascending = p.ordinal(int(rank_ascending))
    rank_descending = p.ordinal(int(rank_descending))

    # Fix for values rounded to 0% to set a minimum of 1%
    if percentage == 0:
        percentage = 1

    overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
    overview = overview.replace("<rank_ascending>", rank_ascending)
    overview = overview.replace("<rank_descending>", rank_descending)
    overview = overview.replace("<value>", value)

    return overview


def assign_categorical_medal(percentage, medal_details):
    """
    Assign a medal (Gold, Silver, Bronze, or No Medal) based on the percentage and medal thresholds.

    Parameters
    ----------
    percentage : int
        The percentage share of the feature.
    medal_details : dict
        Dictionary with medal threshold details including 'gold_threshold',
        'silver_threshold', and 'bronze_threshold'.

    Returns
    -------
    medal : str
        The assigned medal ('Gold', 'Silver', 'Bronze', or 'No Medal').
    """
    if percentage <= medal_details["gold_threshold"]:
        return "Gold"
    elif percentage <= medal_details["silver_threshold"]:
        return "Silver"
    elif percentage <= medal_details["bronze_threshold"]:
        return "Bronze"
    return "No Medal"


def process_categorical_medal(
    medal_name, medal_details, team_data, lookup_table_categorical
):
    """
    Process a single categorical medal, calculate the ranks and percentage, and generate the result row.

    Parameters
    ----------
    medal_name : str
        Name of the categorical medal to process.
    medal_details : dict
        Dictionary with details of the categorical medal.
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

    # Determine the medal type based on thresholds
    medal = assign_categorical_medal(percentage, medal_details)

    # Generate the overview text
    overview = generate_categorical_overview(
        medal_details, percentage, rank_ascending, rank_descending, value
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


def get_categorical_medals(
    medal_details_categorical, lookup_table_categorical, team_data
):
    """
    Calculate medals for categorical features based on thresholds and team data.

    Parameters
    ----------
    medal_details_categorical : dict
        Dictionary with medal details for categorical features including 'feature_name',
        'gold_threshold', 'silver_threshold', 'bronze_threshold', 'text', 'image_path',
        and 'medal_background'.
    lookup_table_categorical : pd.DataFrame
        DataFrame containing categorical lookup data.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    medals : pd.DataFrame
        DataFrame with the results for all categorical medals including columns for 'Medal Name',
        'Medal', 'Overview', 'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_categorical.items():
        # Process each categorical medal
        medal_entry = process_categorical_medal(
            medal_name=medal_name,
            medal_details=medal_details,
            team_data=team_data,
            lookup_table_categorical=lookup_table_categorical,
        )
        # Append the medal entry to the medals DataFrame
        medals = pd.concat([medals, medal_entry], axis=0, ignore_index=True)

    return medals
