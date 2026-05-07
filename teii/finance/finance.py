""" Finance Client classes """


import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import requests

from teii.finance import (FinanceClientAPIError, FinanceClientInvalidAPIKey,
                          FinanceClientInvalidData, FinanceClientIOError)


class FinanceClient(ABC):
    """
    Abstract base class for finance API clients.

    Attributes
    ----------
    _FinanceBaseQueryURL : str
        Base URL for the finance API.
    """

    _FinanceBaseQueryURL = "https://www.alphavantage.co/query?"  # Class variable

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING,
                 logging_file: Optional[str] = None) -> None:
        """
        Initialize the FinanceClient.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol.
        api_key : str, optional
            The API key for the finance API. If not provided, it will be read from
            the TEII_FINANCE_API_KEY environment variable.
        logging_level : int or str, optional
            The logging level (default is logging.WARNING).
        logging_file : str, optional
            The file to write logs to.

        Raises
        ------
        FinanceClientInvalidAPIKey
            If the API key is not provided or is invalid.
        FinanceClientAPIError
            If the API request fails.
        FinanceClientInvalidData
            If the API response data is invalid.
        """

        self._ticker: str = ticker
        self._api_key: Optional[str] = api_key

        # Logging configuration
        self._setup_logging(logging_level, logging_file)

        # Finance API key configuration
        self._logger.info("API key configuration")
        if self._api_key is None:
            self._api_key = os.getenv("TEII_FINANCE_API_KEY")
        if self._api_key is None or not isinstance(self._api_key, str):
            self._logger.critical("API key is not available or invalid.")
            raise FinanceClientInvalidAPIKey(f"{self.__class__.__qualname__} operation failed")

        # Query Finance API
        self._logger.info("Finance API access...")
        response = self._query_api()

        # Process query response
        self._logger.info("Finance API query response processing...")
        self._process_query_response(response)

        # Validate query data
        self._logger.info("Finance API query data validation...")
        self._validate_query_data()

        # Panda's Data Frame
        self._data_frame: Optional[pd.DataFrame] = None

    def _setup_logging(self,
                       logging_level: Union[int, str],
                       logging_file: Optional[str]) -> None:
        """
        Set up logging configuration.

        Parameters
        ----------
        logging_level : int or str
            The logging level.
        logging_file : str, optional
            The file to write logs to.
        """

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging_level)

        # Avoid adding multiple handlers if already configured
        if not self._logger.handlers:
            handler: Union[logging.StreamHandler, logging.FileHandler] = logging.StreamHandler()
            if logging_file:
                handler = logging.FileHandler(logging_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    @classmethod
    def _build_base_query_url(cls) -> str:
        """
        Return base query URL.

        Returns
        -------
        str
            The base query URL.
        """

        return cls._FinanceBaseQueryURL

    @abstractmethod
    def _build_base_query_url_params(self) -> str:
        """
        Return base query URL parameters.

        Returns
        -------
        str
            The query parameters.
        """

        pass  # pragma: nocover

    def _query_api(self) -> requests.Response:
        """
        Query the API endpoint.

        Returns
        -------
        requests.Response
            The response from the API.

        Raises
        ------
        FinanceClientAPIError
            If the API request is unsuccessful.
        """

        try:
            url = self.__class__._build_base_query_url()
            params = self._build_base_query_url_params()
            response = requests.get(f"{url}{params}")
            assert response.status_code == 200
        except Exception as e:
            self._logger.error("Failed to query the API endpoint.")
            raise FinanceClientAPIError("Unsuccessful API access") from e
        else:
            self._logger.info("Successful API access "
                              f"[URL: {response.url}, status: {response.status_code}]")
        return response

    @classmethod
    def _build_query_metadata_key(cls) -> str:
        """
        Return the metadata query key.

        Returns
        -------
        str
            The metadata key.
        """

        return "Meta Data"

    @classmethod
    @abstractmethod
    def _build_query_data_key(cls) -> str:
        """
        Return the data query key.

        Returns
        -------
        str
            The data key.
        """

        pass  # pragma: nocover

    def _process_query_response(self, response: requests.Response) -> None:
        """
        Preprocess query data from the API response.

        Parameters
        ----------
        response : requests.Response
            The response from the API.

        Raises
        ------
        FinanceClientInvalidData
            If the response data cannot be processed.
        """

        try:
            json_data_downloaded = response.json()
            self._json_metadata = json_data_downloaded[self._build_query_metadata_key()]
            self._json_data = json_data_downloaded[self._build_query_data_key()]
        except Exception as e:
            self._logger.error("Error processing query response")
            self._logger.debug(f"Response content: '{response.text}'")
            raise FinanceClientInvalidData("Invalid data") from e
        else:
            self._logger.info("Metadata and data fields found")

        self._logger.info(f"Metadata: '{self._json_metadata}'")
        self._logger.info(f"Data: '{json.dumps(self._json_data)[0:218]}...'")

    @abstractmethod
    def _validate_query_data(self) -> None:
        """
        Validate the query data.
        """

        pass  # pragma: nocover

    def to_pandas(self) -> pd.DataFrame:
        """
        Return the data as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            The processed finance data.
        """

        assert self._data_frame is not None

        return self._data_frame

    def to_csv(self, path2file: Path) -> Path:
        """
        Write the data to a CSV file.

        Parameters
        ----------
        path2file : Path
            The path to the CSV file.

        Returns
        -------
        Path
            The path to the created CSV file.

        Raises
        ------
        FinanceClientIOError
            If the file cannot be written.
        """

        assert self._data_frame is not None

        try:
            self._data_frame.to_csv(path2file)
        except (IOError, PermissionError) as e:
            raise FinanceClientIOError(f"Unable to write json data into file '{path2file}'") from e

        return path2file
