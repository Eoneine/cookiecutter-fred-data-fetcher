import time
import requests
import pandas as pd
from fred_data_pipeline.config import FRED_BASE_URL

class FREDClient:
    def __init__(self, api_key: str):
        """
        Initialize the FRED client.

        Args:
            api_key (str): The API key for FRED API authentication.
        """
        self.api_key = api_key
        self.api_url = FRED_BASE_URL

    def fetch_series(self, series_id: str, start_date: str = None,
                      end_date: str = None) -> pd.DataFrame:
        """
        Fetch data for a specific FRED series.

        Args:
            series_id (str): The FRED series ID to fetch (e.g., 'GDP').
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to None.
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the observation dates and values for the series.
        """
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }
        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date

        try:
            response = requests.get(self.api_url, params=params, timeout=20)
        except requests.exceptions.RequestException:
            print(f"Request failed for {series_id}, retrying in 3s...")
            time.sleep(3)
            response = requests.get(self.api_url, params=params, timeout=20)

        if response.status_code != 200:
            print(f"Failed to fetch data for {series_id}. "
                  f"Status: {response.status_code}")
            return pd.DataFrame()

        observations = response.json()["observations"]
        data = [
            {"date": obs["date"], "value": obs["value"], "series_id": series_id}
            for obs in observations
        ]
        return pd.DataFrame(data)
