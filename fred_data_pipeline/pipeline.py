from typing import List, Optional
import pandas as pd
from fred_data_pipeline.config import (
    FRED_API_KEY, SERIES_IDS, PROCESSED_DATA_DIR, OUTPUT_FORMAT
)
from fred_data_pipeline.dataset import FREDClient
from fred_data_pipeline.features import clean_data, reshape_data

def main(output_format: str = OUTPUT_FORMAT,
         series_ids: Optional[List[str]] = None,
         start_date: Optional[str] = None,
         end_date: Optional[str] = None):
    """
    Run the full data pipeline: fetch data, clean it, reshape it, and save to CSV.

    Args:
        output_format (str): The shape of the output data, either 'long' or 'wide'.
        series_ids (list[str], optional): FRED series IDs to fetch. Defaults to config.SERIES_IDS.
        start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to None (all history).
        end_date (str, optional): End date in YYYY-MM-DD format. Defaults to None (latest available).
    """
    if series_ids is None:
        series_ids = SERIES_IDS

    client = FREDClient(FRED_API_KEY)

    all_tables = []
    for series_id in series_ids:
        table = client.fetch_series(series_id, start_date=start_date, end_date=end_date)
        print(f"Series '{series_id}': {len(table)} rows")
        all_tables.append(table)

    df_combined = pd.concat(all_tables, ignore_index=True)
    df_clean = clean_data(df_combined)
    df_output = reshape_data(df_clean, output_format=output_format)

    # Ensure processed directory exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Build descriptive filename
    series_part = "_".join(series_ids)
    date_part = ""
    if start_date and end_date:
        date_part = f"_{start_date}_to_{end_date}"
    elif start_date:
        date_part = f"_{start_date}_to_latest"
    elif end_date:
        date_part = f"_earliest_to_{end_date}"

    output_path = PROCESSED_DATA_DIR / f"dataset_fred_{series_part}{date_part}_{output_format}.csv"
    df_output.to_csv(output_path, index=False)

    print(f"\nRows before cleaning: {len(df_combined)}")
    print(f"Rows after cleaning : {len(df_clean)}")
    print(f"Output format        : {output_format}")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
