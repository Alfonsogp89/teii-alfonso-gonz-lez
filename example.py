""" Ejemplo de uso del paquete teii. """


import datetime as dt
import logging

import matplotlib.pyplot as plt

import teii.finance as tf


def setup_logging(logging_level):
    """ Crea y configura logger. """

    logging.basicConfig(filename='example.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)
    logger.info("Logger creado")

    return logger


def plot(pandas_series, ticker, logger):
    """ Dibuja una gráfica a partir de la serie de Pandas. """

    logger.info("Dibujando gráfica...")

    pandas_series.plot(xlabel='Fecha', ylabel='Precio en USD', title=f"Evolución del Precio de {ticker}")
    plt.show()  # ¡Necesario para que se muestre la gráfica en una ventana!


def main():
    """ Muestra como usar teii-finance. """

    logger = setup_logging(logging.DEBUG)

    logger.info("Inicio")

    # Define ticker y API key
    ticker = 'IBM'
    my_alpha_vantage_api_key = 'KPCY3YFXA24HEJSY'
    # Sólo funcionará con IBM (para demos). Obtener un API key real de:
    # https://www.alphavantage.co/support/#api-key
    # (Pero hay fuertes limitaciones de uso diario: no más de 1 llamada por segundo,
    # 5 llamadas por minuto y 25 llamadas por día)

    # Crea cliente
    try:
        tf_client = tf.TimeSeriesFinanceClient(ticker,
                                               my_alpha_vantage_api_key,
                                               logging_level=logging.DEBUG)
    # Captura y muestra todas las excepciones
    except Exception as e:
        logger.error(f"{e}", exc_info=False)
    # Usa el cliente
    else:
        # Genera una serie de Pandas con precio de cierre semanal filtrada para el año 2026
        pd_series = tf_client.weekly_price(from_date=dt.date(2026, 1, 1),
                                           to_date=dt.date(2026, 12, 31))

        logger.info(pd_series)

        # Dibuja una gráfica a partir de la serie de Pandas
        plot(pd_series, ticker, logger)
    finally:
        logger.info("Fin")


if __name__ == "__main__":
    main()
