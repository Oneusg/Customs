
import streamlit as st
import pandas as pd

# Load the HTS data
hts_data = pd.read_csv("htsdata.csv")

# Set up the interface
st.title("HTS Duty and Tariff Calculator (Including 145% China Reciprocal Tariff)")

hts_input = st.text_input("Enter HTS Code (e.g., 3923.50.0000)")

if hts_input:
    match = hts_data[hts_data['HTS Number'] == hts_input.strip()]
    
    if not match.empty:
        desc = match.iloc[0]['Description']
        general_duty = match.iloc[0]['General Rate of Duty']
        additional_duties = match.iloc[0]['Additional Duties']
        
        try:
            general_rate = float(str(general_duty).replace('%', '').strip()) if '%' in str(general_duty) else 0
        except:
            general_rate = 0

        try:
            add_rate = float(str(additional_duties).replace('%', '').strip()) if '%' in str(additional_duties) else 0
        except:
            add_rate = 0

        total_tariff = general_rate + add_rate + 145  # 145% reciprocal tariff for China

        st.markdown(f"**Description:** {desc}")
        st.markdown(f"**General Duty Rate:** {general_duty}")
        st.markdown(f"**Additional Duties:** {additional_duties}")
        st.markdown(f"**Reciprocal Tariff (China):** 145%")
        st.markdown(f"**Estimated Total Tariff (Chinese Origin):** {total_tariff:.2f}%")
    else:
        st.error("HTS code not found.")
