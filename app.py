import pandas as pd
import streamlit as st

# Căile locale către fișiere
CSV_PATH = "data/web_bl_bs_sl_an2023.csv"
TXT_PATH = "data/web_bl_bs_sl_an2023.txt"

@st.cache_data(show_spinner="Se încarcă datele...")
def incarca_date_si_legenda():
    # Încarcă datele din fișierul .txt
    df_data = pd.read_csv(TXT_PATH, sep=";", dtype=str, low_memory=False)
    df_data.columns = df_data.columns.str.strip()

    # Încarcă legenda din fișierul .csv
    df_legend_raw = pd.read_csv(CSV_PATH, sep=";", header=None, names=["Label"])
    legend_dict = {}
    for row in df_legend_raw["Label"]:
        if ";" in row:
            descriere, cod = row.split(";", 1)
            legend_dict[cod.strip()] = descriere.strip()
    return df_data, legend_dict

st.title("🔍 Căutare situații financiare 2023")

# Câmpuri de căutare
cui = st.text_input("Caută după CUI:")
caen = st.text_input("Caută după cod CAEN:")

# Încărcare date
df, legenda = incarca_date_si_legenda()

# Curățare antet
df.columns = df.columns.str.strip()

# Căutare
rezultate = df.copy()
if cui:
    rezultate = rezultate[rezultate["CUI"].str.strip() == cui.strip()]
if caen:
    rezultate = rezultate[rezultate["CAEN"].str.strip() == caen.strip()]

# Afișare rezultate
if not rezultate.empty:
    st.subheader("📊 Rezultate găsite:")
    st.dataframe(rezultate)

    st.subheader("📘 Legendă coloane:")
    for cod, descriere in legenda.items():
        st.markdown(f"**{cod}**: {descriere}")
else:
    st.warning("Nicio înregistrare găsită.")
