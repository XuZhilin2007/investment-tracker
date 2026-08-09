# Investment Tracker

A personal investment record and review system built with Python.

The goal of this project is not to build an automated trading system, but to create a structured way to record investment decisions, review past operations, and improve investment thinking through data analysis and AI assistance.

---

## Project Goals

Investment decisions are often affected by emotions, incomplete information, and lack of systematic review.

This project aims to help investors:

- Record every investment decision with context and reasoning.
- Track trading history in a structured database.
- Review past decisions and identify mistakes or successful patterns.
- Generate periodic investment summaries.
- Use AI as an assistant for reflection and analysis.

---

## Non-Goals

This project is **not** designed for:

- Automated trading.
- High-frequency trading.
- Quantitative strategy execution.
- Real-time market prediction.
- Replacing human investment decisions.

Market data and AI features will only serve as optional assistants.

The final investment decisions always remain with the user.

---

# Current Features (MVP)

## Investment Record Model

Each investment record contains:

### Trading Information

- Trade date
- Symbol
- Asset name
- Market
- Asset type
- Buy / Sell action
- Price
- Quantity
- Transaction amount
- Fees

### Investment Reasoning

- Investment strategy
- Holding plan
- Purchase / selling reason
- Market environment
- Investment thesis
- Risks
- Exit conditions

### Review Information

- Tags
- Future review notes
- Lessons learned

The system keeps both:

Investment action
        +
Investment reasoning
        +
Future reflection

instead of only storing transaction history.

---

# Data Storage

The project uses SQLite as the local database.

Database location:

data/investment_tracker.db

Current table:

investment_records

Design principles:

- Local-first storage.
- User owns all investment data.
- No personal financial information is uploaded.
- Database files are ignored by Git.

---

# Project Structure

investment-tracker/
├── main.py                  # Application entry point
│
├── src/
│   │
│   ├── records/              # Investment record models
│   │   ├── models.py
│   │   └── init.py
│   │
│   ├── storage/              # Database operations
│   │   ├── sqlite_repository.py
│   │   └── init.py
│   │
│   ├── reviews/              # Future review generation
│   │
│   └── integrations/         # Optional AI and external services
│
├── tests/                    # Automated tests
│
├── data/                     # Local database files
│
├── README.md
└── requirements.txt

---

# Technology Stack

Current:

- Python
- SQLite
- unittest
- Git / GitHub


Future:

- Pandas for data analysis
- Data visualization
- OCR transaction import
- AI-assisted investment review
- Web interface

---

# Running the Project

Create and activate the environment:

```bash
conda activate investment
Initialize database:
python main.py
Expected output:
Database initialized:
data/investment_tracker.db
Running Tests
Execute:
python -m unittest discover -s tests -v
Current tests cover:
Investment record validation.
Amount calculation.
Enum restrictions.
SQLite database creation.
CRUD operations.
Data integrity.
Development Roadmap
Phase 1 - MVP (Completed)

Investment record model

SQLite local storage

Basic CRUD operations

Automated tests
Phase 2 - Personal Investment Journal

Command line interface

Import/export CSV files

Investment timeline

Monthly review generation

Annual investment summary
Phase 3 - AI Assisted Analysis

AI investment journal analysis

Decision pattern discovery

Risk identification

Personalized review suggestions
Phase 4 - User Interface

Web dashboard

Portfolio visualization

Mobile-friendly access
Design Philosophy
A good investment system should not only answer:
"What did I buy?"

but also:
"Why did I buy it?"
"What information did I have at that time?"
"Was my reasoning correct?"
"What can I learn from this decision?"

This project focuses on improving the investment process rather than predicting the market.
License
This project is for personal learning and research purposes.