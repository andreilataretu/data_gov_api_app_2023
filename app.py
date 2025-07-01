import pandas as pd
import streamlit as st

# Link către fișierul CSV cu datele din 2023
CSV_URL = "https://data.gov.ro/dataset/7861a98f-4d5c-4faa-90d4-8e934ebd1782/resource/2de79441-0db1-468d-9e7e-ebc9b0f3ff17/download/web_bl_bs_sl_an2023.csv"

# Dimensiunea pentru citire eficientă (evită blocajele)
CHUNKSIZE = 10000

# Configurare pagină
st.set_page_config(page_title="Situații financiare 2023", layout="wide")
st.title("🔍 Situații financiare 2023 - căutare după CUI, firmă, CAEN")

st.markdown("""
Caută date financiare folosind unul sau mai multe filtre:
- **CUI** (Cod Fiscal)
- **Denumire firmă** (sau fragment)
- **Cod CAEN** (exact)
""")

# Câmpuri de căutare
cif_search = st.text_input("Cod Fiscal (CUI):")
den_search = st.text_input("Denumire firmă (sau parte din ea):")
caen_search = st.text_input("Cod CAEN:")

# Funcție pentru citirea cu filtrare
@st.cache_data(show_spinner="Se caută în fișier...")
def search_csv(url, cif=None, denumire=None, caen=None):
    results = []
    for chunk in pd.read_csv(url, sep=";", chunksize=CHUNKSIZE, dtype=str, low_memory=False):
        chunk = chunk.fillna("")

        if cif:
            chunk = chunk[chunk["CUI"].str.strip() == cif.strip()]
        if denumire:
            chunk = chunk[chunk["Denumire entitate"].str.contains(denumire.strip(), case=False, na=False)]
        if caen:
            chunk = chunk[chunk["CAEN"].str.strip() == caen.strip()]

        if not chunk.empty:
            results.append(chunk)

    if results:
        return pd.concat(results, ignore_index=True)
    else:
        return pd.DataFrame()

# Buton căutare
if st.button("🔎 Caută"):
    results = search_csv(CSV_URL, cif=cif_search, denumire=den_search, caen=caen_search)

    if not results.empty:
        st.success(f"✅ {len(results)} înregistrări găsite.")
        st.dataframe(results, use_container_width=True)
    else:
        st.warning("⚠️ Nicio înregistrare găsită.")
else:
    st.info("🔹 Introdu un criteriu de căutare și apasă 'Caută'.")

