import streamlit as st
import pandas as pd

# Căile locale către fișiere
DATA_PATH = "data/web_bl_bs_sl_an2023_convertit.csv"  # datele reale
CSV_PATH  = "data/web_bl_bs_sl_an2023.csv"            # legenda

st.set_page_config(page_title="Situații Financiare 2023", layout="wide")
st.title("🔍 Căutare situații financiare 2023")

# --- Încărcare date ---
@st.cache_data(show_spinner="Se încarcă datele…")
def load_data():
    # Citim CSV-ul convertit cu separatorul corect
    df = pd.read_csv(DATA_PATH, sep=";", dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()
    return df

# --- Încărcare legendă ---
@st.cache_data
def load_legend():
    raw = pd.read_csv(CSV_PATH, header=None, dtype=str, encoding="utf-8")
    lines = raw.iloc[:, 0].dropna().astype(str)
    df_leg = lines.str.split(";", n=1, expand=True)
    df_leg.columns = ["explicatie", "cod"]
    df_leg["explicatie"] = df_leg["explicatie"].str.strip()
    df_leg["cod"]        = df_leg["cod"].str.strip()
    return df_leg

# Rulează încărcările
df   = load_data()
leg  = load_legend()

# --- Debug: afișează antetul detectat (în sidebar) ---
st.sidebar.subheader("💡 Coloane detectate")
st.sidebar.write(df.columns.tolist())

# --- Filtre de căutare ---
st.sidebar.subheader("🔎 Filtre")
cui  = st.sidebar.text_input("CUI (exact)")
caen = st.sidebar.text_input("CAEN (exact)")

rez = df.copy()
if cui:
    if "CUI" in rez.columns:
        rez = rez[rez["CUI"].str.strip() == cui.strip()]
    else:
        st.sidebar.error("⚠️ Coloana 'CUI' nu există!")

if caen:
    if "CAEN" in rez.columns:
        rez = rez[rez["CAEN"].str.strip() == caen.strip()]
    else:
        st.sidebar.error("⚠️ Coloana 'CAEN' nu există!")

# --- Afișare rezultate ---
st.subheader("📋 Rezultate")
if rez.empty:
    st.warning("Nicio înregistrare găsită.")
else:
    st.success(f"{len(rez)} înregistrare găsită.")
    st.dataframe(rez, use_container_width=True)

# --- Afișare legendă ---
st.subheader("📘 Legenda coloanelor")
st.dataframe(leg.set_index("cod"), use_container_width=True)
