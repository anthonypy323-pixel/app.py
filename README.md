# ESP32 Monitor

Monitor en tiempo real de temperatura y humedad usando:

- ESP32
- Google Sheets
- Streamlit
- Python

## Datos

Los datos son enviados automáticamente desde el ESP32 a Google Sheets.

## Dashboard

La aplicación muestra:

- Temperatura en tiempo real
- Humedad en tiempo real
- Actualización automática

## Tecnologías

- Python
- Streamlit
- Pandas
- Matplotlib

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
    (df["humedad"] >= 0) & (df["humedad"] <= 100)
]

df["temperatura_suave"] = df["temperatura"].rolling(window=5).mean()
df["humedad_suave"] = df["humedad"].rolling(window=5).mean()

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(df["fecha"], df["temperatura_suave"], label="Temperatura °C")
ax.plot(df["fecha"], df["humedad_suave"], label="Humedad %")

ax.legend()
ax.grid(True)

st.pyplot(fig)
