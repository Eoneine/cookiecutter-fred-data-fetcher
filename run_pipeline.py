import argparse
from fred_data_pipeline.pipeline import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FRED data pipeline.")
    parser.add_argument(
        "--format", choices=["long", "wide"], default="long",
        help="Output shape of the saved dataset (default: long)."
    )
    parser.add_argument(
        "--series", nargs="+", default=None,
        help="FRED series IDs to fetch (default: GDP UNRATE CPIAUCSL)."
    )
    parser.add_argument(
        "--start", default=None,
        help="Start date in YYYY-MM-DD format (default: earliest available)."
    )
    parser.add_argument(
        "--end", default=None,
        help="End date in YYYY-MM-DD format (default: latest available)."
    )
    args = parser.parse_args()
    main(
        output_format=args.format,
        series_ids=args.series,
        start_date=args.start,
        end_date=args.end,
    )
