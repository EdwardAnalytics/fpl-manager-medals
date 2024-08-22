from src.data_prep.create_sample import get_all_data_sample
from src.data_prep.load_data import (
    get_boostrap_data,
    get_player_data,
    get_current_season_year,
)
from src.profiling.create_lookup_tables import (
    create_lookup_tables_aggregated,
)
from src.app_tools.yaml_loader import load_yaml_file
import pandas as pd
import json

### Data Collection
# Get boostrap data
bootstrap_data = get_boostrap_data()

# Get player data
current_season_year = get_current_season_year(bootstrap_data=bootstrap_data)
player_data, current_gameweek = get_player_data(current_season_year=current_season_year)

# Store metadata for scoring
file_path = "data/training_meta.json"
training_meta = {"training_data_gameweek": current_gameweek}

with open(file_path, "w") as file:
    json.dump(training_meta, file, indent=4)

# Store gameweek player data for scoring if season has started
if isinstance(player_data, pd.DataFrame):  # i.e. season has started
    file_path = f"data/vaastav-data/player_data_{current_season_year}.csv"
    player_data.to_csv(file_path)


# Get sample data
sample_data = get_all_data_sample(
    bootstrap_data=bootstrap_data,
    current_gameweek=current_gameweek,
    player_data=player_data,
)

df = pd.DataFrame(sample_data)

# Save DataFrame as CSV
file_path = f"data/sample/team_sample_data.csv"
df.to_csv(file_path, index=False)


### Profiling

# Get null imputing values
yaml_file_path = "conf/impute_nulls.yaml"
impute_nulls = load_yaml_file(yaml_file_path)

# Create profile distribution tables
lookup_table_numeric, lookup_table_categorical = create_lookup_tables_aggregated(
    df=df, impute_nulls=impute_nulls
)

# Save DataFrame as CSVs
lookup_table_numeric.to_csv(
    f"data/variable_lookup_tables/numeric_columns.csv", index=False
)
lookup_table_categorical.to_csv(
    f"data/variable_lookup_tables/categorical_columns.csv", index=False
)
