import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading the file: {e}")
        return None

# Check if a zone is restricted
def check_restricted(zone_name, data):
    result = data[data['Zone_Name'] == zone_name]['Restricted_Access']
    if not result.empty:
        return result.values[0]
    else:
        return "Zone not found in the dataset."

# Streamlit app
def main():
    st.title("Zone Access Checker")
    st.write("This app checks if a zone is restricted or not based on your dataset.")
    
    # Path to your dataset
    file_path ="D:/6 SEM LAB\DL LAB/hazard/zone_based_safety_monitoring.csv"
    
    # Load the data
    data = load_data(file_path)
    
    if data is not None:
        st.write("Dataset Preview:")
        st.dataframe(data.head())
        
        # Input zone name
        zone_name = st.text_input("Enter Zone Name:")
        
        if st.button("Check Access"):
            if zone_name.strip() != "":
                is_restricted = check_restricted(zone_name, data)
                if is_restricted == "Zone not found in the dataset.":
                    st.warning(f"The zone '{zone_name}' was not found in the dataset.")
                elif is_restricted == "Yes":
                    st.success(f"The zone '{zone_name}' is **Restricted**.")
                elif is_restricted == "No":
                    st.info(f"The zone '{zone_name}' is **Not Restricted**.")
                else:
                    st.error("Unexpected value found in the dataset.")
            else:
                st.warning("Please enter a valid Zone Name.")
    else:
        st.error("Failed to load dataset.")

if __name__ == "__main__":
    main()
