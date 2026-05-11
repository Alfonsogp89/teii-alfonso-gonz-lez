import marimo

__generated_with = "0.2.13"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import datetime as dt
    from teii.finance.timeseries import TimeSeriesFinanceClient
    return dt, mo, pd, TimeSeriesFinanceClient


@app.cell
def __(mo):
    mo.md(
        r"""
        # 📈 TEII Finance Dashboard
        Esta aplicación permite consultar datos financieros utilizando el paquete `teii.finance`.
        """
    )
    return


@app.cell
def __(mo):
    # Widgets de configuración
    ticker_input = mo.ui.text(value="IBM", label="Ticker Symbol", placeholder="e.g., IBM, AAPL")
    api_key_input = mo.ui.text(value="TEII_FINANCE_API_KEY", label="API Key (AlphaVantage)")

    query_type = mo.ui.dropdown(
        options={
            "Precios Semanales": "price",
            "Volumen Semanal": "volume",
            "Dividendos Anuales": "dividends",
            "Variación Máxima": "variation"
        },
        value="Precios Semanales",
        label="Tipo de Consulta"
    )

    mo.hstack([ticker_input, api_key_input, query_type], justify="start")
    return api_key_input, query_type, ticker_input


@app.cell
def __(dt, mo, query_type):
    # Widgets de fecha condicionales
    today = dt.date.today()
    last_year = today.replace(year=today.year - 1)

    date_range = None
    year_range = None

    if query_type.value in ["price", "volume", "variation"]:
        date_range = mo.ui.date_range(
            start=dt.date(2020, 1, 1),
            stop=today,
            value=[dt.date(2024, 1, 1), today],
            label="Rango de Fechas"
        )
        display_date = date_range
    else:
        year_range = mo.ui.range_slider(
            start=2010,
            stop=today.year,
            value=[2020, today.year],
            label="Rango de Años"
        )
        display_date = year_range

    display_date
    return date_range, display_date, last_year, today, year_range


@app.cell
def __(TimeSeriesFinanceClient, api_key_input, ticker_input):
    # Inicialización del cliente
    # Nota: El constructor hace una petición a la API
    client = None
    error_msg = None

    if ticker_input.value and api_key_input.value:
        try:
            client = TimeSeriesFinanceClient(
                ticker=ticker_input.value,
                api_key=api_key_input.value
            )
        except Exception as e:
            error_msg = str(e)

    return client, error_msg


@app.cell
def __(client, date_range, error_msg, mo, query_type, year_range):
    # Ejecución de la consulta y visualización
    if error_msg:
        result_view = mo.callout(f"Error al conectar con la API: {error_msg}", kind="error")
    elif client is None:
        result_view = mo.md("Esperando configuración...")
    else:
        try:
            if query_type.value == "price":
                data = client.weekly_price(from_date=date_range.value[0], to_date=date_range.value[1])
                title = f"Precios de Cierre Ajustados - {client._ticker}"
                # Gráfico y tabla
                result_view = mo.vstack([
                    mo.md(f"## {title}"),
                    mo.ui.chart(data.reset_index(), mark="line", x="index", y="aclose").properties(title=title),
                    mo.ui.table(data.reset_index(), label="Datos Detallados")
                ])

            elif query_type.value == "volume":
                data = client.weekly_volume(from_date=date_range.value[0], to_date=date_range.value[1])
                title = f"Volumen de Negociación - {client._ticker}"
                result_view = mo.vstack([
                    mo.md(f"## {title}"),
                    mo.ui.chart(data.reset_index(), mark="bar", x="index", y="volume").properties(title=title),
                    mo.ui.table(data.reset_index(), label="Datos Detallados")
                ])

            elif query_type.value == "dividends":
                data = client.yearly_dividends(from_year=int(year_range.value[0]), to_year=int(year_range.value[1]))
                title = f"Dividendos Anuales Sumados - {client._ticker}"
                result_view = mo.vstack([
                    mo.md(f"## {title}"),
                    mo.ui.chart(data.reset_index(), mark="bar", x="index", y="dividend").properties(title=title),
                    mo.ui.table(data.reset_index(), label="Datos Detallados")
                ])

            elif query_type.value == "variation":
                res = client.highest_weekly_variation(from_date=date_range.value[0], to_date=date_range.value[1])
                date_max, high, low, diff = res
                result_view = mo.vstack([
                    mo.md("## Variación Máxima en el Periodo"),
                    mo.stat(label="Fecha", value=str(date_max)),
                    mo.hstack([
                        mo.stat(label="Máximo", value=f"{high:.2f}"),
                        mo.stat(label="Mínimo", value=f"{low:.2f}"),
                        mo.stat(label="Diferencia", value=f"{diff:.2f}", caption="High - Low")
                    ], justify="space-around"),
                    mo.md("---"),
                    mo.md("Los datos se calculan sobre la serie completa filtrada por fechas.")
                ])
        except Exception as ex:
            result_view = mo.callout(f"Error procesando la consulta: {ex}", kind="warn")

    result_view
    return (
        date_max,
        diff,
        high,
        low,
        res,
        result_view,
    )


if __name__ == "__main__":
    app.run()
