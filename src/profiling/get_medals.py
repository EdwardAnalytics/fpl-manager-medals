import pandas as pd
import inflect


def team_medal_numeric(
    lookup_table_numeric, feature_name, value, objective, partition_value
):
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
