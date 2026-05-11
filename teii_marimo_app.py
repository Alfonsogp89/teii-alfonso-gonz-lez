import marimo

__generated_with = "0.2.13"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import requests
    import json
    return json, mo, pd, requests


@app.cell
def __(mo):
    mo.md(
        """
        # 🌦️ Open-Meteo Dashboard
        Esta aplicación es un dashboard interactivo construido con **Marimo**.
        Consume datos meteorológicos de la API pública [Open-Meteo](https://open-meteo.com/),
        y los procesa con **pandas** para visualizarlos.

        Demuestra los fundamentos de cuadernos reactivos, uso de librerías gráficas integradas
        en Marimo (`mo.ui.chart`) y acceso a APIs HTTP.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## ⚙️ Configuración de Datos")
    return


@app.cell
def __(mo):
    # Selector de origen de datos
    data_source = mo.ui.radio(
        options={
            "API Pública (Open-Meteo)": "api",
            "Datos Locales Predescargados": "local"
        },
        value="API Pública (Open-Meteo)",
        label="Origen de los datos"
    )

    # Selector de variable meteorológica
    weather_variable = mo.ui.dropdown(
        options={
            "Temperatura (°C)": "temperature_2m",
            "Precipitación (mm)": "precipitation"
        },
        value="Temperatura (°C)",
        label="Variable a mostrar"
    )

    mo.hstack([data_source, weather_variable], justify="start")
    return data_source, weather_variable


@app.cell
def __(data_source, json, mo, requests):
    # Recuperación de los datos
    raw_data = None
    error_msg = None

    try:
        if data_source.value == "api":
            # Coordenadas de Madrid como ejemplo
            url = (
                "https://api.open-meteo.com/v1/forecast?latitude=40.4165"
                "&longitude=-3.7026&hourly=temperature_2m,precipitation&timezone=Europe%2FMadrid"
            )
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            raw_data = response.json()
        else:
            # Uso de archivo local
            with open("madrid_weather.json", "r") as f:
                raw_data = json.load(f)
    except Exception as e:
        error_msg = str(e)

    if error_msg:
        mo.callout(f"Error al cargar los datos: {error_msg}", kind="error")
    else:
        mo.callout(f"Datos cargados exitosamente desde: **{data_source.value}**", kind="success")
    return error_msg, raw_data, response, url


@app.cell
def __(error_msg, pd, raw_data):
    # Procesamiento con pandas
    df = None
    if not error_msg and raw_data:
        # Extraemos los campos horarios
        hourly_data = raw_data.get("hourly", {})

        if hourly_data:
            df = pd.DataFrame(hourly_data)
            # Convertimos la columna de tiempo a datetime
            df["time"] = pd.to_datetime(df["time"])
    return df, hourly_data


@app.cell
def __(df, mo, weather_variable):
    # Visualización
    if df is not None:
        title = f"Pronóstico: {weather_variable.label}"

        # Color según variable
        color = "#ff7f0e" if weather_variable.value == "temperature_2m" else "#1f77b4"

        # Gráfico reactivo (Marimo usa Altair por debajo)
        chart = mo.ui.chart(
            df,
            mark="line",
            x="time",
            y=weather_variable.value
        ).properties(title=title)

        # Tabla interactiva
        table = mo.ui.table(df[["time", weather_variable.value]], pagination=True)

        # Mostrar ambos verticalmente
        display = mo.vstack([
            mo.md("### Gráfico Evolutivo"),
            chart,
            mo.md("### Datos Detallados"),
            table
        ])
    else:
        display = mo.md("Esperando datos...")

    display
    return chart, color, display, table, title


if __name__ == "__main__":
    app.run()
