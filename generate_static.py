import json
import sqlite3
from datetime import datetime

def generate_static_site():
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT title, authors, abstract, url, category, published
        FROM papers
        ORDER BY published DESC
        LIMIT 100
    ''')
    
    papers = []
    for row in cursor.fetchall():
        paper = {
            'title': row[0],
            'authors': row[1],
            'abstract': row[2],
            'url': row[3],
            'category': row[4],
            'published': row[5]
        }
        papers.append(paper)
    
    with open('papers.json', 'w') as f:
        json.dump(papers, f, indent=2)
    
    conn.close()

if __name__ == '__main__':
    generate_static_site() 