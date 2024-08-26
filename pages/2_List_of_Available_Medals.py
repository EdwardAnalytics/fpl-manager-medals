import streamlit as st
from src.app_tools.yaml_loader import load_yaml_file

# Get medal details
yaml_file_path = "conf/medal_details/medal_details_numeric.yaml"
medal_details_numeric = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_categorical.yaml"
medal_details_categorical = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_binary.yaml"
medal_details_binary = load_yaml_file(yaml_file_path)

yaml_file_path = "conf/medal_details/medal_details_special.yaml"
medal_details_special = load_yaml_file(yaml_file_path)

# Combine medals
medals_dict = {
    **medal_details_numeric,
    **medal_details_categorical,
    **medal_details_binary,
    **medal_details_special,
}

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
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])

index += 1
if index < number_of_medals:
    with st.container(border=True):
        medal_name = medal_names[index]
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{medal_name}")
            st.markdown(
                f"{medals_dict[medal_name]['medal_details']}<br>*[Medal Background]({medals_dict[medal_name]['medal_background']})*",
                unsafe_allow_html=True,
            )

        with col2:
            st.image(image=medals_dict[medal_name]["image_path"])
