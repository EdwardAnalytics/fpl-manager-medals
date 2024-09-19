import pandas as pd
from src.app_tools.yaml_loader import load_yaml_file

# Load rival teams from the YAML file
yaml_file_path = "conf/rival_teams.yaml"
rival_teams = load_yaml_file(yaml_file_path)


def get_feature_partition(medal_details, team_data):
    """
    Determine the partition value for a feature.

    Parameters
    ----------
    medal_details : dict
        Dictionary containing medal details for a feature.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    str
        The partition value or 'Not Specified' if not applicable.
    """
    try:
        return team_data[medal_details["partition_feature"]]
    except KeyError:
        return "Not Specified"


def calculate_percentage(
    lookup_table_numeric, feature_name, value, objective, partition_value
):
    """
    Calculate the percentage based on a numeric feature, objective, and partition value.

    Parameters
    ----------
    lookup_table_numeric : pd.DataFrame
        DataFrame containing numeric lookup data.
    feature_name : str
        The name of the feature to lookup.
    value : float
        The value to compare against the lookup table.
    objective : str
        The objective for the comparison, either 'minimise' or 'maximise'.
    partition_value : str
        The partition value used to refine the feature name.

    Returns
    -------
    float
        The percentage corresponding to the feature and value.
    """
    if partition_value != "Not Specified":
        feature_name = f"{feature_name}_{partition_value}"

    if objective == "minimise":
        interpolated_value_col = "interpolated_value_below"
        filtered_df = lookup_table_numeric[
            (lookup_table_numeric["column_name"] == feature_name)
            & (lookup_table_numeric[interpolated_value_col] >= value)
        ]
    elif objective == "maximise":
        interpolated_value_col = "interpolated_value_above"
        filtered_df = lookup_table_numeric[
            (lookup_table_numeric["column_name"] == feature_name)
            & (lookup_table_numeric[interpolated_value_col] <= value)
        ]

    percentage = filtered_df["percentage"].min()
    return percentage if not pd.isna(percentage) else 100


def determine_medal(percentage, medal_details):
    """
    Determine the medal type based on the percentage and medal thresholds.

    Parameters
    ----------
    percentage : float
        The percentage for the feature.
    medal_details : dict
        Dictionary containing medal thresholds.

    Returns
    -------
    str
        The medal type: 'Gold', 'Silver', 'Bronze', or 'No Medal'.
    """
    if percentage <= medal_details["gold_threshold"]:
        return "Gold"
    elif percentage <= medal_details["silver_threshold"]:
        return "Silver"
    elif percentage <= medal_details["bronze_threshold"]:
        return "Bronze"
    else:
        return "No Medal"


def apply_manual_adjustments(medal_details, value, partition_value, medal):
    """
    Apply manual adjustments for specific features like 'rival_team_player' and 'bank_mean'.

    Parameters
    ----------
    medal_details : dict
        Dictionary containing medal details for a feature.
    value : float
        The current value being evaluated.
    partition_value : str
        The partition value for the feature.
    medal : str
        The current medal assigned based on thresholds.

    Returns
    -------
    value : float
        Adjusted value for specific features like 'bank_mean'.
    medal : str
        Adjusted medal based on conditions like 'rival_team_player'.
    """
    if medal_details["feature_name"] == "rival_team_player":
        if partition_value == "Not Specified" or rival_teams.get(partition_value) == [
            "None"
        ]:
            medal = "No Medal"

    if medal_details["feature_name"] == "bank_mean":
        value = value / 10

    return value, medal


def format_overview(medal_details, percentage, value, partition_value):
    """
    Format the overview text for the medal based on details.

    Parameters
    ----------
    medal_details : dict
        Dictionary containing medal details including text template.
    percentage : float
        The percentage for the feature.
    value : float
        The current value being evaluated.
    partition_value : str
        The partition value for the feature.

    Returns
    -------
    str
        The formatted overview text.
    """
    overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
    overview = overview.replace("<value>", f'{format(value, ",")}')
    overview = overview.replace("<partition_value>", partition_value)
    return overview


def get_numeric_medals(medal_details_numeric, lookup_table_numeric, team_data):
    """
    Calculate medals for numeric features based on thresholds and team data.

    Parameters
    ----------
    medal_details_numeric : dict
        Dictionary with medal details for numeric features including 'feature_name',
        'objective', 'partition_feature', 'gold_threshold', 'silver_threshold',
        'bronze_threshold', 'text', 'image_path', and 'medal_background'.
    lookup_table_numeric : pd.DataFrame
        DataFrame with numeric lookup data.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame with the results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_numeric.items():
        feature_name = medal_details["feature_name"]
        objective = medal_details["objective"]
        value = team_data.get(feature_name)

        # Skip if value is None
        if value is None:
            continue

        partition_value = get_feature_partition(medal_details, team_data)

        # Calculate the percentage based on numeric lookup
        percentage = calculate_percentage(
            lookup_table_numeric=lookup_table_numeric,
            feature_name=feature_name,
            value=value,
            objective=objective,
            partition_value=partition_value,
        )

        # Determine the medal based on percentage
        medal = determine_medal(percentage, medal_details)

        # Apply manual adjustments for specific features
        value, medal = apply_manual_adjustments(
            medal_details, value, partition_value, medal
        )

        # Format the overview text with relevant details
        overview = format_overview(medal_details, percentage, value, partition_value)

        # Create a DataFrame entry for this medal and append to the medals DataFrame
        medal_stage = pd.DataFrame(
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
        medals = pd.concat([medals, medal_stage], axis=0, ignore_index=True)

    return medals
