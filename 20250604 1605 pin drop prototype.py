import streamlit as st
from streamlit_folium import st_folium
import folium

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="NZ Demographic Pin Drop")

st.title("🗺️ New Zealand Demographic Data by Pin Drop")
st.markdown("Drop a pin on the map to get its coordinates and simulated demographic data for the general region.")

# --- Map Initialization ---
# Center the map on New Zealand
initial_lat = -40.9006  # Approximate center of NZ
initial_lon = 174.8860
initial_zoom = 5

m = folium.Map(location=[initial_lat, initial_lon], zoom_start=initial_zoom)

# Add a marker for the initial center (optional)
folium.Marker(
    location=[initial_lat, initial_lon],
    tooltip="Initial Center of NZ",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Add a click event listener to the map
# This JavaScript code sends the clicked coordinates back to Streamlit
m.add_child(folium.LatLngPopup())

# --- Display Map in Streamlit ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Click on the map to drop a pin:")
    output = st_folium(m, width=None, height=500, returned_objects=["last_clicked"])

with col2:
    if output and output["last_clicked"]:
        st.subheader("Location Information:")
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]

        st.success(f"Pin dropped at: Latitude {lat:.4f}, Longitude {lon:.4f}")

        # --- Simulated Demographic Data Retrieval ---
        st.subheader("Simulated Demographic Data:")

        # Simple regional classification for demonstration
        if lat < -41.0:
            region = "South Island"
            simulated_data = {
                "Region": "South Island",
                "Estimated Population (2023)": "Approx. 1.2 million",
                "Major Industries": "Agriculture, Tourism, Hydroelectric Power",
                "Key Demographics": "Slightly older population, higher proportion of European ethnicity",
                "Average Household Size": "2.5 people",
                "Notes": "This is simulated data. Real demographic data would be much more granular and specific to the exact statistical area."
            }
        elif lat >= -41.0 and lat < -36.0:
            region = "Central North Island"
            simulated_data = {
                "Region": "Central North Island",
                "Estimated Population (2023)": "Approx. 1.5 million",
                "Major Industries": "Dairy Farming, Forestry, Geothermal Energy, Tourism",
                "Key Demographics": "Diverse population, significant Māori population, younger families in some areas",
                "Average Household Size": "2.8 people",
                "Notes": "This is simulated data. Real demographic data would be much more granular and specific to the exact statistical area."
            }
        else:
            region = "Upper North Island (Auckland/Northland)"
            simulated_data = {
                "Region": "Upper North Island (Auckland/Northland)",
                "Estimated Population (2023)": "Approx. 2.0 million",
                "Major Industries": "Finance, Technology, Trade, Tourism, Manufacturing",
                "Key Demographics": "Highly diverse, younger population, significant Asian and Pacific Islander populations",
                "Average Household Size": "3.1 people",
                "Notes": "This is simulated data. Real demographic data would be much more granular and specific to the exact statistical area."
            }

        st.info(f"Based on your pin location, you are in the **{region}**.")
        for key, value in simulated_data.items():
            st.write(f"**{key}:** {value}")


        else:
            st.info("Click anywhere on the map to drop a pin and see location details.")

st.markdown(
    """
    ---
    **How real demographic data would be obtained:**
    1.  **Spatial Lookup:** Use the clicked latitude/longitude to find the specific Statistical Area 1 (SA1) or Meshblock boundary it falls within. This requires a geographic dataset of NZ boundaries.
    2.  **Stats NZ API Query:** Once the SA1/Meshblock ID is known, an API call to Statistics New Zealand's Aotearoa Data Explorer API would be made to retrieve relevant demographic indicators (e.g., population counts, age distribution, ethnicity, income, household composition) for that specific area.
    3.  **Data Processing:** The API response (typically JSON) would be parsed and presented.
    """
)        
