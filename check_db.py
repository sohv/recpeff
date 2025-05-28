from database import Database, Paper
from datetime import datetime

def check_database():
    db = Database()
    papers = db.session.query(Paper).all()
    print(f"\nTotal papers in database: {len(papers)}")
    print("\nMost recent papers:")
    for paper in sorted(papers, key=lambda x: x.published_date, reverse=True)[:5]:
        print(f"\nTitle: {paper.title}")
        print(f"Published: {paper.published_date}")
        print(f"Keywords: {[k.name for k in paper.keywords]}")
        print("-" * 80)
    db.close()

if __name__ == "__main__":
    check_database() 