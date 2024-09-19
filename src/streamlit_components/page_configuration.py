import streamlit as st
import base64


def hide_streamlit_deploy_button():
    """
    Hide the deploy button in Streamlit.

    Returns
    -------
    None
    """
    st.markdown(
        r"""
        <style>
        .stDeployButton {
                visibility: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_streamlit_header_with_logo(github_url, logo_image_path):
    """
    Create a Streamlit header with a GitHub link and logo.

    Parameters
    ----------
    github_url : str
        URL to the GitHub repository.
    logo_image_path : str
        Path to the logo image.

    Returns
    -------
    None
    """
    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight: 0 !important;
            font-size: 15px !important;
            padding-top: 0px !important;
            margin-left: 0px;
            font-style: italic; 
        }
        .logo-img {
            float:right;
            width: 28px;
            height: 28px;
            margin-right: 8px; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(logo_image_path, "rb").read()).decode()}">
            <p class="logo-text"><a href="{github_url}">GitHub Repo</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
