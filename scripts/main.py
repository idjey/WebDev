import argparse
from etl_pipeline import run_pipeline, schedule_jobs
from config_manager import ConfigManager
from logging_config import setup_logging

def main(args):
    # Setup logging
    setup_logging()

    # Load and validate configuration
    config = ConfigManager(default_config_path='config.json')
    # You could validate config here if you have a function for that
    
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
