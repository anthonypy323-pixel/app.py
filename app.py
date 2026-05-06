import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQeZT4gUHYSv3GYZQLKRK0PN3uxfNppGJ8m1QrywlS86WJ-3z6d6toA-nWIF6g2mbsaThrIBYlOnaon/pub?output=csv"

st.set_page_config(page_title="ESP32 Monitor", layout="wide")

st.title("🌡️ ESP32 Monitor")
st.subheader("Temperatura y humedad en tiempo real")

df = pd.read_csv(url, header=None, engine="python", on_bad_lines="skip")

df = df.iloc[:, 0:3]
df.columns = ["fecha", "temperatura", "humedad"]

df["fecha"] = pd.to_datetime(
    df["fecha"].astype(str).str.strip(),
    format="%d/%m/%Y %H:%M:%S",
    errors="coerce"
)

df["temperatura"] = pd.to_numeric(df["temperatura"], errors="coerce")
df["humedad"] = pd.to_numeric(df["humedad"], errors="coerce")

df = df.dropna(subset=["fecha", "temperatura", "humedad"])

df = df[
    (df["temperatura"] >= 5) & (df["temperatura"] <= 35) &
    (df["humedad"] >= 0) & (df["humedad"] <= 100)
]

df = df.sort_values("fecha")

ultimo_dia = df["fecha"].max().date()
df = df[df["fecha"].dt.date == ultimo_dia]

df["temperatura_suave"] = df["temperatura"].rolling(window=5).mean()
df["humedad_suave"] = df["humedad"].rolling(window=5).mean()

st.write(f"📅 Día mostrado: **{ultimo_dia}**")
st.write(f"📊 Filas válidas: **{len(df)}**")

col1, col2 = st.columns(2)

with col1:
    st.metric("Temperatura actual", f"{df['temperatura'].iloc[-1]:.2f} °C")

with col2:
    st.metric("Humedad actual", f"{df['humedad'].iloc[-1]:.2f} %")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df["fecha"], df["temperatura_suave"], label="Temperatura (°C)")
ax.plot(df["fecha"], df["humedad_suave"], label="Humedad (%)")

ax.set_xlabel("Hora")
ax.set_ylabel("Valor")
ax.set_title(f"Temperatura y humedad ESP32 - {ultimo_dia}")
ax.legend()
ax.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.subheader("Últimos datos")
st.dataframe(df.tail(20))