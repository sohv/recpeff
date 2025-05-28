import schedule
import time
import logging
import argparse
from arxiv_fetcher import ArxivFetcher
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PaperAlerts:
    def __init__(self, keywords):
        self.keywords = keywords
        self.fetcher = ArxivFetcher()
        self.last_check = datetime.now() - timedelta(days=1)  # track last check time
    
    def check_papers(self):
        logger.info("Starting paper check...")
        current_time = datetime.now()
        
        for keyword in self.keywords:
            papers = self.fetcher.fetch_papers([keyword])
            for paper in papers:
                if paper['published_date'] > self.last_check:
                    self.send_alert(paper)
        
        self.last_check = current_time
        logger.info("Paper check completed")
    
    def send_alert(self, paper):
        alert_message = f"""
New Paper Alert!
Title: {paper['title']}
Authors: {paper['authors']}
Published: {paper['published_date']}
PDF: {paper['pdf_url']}
Abstract: {paper['abstract'][:200]}...
"""
        logger.info(alert_message)
        # add code to send alerts via email
    
    def run_scheduled_checks(self, interval_hours=24):
        schedule.every(interval_hours).hours.do(self.check_papers)
        
        self.check_papers()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Get alerts for new academic papers')
    parser.add_argument('--keywords', '-k', nargs='+', required=True,
                      help='List of keywords to search for (e.g., "llm evaluation" "reinforcement learning")')
    parser.add_argument('--interval', '-i', type=int, default=24,
                      help='Check interval in hours (default: 24)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    alerts = PaperAlerts(args.keywords)
    
    try:
        logger.info(f"Starting paper alerts with keywords: {args.keywords}")
        alerts.run_scheduled_checks(interval_hours=args.interval)
    except KeyboardInterrupt:
        logger.info("Shutting down...") 