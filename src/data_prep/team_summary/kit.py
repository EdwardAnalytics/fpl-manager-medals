import pandas as pd
import ast


def get_kit_information(team_data):
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
