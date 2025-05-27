import arxiv
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArxivFetcher:
    def __init__(self, max_results=100):
        self.max_results = max_results
        self.client = arxiv.Client()
    
    def fetch_papers(self, keywords, days_back=7):
        try:
            date_threshold = datetime.now() - timedelta(days=days_back)
            search_query = ' OR '.join(f'"{keyword}"' for keyword in keywords)
            logger.info(f"Searching with query: {search_query}")
            
            search = arxiv.Search(
                query=search_query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            papers = []
            for result in self.client.results(search):
                published_date = result.published.replace(tzinfo=None)
                
                if published_date < date_threshold:
                    continue
                
                paper_data = {
                    'arxiv_id': result.entry_id.split('/')[-1],
                    'title': result.title,
                    'authors': ', '.join(author.name for author in result.authors),
                    'abstract': result.summary,
                    'published_date': published_date,
                    'pdf_url': result.pdf_url,
                    'keywords': keywords
                }
                papers.append(paper_data)
            
            logger.info(f"Found {len(papers)} new papers for keywords: {keywords}")
            return papers
            
        except Exception as e:
            logger.error(f"Error fetching papers for keywords {keywords}: {str(e)}")
            return [] 