import schedule
import time
import logging
from database import Database
from arxiv_fetcher import ArxivFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperTracker:
    def __init__(self, topics=None):
        self.topics = topics or ['cs.AI', 'cs.CL', 'cs.LG']  # Default topics
        self.db = Database()
        self.fetcher = ArxivFetcher()
    
    def update_papers(self):
        """
        Fetch and store new papers for all topics
        """
        logger.info("Starting paper update...")
        for topic in self.topics:
            papers = self.fetcher.fetch_papers(topic)
            for paper in papers:
                if self.db.add_paper(**paper):
                    logger.info(f"Added new paper: {paper['title']}")
        
        logger.info("Paper update completed")
    
    def run_scheduled_updates(self, interval_hours=24):
        """
        Run updates at regular intervals
        """
        schedule.every(interval_hours).hours.do(self.update_papers)
        
        # Run initial update
        self.update_papers()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    tracker = PaperTracker([
        'cs.AI',    # Artificial Intelligence
        'cs.CL',    # Computation and Language
        'cs.LG',    # Machine Learning
        'cs.CV',    # Computer Vision
        'cs.NE'     # Neural and Evolutionary Computing
    ])
    
    try:
        tracker.run_scheduled_updates()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        tracker.close() 