import schedule
import time
import logging
import argparse
from database import Database
from arxiv_fetcher import ArxivFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperTracker:
    def __init__(self, keywords):
        self.keywords = keywords
        self.db = Database()
        self.fetcher = ArxivFetcher()
    
    def update_papers(self):
        logger.info("Starting paper update...")
        for keyword in self.keywords:
            papers = self.fetcher.fetch_papers([keyword])
            for paper in papers:
                if self.db.add_paper(**paper):
                    logger.info(f"Added new paper: {paper['title']}")
        
        logger.info("Paper update completed")
    
    def run_scheduled_updates(self, interval_hours=24):
        schedule.every(interval_hours).hours.do(self.update_papers)
        self.update_papers()
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def close(self):
        self.db.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Track academic papers based on keywords')
    parser.add_argument('--keywords', '-k', nargs='+', required=True,
                      help='List of keywords to search for (e.g., "llm evaluation" "reinforcement learning")')
    parser.add_argument('--interval', '-i', type=int, default=24,
                      help='Update interval in hours (default: 24)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    tracker = PaperTracker(args.keywords)
    
    try:
        logger.info(f"Starting paper tracker with keywords: {args.keywords}")
        tracker.run_scheduled_updates(interval_hours=args.interval)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        tracker.close() 