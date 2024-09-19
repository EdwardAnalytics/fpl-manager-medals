import pandas as pd
from src.profiling.get_binary_medals import get_binary_medals
from src.profiling.get_categorical_medals import get_categorical_medals
from src.profiling.get_numeric_medals import get_numeric_medals


def combine_medals(medals_numeric, medals_categorical, medals_binary):
    """
    Combine numeric, categorical, and binary medals into a single DataFrame and remove 'No Medal' rows.

    Parameters
    ----------
    medals_numeric : pd.DataFrame
        DataFrame containing numeric medals.
    medals_categorical : pd.DataFrame
        DataFrame containing categorical medals.
    medals_binary : pd.DataFrame
        DataFrame containing binary medals.

    Returns
    -------
    medals : pd.DataFrame
        Combined DataFrame with rows where 'Medal' is not 'No Medal'.
    """
    medals = pd.concat(
        [medals_numeric, medals_categorical, medals_binary], axis=0, ignore_index=True
    )
    medals = medals[medals["Medal"] != "No Medal"]
    return medals


def add_special_medal_if_needed(medals, medal_details_special):
    """
    Add a special gold medal if no gold medals are present in the given DataFrame.

    Parameters
    ----------
    medals : pd.DataFrame
        DataFrame containing medals.
    medal_details_special : dict
        Dictionary containing special medal details.

    Returns
    -------
    medals : pd.DataFrame
        DataFrame with a special gold medal added if no gold medals were present.
    """
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
    return medals


def sort_medals(medals):
    """
    Sort the medals by their type in the order of Gold, Silver, and Bronze.

    Parameters
    ----------
    medals : pd.DataFrame
        DataFrame containing medals to be sorted.

    Returns
    -------
    medals : pd.DataFrame
        DataFrame with medals sorted by their type (Gold, Silver, Bronze).
    """
    medal_order = pd.Categorical(
        medals["Medal"], categories=["Gold", "Silver", "Bronze"], ordered=True
    )
    medals["Medal"] = medal_order
    medals = medals.sort_values(by="Medal")
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
    medals : pd.DataFrame
        Combined DataFrame with the results including columns for 'Medal Name', 'Medal', 'Overview',
        'image_path', and 'medal_background', sorted by medal type (Gold, Silver, Bronze).
    """
    # Step 1: Calculate each type of medals
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

    # Step 2: Combine all medals into one DataFrame
    medals = combine_medals(medals_numeric, medals_categorical, medals_binary)

    # Step 3: Add special medal if no gold medals are present
    medals = add_special_medal_if_needed(medals, medal_details_special)

    # Step 4: Sort medals by their type (Gold, Silver, Bronze)
    medals = sort_medals(medals)

    return medals
