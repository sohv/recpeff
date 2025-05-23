from sqlalchemy import create_engine, Column, String, DateTime, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between papers and topics
paper_topic = Table('paper_topic', Base.metadata,
    Column('paper_id', String, ForeignKey('papers.arxiv_id')),
    Column('topic_id', Integer, ForeignKey('topics.id'))
)

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    papers = relationship('Paper', secondary=paper_topic, back_populates='topics')

class Paper(Base):
    __tablename__ = 'papers'
    
    arxiv_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(String)
    abstract = Column(String)
    published_date = Column(DateTime)
    pdf_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    topics = relationship('Topic', secondary=paper_topic, back_populates='papers')

class Database:
    def __init__(self, db_url='sqlite:///papers.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_topic(self, topic_name):
        topic = self.session.query(Topic).filter_by(name=topic_name).first()
        if not topic:
            topic = Topic(name=topic_name)
            self.session.add(topic)
            self.session.commit()
        return topic
    
    def add_paper(self, arxiv_id, title, authors, abstract, published_date, pdf_url, topics):
        # Check if paper already exists
        existing_paper = self.session.query(Paper).filter_by(arxiv_id=arxiv_id).first()
        if existing_paper:
            return False
        
        # Create new paper
        paper = Paper(
            arxiv_id=arxiv_id,
            title=title,
            authors=authors,
            abstract=abstract,
            published_date=published_date,
            pdf_url=pdf_url
        )
        
        # Add topics
        for topic_name in topics:
            topic = self.add_topic(topic_name)
            paper.topics.append(topic)
        
        self.session.add(paper)
        self.session.commit()
        return True
    
    def get_papers_by_topic(self, topic_name):
        topic = self.session.query(Topic).filter_by(name=topic_name).first()
        if not topic:
            return []
        return topic.papers
    
    def close(self):
        self.session.close() 