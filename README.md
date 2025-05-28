# RecPEff - fetch RECent Papers EFFectively

A tool that tracks and stores the latest academic papers from arXiv based on user-defined topics.

## Features

- Fetches papers from arXiv based on topic categories
- Stores papers in a local SQLite database
- Prevents duplicate entries
- Scheduled updates at configurable intervals
- Supports multiple topics
- Logs new paper additions

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the main script:
```bash
python main.py
```

## Configuration

The system comes with default topics in computer science:
- cs.AI (Artificial Intelligence)
- cs.CL (Computation and Language)
- cs.LG (Machine Learning)
- cs.CV (Computer Vision)
- cs.NE (Neural and Evolutionary Computing)

You can modify the topics in `main.py` by changing the list passed to the `PaperTracker` class.

## Database

The system uses SQLite by default, storing the database in `paper.db`. The database schema includes:
- Papers table: stores paper metadata
- Topics table: stores topic categories
- Paper-Topic association table: manages many-to-many relationships

## Usage

The system will:
1. Run an initial paper fetch when started
2. Continue to check for new papers every 24 hours
3. Log new papers as they are added to the database

To stop the system, press Ctrl+C.

## Adding Custom Topics

To add custom topics, modify the topics list in `main.py`. Topics should be valid arXiv category codes. You can find the complete list of arXiv categories at: https://arxiv.org/category_taxonomy 
