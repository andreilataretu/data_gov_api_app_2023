import streamlit as st
import pandas as pd

DATA_PATH = "data/web_bl_bs_sl_an2023_convertit.csv"
CSV_PATH  = "data/web_bl_bs_sl_an2023.csv"

st.set_page_config(page_title="Situații Financiare 2023", layout="wide")
st.title("🔍 Căutare după CUI & CAEN")

@st.cache_data(show_spinner="Se încarcă datele...")
def load_data():
    df = pd.read_csv(DATA_PATH, sep=None, engine="python", dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_legend():
    raw = pd.read_csv(CSV_PATH, header=None, dtype=str, encoding="utf-8")
    lines = raw.iloc[:, 0].dropna().astype(str)
    df_leg = lines.str.split(";", n=1, expand=True)
    df_leg.columns = ["explicatie", "cod"]
    df_leg["explicatie"] = df_leg["explicatie"].str.strip()
    df_leg["cod"]        = df_leg["cod"].str.strip()
    return df_leg

df   = load_data()
leg  = load_legend()

# Debug: vezi coloanele reale
st.sidebar.subheader("💡 Coloane detectate")
st.sidebar.write(df.columns.tolist())

st.sidebar.subheader("🔎 Filtre")
cui  = st.sidebar.text_input("CUI exact")
caen = st.sidebar.text_input("CAEN exact")

rez = df.copy()
if cui:
    rez = rez[rez["CUI"].str.strip() == cui.strip()]
if caen:
    rez = rez[rez["CAEN"].str.strip() == caen.strip()]

st.subheader("📋 Rezultate")
if rez.empty:
    st.warning("Nicio înregistrare găsită.")
else:
    st.success(f"{len(rez)} înregistrare găsită.")
    st.dataframe(rez, use_container_width=True)

st.subheader("📘 Legenda coloanelor")
st.dataframe(leg.set_index("cod"), use_container_width=True)
