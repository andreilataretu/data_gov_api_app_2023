import pandas as pd
import streamlit as st

# Căile locale către fișiere
DATA_PATH = "data/web_bl_bs_sl_an2023_convertit.csv"  # datele reale transformate din TXT
CSV_PATH  = "data/web_bl_bs_sl_an2023.csv"            # legenda originală

st.set_page_config(page_title="Situații Financiare 2023", layout="wide")
st.title("🔍 Caută firme după CUI & CAEN")

# === Încărcare date (în cache) ===
@st.cache_data(show_spinner="Se încarcă datele...")
def load_data():
    # autodetectăm separatorul (`,` sau `;`)
    df = pd.read_csv(DATA_PATH, sep=None, engine="python", dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()
    return df

# === Încărcare legendă (în cache) ===
@st.cache_data
def load_legend():
    # citim două coloane: explicatie + cod
    df_leg = pd.read_csv(CSV_PATH, sep=";", header=None, dtype=str, low_memory=False)
    df_leg.columns = ["explicatie", "cod"]
    # eliminăm eventuale spații
    df_leg["explicatie"] = df_leg["explicatie"].str.strip()
    df_leg["cod"]       = df_leg["cod"].str.strip()
    return df_leg

df   = load_data()
leg  = load_legend()

# === Debug: afișăm antetul detectat ===
st.sidebar.subheader("🛠 Debug antet")
st.sidebar.write(df.columns.tolist())

# === Filtre de căutare ===
st.sidebar.subheader("🔎 Filtre")
cui  = st.sidebar.text_input("CUI exact")
caen = st.sidebar.text_input("CAEN exact")

# === Aplicare filtre ===
rez = df
if cui:
    if "CUI" in rez.columns:
        rez = rez[rez["CUI"].str.strip() == cui.strip()]
    else:
        st.error("⚠️ Coloana 'CUI' nu există!")

if caen:
    if "CAEN" in rez.columns:
        rez = rez[rez["CAEN"].str.strip() == caen.strip()]
    else:
        st.error("⚠️ Coloana 'CAEN' nu există!")

# === Afișare rezultate ===
st.subheader("📋 Rezultate")
if rez.empty:
    st.warning("Nicio înregistrare găsită.")
else:
    st.success(f"{len(rez)} înregistrare găsită.")
    st.dataframe(rez, use_container_width=True)

# === Afișare legendă ===
st.subheader("📘 Legenda coloanelor")
st.dataframe(leg.set_index("cod"), use_container_width=True)
