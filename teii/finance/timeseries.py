""" Time Series Finance Client classes """


import datetime as dt
import logging
from typing import Optional, Union

import pandas as pd

from teii.finance import FinanceClient, FinanceClientInvalidData, FinanceClientParamError


class TimeSeriesFinanceClient(FinanceClient):
    """
    Client for the AlphaVantage Time Series Weekly Adjusted API.

    Source:
        https://www.alphavantage.co/documentation/ (TIME_SERIES_WEEKLY_ADJUSTED)

    Attributes
    ----------
    _data_field2name_type : dict
        Mapping of API fields to internal names and types.
    """

    _data_field2name_type = {
        "1. open":                  ("open",     "float"),
        "2. high":                  ("high",     "float"),
        "3. low":                   ("low",      "float"),
        "4. close":                 ("close",    "float"),
        "5. adjusted close":        ("aclose",   "float"),
        "6. volume":                ("volume",   "int"),
        "7. dividend amount":       ("dividend", "float")
    }

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING) -> None:
        """
        Initialize the TimeSeriesFinanceClient.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol.
        api_key : str, optional
            The API key for the AlphaVantage API.
        logging_level : int or str, optional
            The logging level.
        """

        super().__init__(ticker, api_key, logging_level)

        self._build_data_frame()

    def _build_data_frame(self) -> None:
        """
        Build and format the pandas DataFrame from JSON data.

        Raises
        ------
        FinanceClientInvalidData
            If the DataFrame cannot be built or formatted.
        """

        try:
            # Build Panda's data frame
            data_frame = pd.DataFrame.from_dict(self._json_data, orient='index', dtype='float')

            # Rename data fields
            data_frame = data_frame.rename(columns={key: name_type[0]
                                                    for key, name_type in self._data_field2name_type.items()})

            # Set data field types
            data_frame = data_frame.astype(dtype={name_type[0]: name_type[1]
                                                  for key, name_type in self._data_field2name_type.items()})

            # Set index type
            data_frame.index = data_frame.index.astype("datetime64[ns]")
        except Exception as e:
            logging.error(f"Error building DataFrame: {e}")
            raise FinanceClientInvalidData("Failed to build or format financial data frame.")

        # Sort data
        self._data_frame = data_frame.sort_index(ascending=True)

    def _build_base_query_url_params(self) -> str:
        """
        Return the query URL parameters for the Time Series Weekly Adjusted API.

        Returns
        -------
        str
            The query parameters.
        """

        return f"function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={self._ticker}&outputsize=full&apikey={self._api_key}"

    @classmethod
    def _build_query_data_key(cls) -> str:
        """
        Return the data query key for the Time Series Weekly Adjusted API.

        Returns
        -------
        str
            The data key.
        """

        return "Weekly Adjusted Time Series"

    def _validate_query_data(self) -> None:
        """
        Validate the query data metadata.

        Raises
        ------
        FinanceClientInvalidData
            If the metadata is invalid or missing.
        """

        try:
            assert self._json_metadata["2. Symbol"] == self._ticker
        except Exception as e:
            raise FinanceClientInvalidData("Metadata field '2. Symbol' not found") from e
        else:
            self._logger.info(f"Metadata key '2. Symbol' = '{self._ticker}' found")

    def weekly_price(self,
                     from_date: Optional[dt.date] = None,
                     to_date: Optional[dt.date] = None) -> pd.Series:
        """
        Return weekly adjusted close price series.

        Parameters
        ----------
        from_date : dt.date, optional
            The start date for the series.
        to_date : dt.date, optional
            The end date for the series.

        Returns
        -------
        pd.Series
            The series of weekly adjusted close prices.

        Raises
        ------
        FinanceClientParamError
            If from_date is greater than to_date.
        """

        assert self._data_frame is not None

        series = self._data_frame['aclose']

        if from_date is not None and to_date is not None and from_date > to_date:
            raise FinanceClientParamError("'from_date' must be less than or equal to 'to_date'")

        # FIXME: type hint error
        if from_date is not None and to_date is not None:
            series = series.loc[pd.Timestamp(from_date):pd.Timestamp(to_date)]   # type: ignore

        return series

    def weekly_volume(self,
                      from_date: Optional[dt.date] = None,
                      to_date: Optional[dt.date] = None) -> pd.Series:
        """
        Return weekly volume series.

        Parameters
        ----------
        from_date : dt.date, optional
            The start date for the series.
        to_date : dt.date, optional
            The end date for the series.

        Returns
        -------
        pd.Series
            The series of weekly volumes.

        Raises
        ------
        FinanceClientParamError
            If from_date is greater than to_date.
        """

        assert self._data_frame is not None

        series = self._data_frame['volume']

        if from_date is not None and to_date is not None and from_date > to_date:
            raise FinanceClientParamError("'from_date' must be less than or equal to 'to_date'")

        # FIXME: type hint error
        if from_date is not None and to_date is not None:
            series = series.loc[pd.Timestamp(from_date):pd.Timestamp(to_date)]   # type: ignore

        return series

    def yearly_dividends(self,
                         from_year: Optional[int] = None,
                         to_year: Optional[int] = None) -> pd.Series:
        """
        Return yearly dividends series.

        Parameters
        ----------
        from_year : int, optional
            The start year for the series.
        to_year : int, optional
            The end year for the series.

        Returns
        -------
        pd.Series
            The series of yearly dividends sums.

        Raises
        ------
        FinanceClientParamError
            If from_year is greater than to_year.
        """

        assert self._data_frame is not None

        series = self._data_frame['dividend']

        if from_year is not None and to_year is not None and from_year > to_year:
            raise FinanceClientParamError("'from_year' must be less than or equal to 'to_year'")

        # FIXME: type hint error
        if from_year is not None and to_year is not None:
            series = series.loc[str(from_year):str(to_year)]   # type: ignore
        elif from_year is not None:
            series = series.loc[str(from_year):]               # type: ignore
        elif to_year is not None:
            series = series.loc[:str(to_year)]                 # type: ignore

        return series.resample('YE').sum()

    def highest_weekly_variation(self,
                                 from_date: Optional[dt.date] = None,
                                 to_date: Optional[dt.date] = None) -> tuple:
        """
        Return the highest weekly variation (high - low).

        Parameters
        ----------
        from_date : dt.date, optional
            The start date for the period.
        to_date : dt.date, optional
            The end date for the period.

        Returns
        -------
        tuple
            A tuple containing (date, high, low, difference) for the week with maximum variation.

        Raises
        ------
        FinanceClientParamError
            If from_date is greater than to_date.
        """

        assert self._data_frame is not None

        df = self._data_frame[['high', 'low']].copy()

        if from_date is not None and to_date is not None and from_date > to_date:
            raise FinanceClientParamError("'from_date' must be less than or equal to 'to_date'")

        # FIXME: type hint error
        if from_date is not None and to_date is not None:
            df = df.loc[pd.Timestamp(from_date):pd.Timestamp(to_date)]   # type: ignore

        df['variation'] = df['high'] - df['low']

        # Find the row with the maximum variation
        max_idx = df['variation'].idxmax()
        max_row = df.loc[max_idx]

        return (max_idx.date(), float(max_row['high']), float(max_row['low']), float(max_row['variation']))
