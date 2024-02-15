import argparse
from etl_pipeline import run_pipeline, schedule_jobs, validate_config  # Assuming validate_config is properly defined
from config_manager import ConfigManager
from logging_config import setup_logging

def main(args):
    # Setup logging
    setup_logging()

    # Load configuration
    config = ConfigManager(default_config_path='config.json')

    # Validate configuration
    try:
        validate_config()  # Adjust this call according to how you've implemented config validation
        print("Configuration successfully validated.")
    except ValueError as e:
        print(f"Configuration validation error: {e}")
        return

    # Decide whether to run once or schedule based on command-line arguments
    if args.run_once:
        print("Running ETL pipeline once.")
        run_pipeline()
    else:
        print("Scheduling ETL pipeline.")
        schedule_jobs()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline Runner")
    parser.add_argument('--run-once', action='store_true',
                        help='Run the ETL pipeline once and exit. Without this flag, the ETL pipeline is scheduled to run periodically.')

    args = parser.parse_args()
    main(args)
