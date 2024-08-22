import pandas as pd
import numpy as np


def create_distribution_table_numeric(df, column_name):
    # Calculate the total number of non-NaN rows
    total_non_nan_rows = len(df[column_name].dropna())

    # Calculate the counts for each unique value
    value_counts = df[column_name].value_counts().sort_index()

    # Calculate percentage of rows that are each value and above
    cumulative_counts_above = value_counts.sort_index(ascending=False).cumsum()
    percentage_above = (cumulative_counts_above / total_non_nan_rows) * 100

    # Calculate percentage of rows that are each value and below
    cumulative_counts_below = value_counts.sort_index(ascending=True).cumsum()
    percentage_below = (cumulative_counts_below / total_non_nan_rows) * 100

    # Create the distribution table
    distribution_table = pd.DataFrame(
        {
            "column_name": column_name,
            "value": value_counts.index,
            "total_volume_sample": value_counts.values,
            "percentage_above": value_counts.index.map(percentage_above),
            "percentage_below": value_counts.index.map(percentage_below),
        }
    )

    # Round percentages
    distribution_table["percentage_above"] = distribution_table[
        "percentage_above"
    ].round(3)
    distribution_table["percentage_below"] = distribution_table[
        "percentage_below"
    ].round(3)

    return distribution_table


def create_distribution_table_numeric_partitioned(
    df, column_name, partition_column="Not Specified"
):
    if partition_column == "Not Specified":
        # No partitioning, just calculate the distribution
        return create_distribution_table_numeric(df, column_name)

    else:
        # Partition by the specified column
        partition_values = df[partition_column].unique()
        all_partitions = []

        for value in partition_values:
            partition_df = df[df[partition_column] == value]
            partition_table = create_distribution_table_numeric(
                partition_df, column_name
            )

            # Append partition column info to column_name
            partition_table["column_name"] = (
                partition_table["column_name"] + f"_{value}"
            )

            all_partitions.append(partition_table)

        # Combine all partitions
        final_distribution_table = pd.concat(all_partitions, ignore_index=True)

        return final_distribution_table


def create_lookup_table_numeric(distribution_table, column_name):
    # interpolate_percentage_above_below_numeric

    distribution_table = distribution_table[
        distribution_table["column_name"] == column_name
    ]
    # Extract the relevant columns
    values = distribution_table["value"]
    percentages_above = distribution_table["percentage_above"]
    percentages_below = distribution_table["percentage_below"]

    # Define the new points for interpolation (100 to 1 in increments of 5)
    new_points = np.arange(100, 0, -5)

    # Perform interpolation for percentage_above
    interpolated_values_above = np.interp(
        new_points, percentages_above[::-1], values[::-1]
    )

    # Perform interpolation for percentage_below
    interpolated_values_below = np.interp(new_points, percentages_below, values)

    # Create a new DataFrame with the interpolated results
    lookup_table = pd.DataFrame(
        {
            "column_name": column_name,
            "percentage": new_points,
            "interpolated_value_above": interpolated_values_above,
            "interpolated_value_below": interpolated_values_below,
        }
    )

    # Round values
    lookup_table["interpolated_value_above"] = lookup_table[
        "interpolated_value_above"
    ].round(3)
    lookup_table["interpolated_value_below"] = lookup_table[
        "interpolated_value_below"
    ].round(3)

    return lookup_table


def create_lookup_table_numeric_partitioned(
    distribution_table, column_name, partition_column="Not Specified"
):
    if partition_column == "Not Specified":
        # Filter the distribution table by the specified column_name
        filtered_table = distribution_table[
            distribution_table["column_name"] == column_name
        ]

        # Calculate the interpolated values without partitioning
        return create_lookup_table_numeric(filtered_table, column_name)

    else:
        # Get the unique values of the partition column
        partition_values = distribution_table["column_name"].unique()
        all_partitions = []

        for partition in partition_values:
            # Filter the distribution table by column_name and partition value
            partitioned_table = distribution_table[
                (distribution_table["column_name"] == partition)
            ]

            # Calculate the interpolated values for the current partition
            lookup_table = create_lookup_table_numeric(partitioned_table, partition)

            all_partitions.append(lookup_table)

        # Combine all lookup tables into one DataFrame
        final_lookup_table = pd.concat(all_partitions, ignore_index=True)

        return final_lookup_table


