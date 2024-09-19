import streamlit as st
from src.app_tools.yaml_loader import load_multiple_yaml_files_combined
from src.streamlit_components.get_medals import get_medal_documentation

# Get medal details
file_paths = [
    "conf/medal_details/medal_details_numeric.yaml",
    "conf/medal_details/medal_details_categorical.yaml",
    "conf/medal_details/medal_details_binary.yaml",
    "conf/medal_details/medal_details_special.yaml",
]
medals_dict = load_multiple_yaml_files_combined(file_paths)

# Get medal names in list
medal_names = list(medals_dict.keys())
medal_names.sort()
number_of_medals = len(medal_names)


st.set_page_config(
    page_title="List of Available Medals",
    page_icon=":soccer:",
)

st.title("List of Avilable Medals")

index = 0
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)

index += 1
get_medal_documentation(
    index=index,
    number_of_medals=number_of_medals,
    medal_names=medal_names,
    medals_dict=medals_dict,
)
