import pandas as pd
import streamlit as st

# Căile locale către fișiere
DATA_PATH = "data/web_bl_bs_sl_an2023_convertit.csv"  # datele reale

@st.cache_data(show_spinner="Se încarcă datele...")
def incarca_date():
    # Citește CSV-ul convertit cu separatorul corect
    df = pd.read_csv(DATA_PATH, sep=";", dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()
    return df

# TITLU
st.title("🔍 Căutare situații financiare 2023")

# INPUT-URI
cui  = st.text_input("Caută după CUI:")
caen = st.text_input("Caută după cod CAEN:")

# ÎNCĂRCARE DATE
df = incarca_date()

# Verifică că există coloanele obligatorii
mandatory = ["CUI", "CAEN"]
missing = [col for col in mandatory if col not in df.columns]
if missing:
    st.error(f"Lipsește coloana(e): {', '.join(missing)} din fișierul de date.")
    st.write("Coloane disponibile:", df.columns.tolist())
    st.stop()

# FILTRARE
rezultate = df
if cui:
    rezultate = rezultate[rezultate["CUI"].str.strip() == cui.strip()]
if caen:
    rezultate = rezultate[rezultate["CAEN"].str.strip() == caen.strip()]

# AFIȘARE REZULTATE
st.subheader("📄 Rezultate")
if rezultate.empty:
    st.warning("⚠️ Nicio înregistrare găsită.")
else:
    st.success(f"✅ {len(rezultate)} înregistrare(gă) găsită(e).")
    st.dataframe(rezultate, use_container_width=True)
