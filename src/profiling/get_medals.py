import pandas as pd
import inflect

from src.app_tools.yaml_loader import load_yaml_file

# Get medal details
yaml_file_path = "conf/rival_teams.yaml"
rival_teams = load_yaml_file(yaml_file_path)


def team_medal_numeric(
    lookup_table_numeric, feature_name, value, objective, partition_value
):
    """
    Determine the percentage threshold and assign a medal based on a numeric feature.

    Parameters
    ----------
    lookup_table_numeric : pd.DataFrame
        DataFrame containing numeric lookup data with columns 'column_name',
        'interpolated_value_below', 'interpolated_value_above', and 'percentage'.
    feature_name : str
        The name of the feature to lookup.
    value : float
        The value to compare against the lookup table.
    objective : str
        The objective for the comparison, which can be 'minimise' or 'maximise'.
    partition_value : str
        The partition value used to refine the feature name (e.g., a specific category).

    Returns
    -------
    float
        The percentage corresponding to the feature and value based on the given objective.
    """
    if partition_value != "Not Specified":
        feature_name = f"{feature_name}_{partition_value}"

    if objective == "minimise":
        # Filter rows where 'value' is greater than the threshold
        interpolated_value_col = "interpolated_value_below"
        filtered_df = lookup_table_numeric[
            (lookup_table_numeric["column_name"] == feature_name)
            & (lookup_table_numeric[interpolated_value_col] >= value)
        ]

        # Find the minimum 'percentage_below' from the filtered rows
        percentage = filtered_df["percentage"].min()
    elif objective == "maximise":
        # Filter rows where 'value' is less than the threshold
        interpolated_value_col = "interpolated_value_above"
        filtered_df = lookup_table_numeric[
            (lookup_table_numeric["column_name"] == feature_name)
            & (lookup_table_numeric[interpolated_value_col] <= value)
        ]

        # Find the minimum 'percentage_below' from the filtered rows
        percentage = filtered_df["percentage"].min()

    # Set percentage to 100 if it is outside of the observned data
    # Note: if the objective is to minimise and the value is lower than the minimum value, it will calcuated as the lowest percentage
    # Likewise for maximise (except if it's higher than the maximum value)
    percentage = percentage if not pd.isna(percentage) else 100

    return percentage


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
    tuple
        A tuple containing:
        - int: The percentage corresponding to the feature and value.
        - int: The rank in ascending order.
        - int: The rank in descending order.
    """
    # Categorical
    filtered_df = lookup_table_categorical[
        (lookup_table_categorical["column_name"] == feature_name)
        & (lookup_table_categorical["value"] == str(value))
    ]

    # Adding new value if it did not appear in training data
    if len(filtered_df) == 0:
        # Adding a new row using append
        # Get max rank asending
        rank_ascending_max = max(
            lookup_table_categorical[
                lookup_table_categorical["column_name"] == feature_name
            ]["rank_ascending"]
        )

        new_row = pd.DataFrame(
            {
                "column_name": ["player_region_iso_code_long"],
                "value": str(value),
                "percentage_share": [0.01],
                "rank_ascending": [rank_ascending_max],
                "rank_descending": [1.0],
            }
        )

        filtered_df = pd.concat([filtered_df, new_row], ignore_index=True)

    percentage = int(round(100 * filtered_df.iloc[0]["percentage_share"], 0))
    rank_ascending = filtered_df.iloc[0]["rank_ascending"]
    rank_descending = filtered_df.iloc[0]["rank_descending"]

    return percentage, rank_ascending, rank_descending


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
        DataFrame with the results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_numeric.items():
        feature_name = medal_details["feature_name"]
        objective = medal_details["objective"]
        value = team_data[feature_name]

        # Checking if None, i.e. no historical data
        if value == None:
            continue

        try:
            partition_column = medal_details["partition_feature"]
            partition_value = team_data[partition_column]
        except:
            partition_value = "Not Specified"

        percentage = team_medal_numeric(
            lookup_table_numeric=lookup_table_numeric,
            feature_name=feature_name,
            value=value,
            objective=objective,
            partition_value=partition_value,
        )

        # Define medal
        if percentage <= medal_details["gold_threshold"]:
            medal = "Gold"
        elif percentage <= medal_details["silver_threshold"]:
            medal = "Silver"
        elif percentage <= medal_details["bronze_threshold"]:
            medal = "Bronze"
        else:
            medal = "No Medal"

        # Manual fix for teams with no rival
        if (
            medal_details["feature_name"] == "rival_team_player"
            and partition_value == "Not Specified"
        ):
            medal = "No Medal"
        elif medal_details["feature_name"] == "rival_team_player" and rival_teams[
            partition_value
        ] == ["None"]:
            medal = "No Medal"

        # Manual fix for bank value, it is 10 times the actual value in the data
        if medal_details["feature_name"] == "bank_mean":
            value = value / 10

        # Update text/overview
        overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
        overview = overview.replace("<value>", f'{format(value, ",")}')
        overview = overview.replace("<partition_value>", partition_value)

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


def get_categorical_medals(
    medal_details_categorical, lookup_table_categorical, team_data
):
    """
    Calculate medals for categorical features based on thresholds and team data.

    Parameters
    ----------
    medal_details_categorical : dict
        Dictionary with medal details for categorical features including
        'feature_name', 'gold_threshold', 'silver_threshold', 'bronze_threshold',
        'text', 'image_path', and 'medal_background'.
    lookup_table_categorical : pd.DataFrame
        DataFrame with categorical lookup data.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    pd.DataFrame
        DataFrame with the results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_categorical.items():
        feature_name = medal_details["feature_name"]
        value = team_data[feature_name]

        percentage, rank_ascending, rank_descending = team_medal_categorical(
            lookup_table_categorical=lookup_table_categorical,
            feature_name=feature_name,
            value=value,
        )

        # Define medal
        if percentage <= medal_details["gold_threshold"]:
            medal = "Gold"
        elif percentage <= medal_details["silver_threshold"]:
            medal = "Silver"
        elif percentage <= medal_details["bronze_threshold"]:
            medal = "Bronze"
        else:
            medal = "No Medal"

        # Update text/overview
        p = inflect.engine()
        rank_ascending = p.ordinal(int(rank_ascending))
        rank_descending = p.ordinal(int(rank_descending))

        # Fix for those round to 0%:
        if percentage == 0:
            percentage = 1

        overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
        overview = overview.replace("<rank_ascending>", rank_ascending)
        overview = overview.replace("<rank_descending>", rank_descending)
        overview = overview.replace("<value>", value)

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
    pd.DataFrame
        DataFrame with the results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background'.
    """
    medals = pd.DataFrame(
        columns=["Medal Name", "Medal", "Overview", "image_path", "medal_background"]
    )

    for medal_name, medal_details in medal_details_binary.items():
        feature_name = medal_details["feature_name"]
        value = team_data[feature_name]

        percentage, rank_ascending, rank_descending = team_medal_categorical(
            lookup_table_categorical=lookup_table_categorical,
            feature_name=feature_name,
            value=value,
        )

        if value == medal_details["gold_values"]:
            medal = "Gold"
        else:
            medal = "No Medal"

        # Update text/overview
        p = inflect.engine()
        rank_ascending = p.ordinal(int(rank_ascending))
        rank_descending = p.ordinal(int(rank_descending))

        overview = medal_details["text"].replace("<percentage>", f"{percentage}%")
        overview = overview.replace("<rank_ascending>", rank_ascending)
        overview = overview.replace("<rank_descending>", rank_descending)

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


def get_all_medals(
    medal_details_numeric,
    lookup_table_numeric,
    medal_details_categorical,
    lookup_table_categorical,
    medal_details_binary,
    medal_details_special,
    team_data,
):
    """
    Aggregate and calculate all types of medals (numeric, categorical, binary) for a team based on provided data.

    Parameters
    ----------
    medal_details_numeric : dict
        Dictionary with medal details for numeric features.
    lookup_table_numeric : pd.DataFrame
        DataFrame with numeric lookup data.
    medal_details_categorical : dict
        Dictionary with medal details for categorical features.
    lookup_table_categorical : pd.DataFrame
        DataFrame with categorical lookup data.
    medal_details_binary : dict
        Dictionary with medal details for binary features.
    medal_details_special : dict
        Dictionary with special medal details.
    team_data : dict
        Dictionary containing the team's data for comparison.

    Returns
    -------
    pd.DataFrame
        DataFrame with the combined results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background', sorted by medal type (Gold, Silver, Bronze).
    """
    medals_numeric = get_numeric_medals(
        medal_details_numeric=medal_details_numeric,
        lookup_table_numeric=lookup_table_numeric,
        team_data=team_data,
    )
    medals_categorical = get_categorical_medals(
        medal_details_categorical=medal_details_categorical,
        lookup_table_categorical=lookup_table_categorical,
        team_data=team_data,
    )
    medals_binary = get_binary_medals(
        medal_details_binary=medal_details_binary,
        lookup_table_categorical=lookup_table_categorical,
        team_data=team_data,
    )
    medals = pd.concat(
        [medals_numeric, medals_categorical, medals_binary], axis=0, ignore_index=True
    )
    # Select only gold, silver and bronze medals (i.e. remove 'No Medal' rows)
    medals = medals[medals["Medal"] != "No Medal"]

    # Check if the manager has no gold medals
    if "Gold" not in medals["Medal"].values:
        medal_name = "Harry Kane Award"
        new_row = pd.DataFrame(
            {
                "Medal Name": [medal_name],
                "Medal": ["Gold"],
                "Overview": [medal_details_special[medal_name]["text"]],
                "image_path": [medal_details_special[medal_name]["image_path"]],
                "medal_background": [
                    medal_details_special[medal_name]["medal_background"]
                ],
            }
        )
        medals = pd.concat([new_row, medals], ignore_index=True)

    # Define the order of the categories
    medal_order = pd.Categorical(
        medals["Medal"], categories=["Gold", "Silver", "Bronze"], ordered=True
    )

    # Assign the categorical data type to the 'medal' column
    medals["Medal"] = medal_order

    # Sort the DataFrame by the 'medal' column
    medals = medals.sort_values(by="Medal")

    return medals
