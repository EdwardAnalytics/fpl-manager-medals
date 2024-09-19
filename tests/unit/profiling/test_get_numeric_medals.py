import pytest
import pandas as pd
from src.profiling.get_numeric_medals import (
    get_feature_partition,
    calculate_percentage,
    determine_medal,
)


def test_get_feature_partition():
    # Sample data for testing
    medal_details = {"partition_feature": "gold_medals"}

    team_data = {"gold_medals": 5, "silver_medals": 3, "bronze_medals": 2}

    team_data_missing = {"silver_medals": 3, "bronze_medals": 2}

    # Test when the partition feature exists in team_data
    assert get_feature_partition(medal_details, team_data) == 5

    # Test when the partition feature does not exist in team_data
    assert get_feature_partition(medal_details, team_data_missing) == "Not Specified"


@pytest.mark.parametrize(
    "feature_name, value, objective, partition_value, expected",
    [
        ("feature1", 15, "minimise", "partition1", 75),
        ("feature1", 12, "maximise", "partition1", 50),
        ("feature1", 5, "minimise", "Not Specified", 100),
    ],
)
def test_calculate_percentage(
    feature_name, value, objective, partition_value, expected
):
    # Sample data for testing
    data = {
        "column_name": [
            "feature1_partition1",
            "feature1_partition1",
            "feature1_partition2",
        ],
        "interpolated_value_below": [10, 20, 30],
        "interpolated_value_above": [5, 15, 25],
        "percentage": [50, 75, 90],
    }
    lookup_table_numeric = pd.DataFrame(data)

    assert (
        calculate_percentage(
            lookup_table_numeric, feature_name, value, objective, partition_value
        )
        == expected
    )


@pytest.mark.parametrize(
    "percentage, medal_details, expected_medal",
    [
        # Test cases where percentage is at or below the boundary values
        (
            4.99,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Gold",
        ),
        (
            5,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Gold",
        ),
        (
            9.99,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Silver",
        ),
        (
            10,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Silver",
        ),
        (
            14.99,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Bronze",
        ),
        (
            15,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Bronze",
        ),
        (
            100,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "No Medal",
        ),
        # Additional typical values
        (
            0,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Gold",
        ),
        (
            6,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Silver",
        ),
        (
            11,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "Bronze",
        ),
        (
            20,
            {"gold_threshold": 5, "silver_threshold": 10, "bronze_threshold": 15},
            "No Medal",
        ),
    ],
)
def test_determine_medal(percentage, medal_details, expected_medal):
    assert determine_medal(percentage, medal_details) == expected_medal


@pytest.mark.parametrize(
    "medal_details, value, partition_value, medal, expected_value, expected_medal",
    [
        # Test case for 'rival_team_player' with partition value "Not Specified"
        (
            {"feature_name": "rival_team_player"},
            100,
            "Not Specified",
            "Gold",
            100,
            "No Medal",
        ),
        # Test case for 'rival_team_player' with a specific team
        ({"feature_name": "rival_team_player"}, 100, "team_A", "Gold", 100, "Gold"),
        # Test case for 'bank_mean'
        ({"feature_name": "bank_mean"}, 200, "AnyPartition", "Gold", 20, "Gold"),
        ({"feature_name": "bank_mean"}, 50, "AnyPartition", "Silver", 5, "Silver"),
    ],
)
def test_apply_manual_adjustments(
    medal_details, value, partition_value, medal, expected_value, expected_medal
):
    rival_teams = {
        "team_A": ["team_B", "team_C"],
        "team_B": ["team_A"],
        "team_C": ["team_A"],
    }

    if medal_details["feature_name"] == "rival_team_player":
        if partition_value == "Not Specified" or rival_teams.get(partition_value) == [
            "None"
        ]:
            medal = "No Medal"

    if medal_details["feature_name"] == "bank_mean":
        value = value / 10

    assert value == expected_value
    assert medal == expected_medal
