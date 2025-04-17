
import streamlit as st
import pandas as pd

def load_data():
    hts_data = pd.read_csv('htsdata.csv')
    sec301_data = pd.read_excel('Sec301-Combined-SingleSheet.xlsx')
    return hts_data, sec301_data

def clean_hts_code(hts):
    return ''.join(filter(str.isdigit, str(hts)))[:10]

def match_section_301(hts_code, sec301_df):
    short_code = hts_code.replace('.', '')[:6]
    sec301_df['HSCode_clean'] = sec301_df['HSCode'].astype(str).str.replace('.', '').str[:6]
    match = sec301_df[sec301_df['HSCode_clean'] == short_code]
    if not match.empty:
        return float(match.iloc[0]['Additional Duty']) * 100
    return 0.0

def parse_base_duty(value):
    if pd.isna(value):
        return 0.0, "0%"
    str_val = str(value).strip()
    if str_val.lower() == "free":
        return 0.0, "Free"
    elif "%" in str_val:
        try:
            rate = float(str_val.replace('%', '').strip())
            return rate, f"{rate}%"
        except:
            return 0.0, str_val
    else:
        return 0.0, str_val

def main():
    st.set_page_config(page_title="Easy Speed Tariff Calculator", layout="centered")
    st.image("easyspeedlogo.png", width=160)
    st.title("U.S. Duty & Tariff Calculator (BETA)")
    st.write("Enter one or more HTS codes to get applicable duties.")

    hts_data, sec301_data = load_data()

    num_codes = st.number_input("How many HTS codes do you want to calculate?", min_value=1, max_value=10, value=1, step=1)
    origin_country = st.selectbox("Country of Origin:", ["China", "Other"])
    shipment_value = st.number_input("Enter Total Shipment Value (USD):", min_value=0.0, value=10000.0, step=100.0)

    total_combined_duty_percent = 0.0

    for i in range(num_codes):
        st.markdown(f"### HTS Code {i + 1}")
        hts_input = st.text_input(f"Enter HTS Code {i + 1}:", f"3923.50.0000", key=f"hts_{i}")
        
        if hts_input:
            hts_clean = clean_hts_code(hts_input)
            matched_hts = hts_data[hts_data['HTS Number'].astype(str).str.replace('.', '').str.startswith(hts_clean)]

            if not matched_hts.empty:
                row = matched_hts.iloc[0]
                description = row['Description']
                base_duty_val = row['General Rate of Duty']
                base_duty, base_duty_display = parse_base_duty(base_duty_val)

                sec301_duty = match_section_301(hts_input, sec301_data)
                reciprocal_tariff = 145.0 if origin_country == "China" else 0.0
                total_duty = base_duty + sec301_duty + reciprocal_tariff
                duty_value = (total_duty / 100) * (shipment_value / num_codes)

                st.write(f"**Description**: {description}")
                st.write(f"**Base Duty**: {base_duty_display}")
                st.write(f"**Section 301 Duty**: {sec301_duty:.2f}%")
                if reciprocal_tariff:
                    st.write(f"**Reciprocal Tariff (China)**: {reciprocal_tariff:.2f}%")
                st.write(f"**Total Duty for this code**: {total_duty:.2f}%")
                st.write(f"**Estimated Duty Amount for this code**: ${duty_value:,.2f}")
                st.markdown("---")

                total_combined_duty_percent += duty_value
            else:
                st.warning(f"HTS code {hts_input} not found. Please try again with a valid code.")

    st.write(f"## 🧾 Estimated Total Duty Owed: ${total_combined_duty_percent:,.2f}")
    st.caption("Note: These estimates are for reference only and do not include quantity- or unit-based duties.")

if __name__ == '__main__':
    main()
