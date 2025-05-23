import arxiv
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArxivFetcher:
    def __init__(self, max_results=100):
        self.max_results = max_results
        self.client = arxiv.Client()
    
    def fetch_papers(self, topic, days_back=7):
        """
        Fetch papers from arXiv for a given topic within the last N days
        """
        try:
            # Calculate the date N days ago
            date_threshold = datetime.now() - timedelta(days=days_back)
            
            # Construct the search query
            search = arxiv.Search(
                query=f"cat:{topic}",
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = []
            for result in self.client.results(search):
                # Convert arXiv date to datetime
                published_date = result.published.replace(tzinfo=None)
                
                # Skip papers older than our threshold
                if published_date < date_threshold:
                    continue
                
                paper_data = {
                    'arxiv_id': result.entry_id.split('/')[-1],
                    'title': result.title,
                    'authors': ', '.join(author.name for author in result.authors),
                    'abstract': result.summary,
                    'published_date': published_date,
                    'pdf_url': result.pdf_url,
                    'topics': [topic]
                }
                papers.append(paper_data)
            
            logger.info(f"Found {len(papers)} new papers for topic: {topic}")
            return papers
            
        except Exception as e:
            logger.error(f"Error fetching papers for topic {topic}: {str(e)}")
            return [] 