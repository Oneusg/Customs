
import streamlit as st
import pandas as pd

# Load the HTS data and Section 301 codes
hts_data = pd.read_csv("htsdata.csv")
sec301_data = pd.read_csv("sec301_hts_codes.csv")
sec301_set = set(sec301_data['HTS Code'].astype(str).str.strip())

# Set up the interface
st.title("HTS Duty and Tariff Calculator (Including 145% China Reciprocal Tariff)")

hts_input = st.text_input("Enter HTS Code (e.g., 3923.50.0000)")

if hts_input:
    input_code = hts_input.strip()
    match = hts_data[hts_data['HTS Number'] == input_code]
    
    if not match.empty:
        desc = match.iloc[0]['Description']
        general_duty = match.iloc[0]['General Rate of Duty']
        existing_additional_duties = match.iloc[0]['Additional Duties']
        
        # Clean and parse existing duty rate
        try:
            general_rate = float(str(general_duty).replace('%', '').strip()) if '%' in str(general_duty) else 0
        except:
            general_rate = 0

        # Parse any listed "Additional Duties"
        try:
            add_rate = float(str(existing_additional_duties).replace('%', '').strip()) if '%' in str(existing_additional_duties) else 0
        except:
            add_rate = 0

        # Check if HTS code is in Section 301 list
        if input_code in sec301_set:
            sec301_duty = 25  # Defaulting to 25% for Sec 301 items
            add_rate += sec301_duty
            sec301_note = "Yes (25%)"
        else:
            sec301_note = "No"

        total_tariff = general_rate + add_rate + 145  # 145% reciprocal tariff for China

        st.markdown(f"**Description:** {desc}")
        st.markdown(f"**General Duty Rate:** {general_duty}")
        st.markdown(f"**Additional Duties:** {existing_additional_duties}")
        st.markdown(f"**Section 301 Tariff:** {sec301_note}")
        st.markdown(f"**Reciprocal Tariff (China):** 145%")
        st.markdown(f"**Estimated Total Tariff (Chinese Origin):** {total_tariff:.2f}%")
    else:
        st.error("HTS code not found.")
