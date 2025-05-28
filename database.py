from sqlalchemy import create_engine, Column, String, DateTime, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

paper_keyword = Table('paper_keyword', Base.metadata,
    Column('paper_id', String, ForeignKey('papers.arxiv_id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)

class Keyword(Base):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    papers = relationship('Paper', secondary=paper_keyword, back_populates='keywords')

class Paper(Base):
    __tablename__ = 'papers' 
    arxiv_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(String)
    abstract = Column(String)
    published_date = Column(DateTime)
    pdf_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    keywords = relationship('Keyword', secondary=paper_keyword, back_populates='papers')

class Database:
    def __init__(self, db_url='sqlite:///paper.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_keyword(self, keyword_name):
        keyword = self.session.query(Keyword).filter_by(name=keyword_name).first()
        if not keyword:
            keyword = Keyword(name=keyword_name)
            self.session.add(keyword)
            self.session.commit()
        return keyword
    
    def add_paper(self, arxiv_id, title, authors, abstract, published_date, pdf_url, keywords):
        existing_paper = self.session.query(Paper).filter_by(arxiv_id=arxiv_id).first()
        if existing_paper:
            return False
        
        paper = Paper(
            arxiv_id=arxiv_id,
            title=title,
            authors=authors,
            abstract=abstract,
            published_date=published_date,
            pdf_url=pdf_url
        )
        
        for keyword_name in keywords:
            keyword = self.add_keyword(keyword_name)
            paper.keywords.append(keyword)
        
        self.session.add(paper)
        self.session.commit()
        return True
    
    def get_papers_by_keyword(self, keyword_name):
        keyword = self.session.query(Keyword).filter_by(name=keyword_name).first()
        if not keyword:
            return []
        return keyword.papers
    
    def close(self):
        self.session.close() 