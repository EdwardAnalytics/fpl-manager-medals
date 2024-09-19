import streamlit as st


def create_medal_scoring(index, number_of_medals, medals_dict):
    """
    Create and display a medal entry in a Streamlit app. medals_dict here is derived from a
    dataframe containing the users medals.

    The text displayed is the medal overview (i.e. why the user has got that medal) .

    Parameters
    ----------
    index : int
        The index of the medal in the `medals_dict` to be displayed.
    number_of_medals : int
        The total number of medals to display. This function will only display
        a medal if the `index` is less than `number_of_medals`.
    medals_dict : dict
        Dictionary containing medal information. Each key in the dictionary represents
        an index and maps to another dictionary with the following keys:
        - 'Medal' : str
            The type of medal (e.g., 'Gold', 'Silver', 'Bronze').
        - 'Medal Name' : str
            The name of the medal.
        - 'Overview' : str
            A description or overview of the medal.
        - 'image_path' : str
            URL or file path to the image representing the medal.
        - 'medal_background' : str
            URL to an image or background related to the medal.

    Returns
    -------
    None
        The function displays the medal information using Streamlit components.
    """
    if index < number_of_medals:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(
                    f"{medals_dict[index]['Medal']} {medals_dict[index]['Medal Name']}"
                )
                st.markdown(
                    f"{medals_dict[index]['Overview']}<br>*[Medal Background]({medals_dict[index]['medal_background']})*",
                    unsafe_allow_html=True,
                )

            with col2:
                st.image(image=medals_dict[index]["image_path"])


def get_medal_documentation(index, number_of_medals, medal_names, medals_dict):
    """
    Display detailed information about a medal in a Streamlit app. edals_dict here is derived from a
    dictionary directly of all the medal config yamls joined together.

    The text displayed is the medal details (i.e. who is eligble for the medal) .

    Parameters
    ----------
    index : int
        The index of the medal to display. The function will only display the medal
        if the `index` is less than `number_of_medals`.
    number_of_medals : int
        The total number of medals available. This parameter ensures that the function
        only processes indices within the valid range.
    medal_names : list of str
        A list of medal names corresponding to the indices in `medals_dict`. Each name
        in the list is used to retrieve detailed information about the medal.
    medals_dict : dict
        Dictionary containing detailed information for each medal. The keys are medal names
        and each value is a dictionary with the following keys:
        - 'medal_details' : str
            A description or overview of the medal.
        - 'image_path' : str
            URL or file path to the image representing the medal.
        - 'medal_background' : str
            URL to an image or background related to the medal.

    Returns
    -------
    None
        The function displays the medal information using Streamlit components.
    """
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


def get_league_medal_scoring(
    index, number_of_medals, medal_list, league_medals, medals_dict
):
    """
    Displays league medal information based on the provided index and medal list.

    Parameters
    ----------
    index : int
        The current index in the list of medals. This determines which medal's information to display.
    number_of_medals : int
        The total number of medals in the list. The function will only process medals up to this number.
    medal_list : list of str
        A list of medal names. The function uses this list to determine which medal's details to display based on the current index.
    league_medals : pd.DataFrame
        A DataFrame containing league medal information. This DataFrame should include columns such as "Medal Name", "Manager", "Team", and "Medal".
    medals_dict : dict
        A dictionary containing additional details for each medal. The keys should be medal names and the values should be dictionaries with a key "medal_details" that provides descriptive information about the medal.

    Returns
    -------
    None
        This function does not return any value. It uses Streamlit functions to display the medal information on a web interface.
    """
    if index < number_of_medals:
        medal_name = medal_list[index]
        st.subheader(medal_name)
        league_medals_filtered = league_medals[
            league_medals["Medal Name"] == medal_name
        ]
        st.markdown(f"*{medals_dict[medal_name]['medal_details']}*")
        st.dataframe(
            league_medals_filtered[["Manager", "Team", "Medal"]],
            hide_index=True,
        )
        st.text("")
