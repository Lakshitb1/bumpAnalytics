import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests

from analysis import overview
from analysis import bump
from analysis import pothole

# Title of the Streamlit app
st.title("Sensor Data Analytics")

# Get the API URL from query parameters
query_params = st.query_params
api_url = query_params.get("api", None)

if not api_url:
    st.error("No API endpoint provided. Please pass the 'api' parameter in the URL.")
else:
    st.write(f"Fetching data from API: `{api_url}`")

    try:
        # Fetch the data from the Flask endpoint
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == "success":
                # Extract readings from the response
                readings = data.get("readings", [])
                if not readings:
                    st.warning("No readings found in the API response.")
                    st.stop()

                # Convert readings into a DataFrame
                df_main = pd.DataFrame(readings)

                if df_main.empty:
                    st.warning("The fetched data is empty. Please check the API response.")
                    st.stop()

                # Ensure correct data types for columns
                df_main["timestamp"] = pd.to_datetime(df_main["timestamp"])
                df_main["x"] = pd.to_numeric(df_main["x"], errors='coerce')
                df_main["y"] = pd.to_numeric(df_main["y"], errors='coerce')
                df_main["z"] = pd.to_numeric(df_main["z"], errors='coerce')

                # Display Data and Analytics
                st.title("Data Analytics")
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Fetched Sensor Data")
                        st.dataframe(df_main)
                    with col2:
                        st.subheader("Data Summary")
                        st.write(df_main.describe())

                # Option Menu for Different Analyses
                with st.container():
                    selected = option_menu(
                        menu_title=None,
                        options=['OverView', 'Bump Analysis', 'Pothole Analysis'],
                        icons=['book', 'bar-chart', 'robot'],
                        orientation='horizontal'
                    )

                    if selected == 'OverView':
                        overview.show_overview(df_main)

                    if selected == 'Bump Analysis':
                        # Filter bump-related data
                        bump_data = df_main[df_main["label"] == "bump"]
                        if not bump_data.empty:
                            bump.show_bump(bump_data)
                        else:
                            st.warning("No 'bump' data available for analysis.")

                    if selected == 'Pothole Analysis':
                        # Filter pothole-related data
                        pothole_data = df_main[df_main["label"] == "pothole"]
                        if not pothole_data.empty:
                            pothole.show_pothole(pothole_data)
                        else:
                            st.warning("No 'pothole' data available for analysis.")

                st.success("Prediction completed successfully!")
            else:
                error_message = data.get('message', 'Unknown error occurred')
                st.error(f"API Error: {error_message}")
        else:
            st.error(f"Failed to fetch data. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"HTTP Request Error: {str(e)}")
    except ValueError as e:
        st.error(f"Data Parsing Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
