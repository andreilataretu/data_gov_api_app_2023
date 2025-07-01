import streamlit as st
import pandas as pd

# --- CONFIGURARE LINKURI ---
TXT_URL = "https://data.gov.ro/dataset/7861a98f-4d5c-4faa-90d4-8e934ebd1782/resource/5ed47b6f-f8a2-4ca8-a272-692aff4fe9e4/download/web_bl_bs_sl_an2023.txt"
CSV_LEGEND_URL = "https://data.gov.ro/dataset/7861a98f-4d5c-4faa-90d4-8e934ebd1782/resource/2de79441-0db1-468d-9e7e-ebc9b0f3ff17/download/web_bl_bs_sl_an2023.csv"

st.set_page_config(page_title="Situații Financiare 2023", layout="wide")
st.title("🔍 Situații Financiare 2023 – Căutare după CUI, Denumire, CAEN")

# --- CĂRȚILE DE DATE ---
@st.cache_data(show_spinner=True)
def incarca_date_si_legenda():
    df_data = pd.read_csv(TXT_URL, sep=";", dtype=str, low_memory=False)

    # Prelucrăm legenda (coloană unică)
    df_raw = pd.read_csv(CSV_LEGEND_URL, header=None, names=["linie"], encoding="utf-8")
    df_legend_split = df_raw["linie"].str.split(";", n=1, expand=True)
    df_legend_split.columns = ["explicatie", "cod"]
    legend_dict = dict(zip(df_legend_split["cod"].str.strip(), df_legend_split["explicatie"].str.strip()))

    return df_data, legend_dict

df_data, legend_dict = incarca_date_si_legenda()

# --- INTERFAȚĂ CĂUTARE ---
with st.sidebar:
    st.subheader("🔎 Filtre de căutare")
    cui = st.text_input("Cod fiscal (CUI)").strip()
    denumire = st.text_input("Denumire firmă").strip().lower()
    caen = st.text_input("Cod CAEN").strip()

# --- APLICĂ FILTRE ---
rezultate = df_data.copy()

if cui:
    rezultate = rezultate[rezultate["CUI"].str.strip() == cui]

if denumire:
    rezultate = rezultate[rezultate["Denumire entitate"].str.lower().str.contains(denumire, na=False)]

if caen:
    rezultate = rezultate[rezultate["CAEN"].str.strip() == caen]

# --- AFIȘARE ---
st.markdown("## 📄 Rezultate")
if rezultate.empty:
    st.warning("⚠️ Nicio înregistrare găsită.")
else:
    st.success(f"✅ {len(rezultate)} înregistrare(gă) găsite.")
    st.dataframe(rezultate, use_container_width=True)

# --- LEGENDA ---
with st.expander("📘 Legenda coloanelor disponibile în fișier"):
    df_legenda = pd.DataFrame(list(legend_dict.items()), columns=["Cod coloană", "Semnificație"])
    st.dataframe(df_legenda, use_container_width=True)