def create_lookup_table_categorical(df, column_name):
    # Calculate the proportion of each unique value
    percentage_share = df[column_name].value_counts(normalize=True)

    # Create lookup table
    lookup_table = pd.DataFrame(
        {
            "column_name": column_name,
            "value": percentage_share.index,
            "percentage_share": percentage_share.values,
        }
    )

    # Add ranks
    lookup_table["rank_ascending"] = lookup_table["percentage_share"].rank(
        method="min", ascending=True
    )
    lookup_table["rank_descending"] = lookup_table["percentage_share"].rank(
        method="min", ascending=False
    )

    # Round percentages
    lookup_table["percentage_share"] = lookup_table["percentage_share"].round(3)

    return lookup_table


def create_lookup_tables_aggregated(df, impute_nulls):
    column_data_types = {
        "player_region_iso_code_long": "categorical",
        "name_change_blocked": "categorical",
        "kit": "categorical",
        "kit_shirt_type": "categorical",
        "kit_shirt_logo": "categorical",
        "kit_socks_type": "categorical",
        "kit_shorts": "categorical",
        "kit_full": "categorical",
        "classic_leagues_competed_in": "numeric",
        "h2h_leagues_competed_in": "numeric",
        "last_deadline_bank": "numeric",
        "last_deadline_value": "numeric",
        "last_deadline_total_transfers": "numeric",
        "summary_overall_points": "numeric",
        "summary_overall_rank": "numeric",
        "leagues_admin": "numeric",
        "min_rank_history": "numeric",
        "max_total_points_history": "numeric",
        "earliest_season_year_history": "numeric",
        "career_break_history": "numeric",
        "seasons_played_in": "numeric",
        "yoyo_score": "numeric",
        "rising_score": "numeric",
        "assists": "numeric",
        "bonus": "numeric",
        "bps": "numeric",
        "clean_sheets": "numeric",
        "goals_conceded": "numeric",
        "goals_scored": "numeric",
        "own_goals": "numeric",
        "penalties_missed": "numeric",
        "penalties_saved": "numeric",
        "red_cards": "numeric",
        "yellow_cards": "numeric",
        "saves": "numeric",
        "rival_team_player": "numeric",
        "total_players_starters": "numeric",
        "total_players_all": "numeric",
        "rival_team_player_categorical": "categorical",
        "points_on_bench_total": "numeric",
        "event_transfers_total": "numeric",
        "event_transfers_cost_total": "numeric",
        "bank_mean": "numeric",
        "bank_latest": "numeric",
        "value_latest": "numeric",
        "total_points_latest": "numeric",
        "points_on_bench_percentage": "numeric",
        "favourite_team": "categorical",
    }

    partition_columns = {"rival_team_player": "favourite_team"}

    # Fill NaN values in each column with specified values
    df = df.fillna(value=impute_nulls)

    lookup_table_numeric = pd.DataFrame(
        columns=[
            "column_name",
            "percentage",
            "interpolated_value_above",
            "interpolated_value_below",
        ]
    )
    lookup_table_categorical = pd.DataFrame(
        columns=[
            "column_name",
            "value",
            "percentage_share",
            "rank_ascending",
            "rank_descending",
        ]
    )

    for column_name, column_type in column_data_types.items():
        if column_type == "numeric":
            # Get partition
            try:
                partition_column = partition_columns[column_name]
            except:
                partition_column = "Not Specified"

            distribution_table_stage_numeric = (
                create_distribution_table_numeric_partitioned(
                    df=df, column_name=column_name, partition_column=partition_column
                )
            )
            if len(distribution_table_stage_numeric) > 0:
                lookup_table_stage_numeric = create_lookup_table_numeric_partitioned(
                    distribution_table=distribution_table_stage_numeric,
                    column_name=column_name,
                    partition_column=partition_column,
                )
                lookup_table_numeric = pd.concat(
                    [lookup_table_numeric, lookup_table_stage_numeric], axis=0
                )
            else:
                continue
        elif column_type == "categorical":
            lookup_table_stage_categorical = create_lookup_table_categorical(
                df=df, column_name=column_name
            )
            lookup_table_categorical = pd.concat(
                [lookup_table_categorical, lookup_table_stage_categorical],
                axis=0,
            )

    return lookup_table_numeric, lookup_table_categorical
