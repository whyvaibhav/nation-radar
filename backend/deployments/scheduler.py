#!/usr/bin/env python3
"""
24/7 Scheduler for Crestal Tweet Monitoring
Runs the pipeline at regular intervals
"""

import schedule
import time
import subprocess
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    """Execute the Crestal monitoring pipeline"""
    try:
        logging.info("🚀 Starting Crestal pipeline run...")
        
        result = subprocess.run([sys.executable, 'run_pipeline.py'], 
                              capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            logging.info("✅ Pipeline completed successfully")
            logging.info(f"Output: {result.stdout[:200]}...")  # First 200 chars
        else:
            logging.error(f"❌ Pipeline failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logging.error("⏰ Pipeline timed out after 10 minutes")
    except Exception as e:
        logging.error(f"💥 Unexpected error: {e}")

def main():
    """Main scheduler loop"""
    logging.info("🎯 Starting 24/7 Crestal Monitor Scheduler")
    
    # Schedule options - choose one:
    
    # Option 1: Every hour
    schedule.every().hour.do(run_pipeline)
    
    # Option 2: Every 30 minutes
    # schedule.every(30).minutes.do(run_pipeline)
    
    # Option 3: Every 4 hours
    # schedule.every(4).hours.do(run_pipeline)
    
    # Option 4: Specific times daily
    # schedule.every().day.at("09:00").do(run_pipeline)
    # schedule.every().day.at("15:00").do(run_pipeline)
    # schedule.every().day.at("21:00").do(run_pipeline)
    
    logging.info("📅 Scheduler configured - running every hour")
    logging.info("Press Ctrl+C to stop")
    
    # Run once immediately
    run_pipeline()
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logging.info("🛑 Scheduler stopped by user")

if __name__ == "__main__":
    main()
