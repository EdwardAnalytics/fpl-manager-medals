import pandas as pd
import ast


def get_kit_information(team_data):
    """
    Extracts and processes information about a team's kit from the provided team data.

    The function checks if the team has a kit and extracts details such as the type of shirt, logo, socks, and shorts.
    It also determines if the kit is considered a "full kit" (socks/shorts/shirt populated).

    Parameters
    ----------
    team_data : dict
        A dictionary containing data about the team, including a string representation of the team's kit details.

    Returns
    -------
    kit_summary_data : dict
        A dictionary summarizing the kit information with the following keys:
        - "kit": Boolean indicating whether a kit is available.
        - "kit_shirt_type": The type of shirt in the kit.
        - "kit_shirt_logo": The logo on the shirt.
        - "kit_socks_type": The type of socks in the kit.
        - "kit_shorts": The type of shorts in the kit.
        - "kit_full": Boolean indicating whether the kit is considered a "full kit" (socks/shorts/shirt populated).
    """
    if team_data["kit"] is None:
        kit = False
        kit_shirt_type = None
        kit_shirt_logo = None
        kit_socks_type = None
        kit_shorts = None
        kit_shirt_base = None

    else:
        kit_dict = ast.literal_eval(team_data["kit"])
        kit = True
        kit_shirt_type = kit_dict["kit_shirt_type"]
        kit_shirt_logo = kit_dict["kit_shirt_logo"]
        kit_socks_type = kit_dict["kit_socks_type"]
        kit_shorts = kit_dict["kit_shorts"]
        kit_shirt_base = kit_dict["kit_shirt_base"]

    # Append full kit flag
    kit_full = (
        kit_shirt_type is not None
        and kit_shirt_type.lower() != "none"
        and kit_socks_type is not None
        and kit_socks_type.lower() != "none"
        and kit_shorts is not None
        and kit_shorts.lower() != "none"
        and kit_shirt_base.upper() != "#E1E1E1"
    )

    kit_summary_data = {
        "kit": kit,
        "kit_shirt_type": kit_shirt_type,
        "kit_shirt_logo": kit_shirt_logo,
        "kit_socks_type": kit_socks_type,
        "kit_shorts": kit_shorts,
        "kit_full": kit_full,
    }

    return kit_summary_data
