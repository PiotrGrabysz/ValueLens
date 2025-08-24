# ValueLens - Company Values Extractor

> 🔍 Discover what companies truly stand for. 

ValueLens is a personal project designed to help job-seekers (like myself) quickly analyze a company’s mission and
values from their website.

Paste a company website URL, and ValueLens will:

* Scrape mission & values statements
* Summarize them with AI (OpenAI GPT-4o-mini)
* Highlight the original paragraphs

This helps with:

* Deciding if a company matches your values
* Preparing tailored CVs and cover letters
* Saving time in the job search process

*I started this project because I found myself many times digging into a company's website trying to understand their
values (and to see if they have any). At the same time, I wanted to sharpen my Generative AI skills.
I realised this project can help both develop and automate a repetitive task.*

## 🛠 Tech Stack

* Python 3.12+
* `uv` for project management 
* OpenAI API (GPT-4o-mini for summarization)
* `trafilatura` for scraping
* `Streamlit` for dashboard
* `pytest` + `pytest-cov` for tests
* `ruff` for linting & formatting

## 🚀 Roadmap

### Phase 1 – Core MVP ✅ (in progress)

* [x] URL → scrape mission/values text
* [x] Summarize with AI (OpenAI GPT-4o-mini)
* Streamlit dashboard for interactive use
    * [x] Input box for company URL
    * [x] Display relevant paragraphs + AI summary
* [x] Unit tests for scraping & filtering
* [ ] Error handling (bad URLs, no values found)
* [x] Integration tests

## Phase 2 – Crawler
* [x] Option to run the application in debug mode (no OpenAI call)
* [ ] Search company's website subpages

## Phase 3 – History & Export

* [ ] Save analyzed companies (SQLite)
* [ ] History view inside dashboard
* [ ] Export summaries (Markdown/PDF)
* [ ] Tests for persistence and export

## Phase 4 – Smart Analysis

* [ ] NLP-based filtering improvements (spaCy / TF-IDF)
* [ ] Extract & tag company values (e.g. Innovation, Sustainability)
* [ ] Side-by-side company comparison

## Phase 5 – Production-grade Polish

* [ ] CI/CD with GitHub Actions (linting, tests, coverage)
* [ ] Dockerfile for reproducibility
* [ ] Deploy the application
* [ ] Add logo, demo GIF, and project badges to README

## 💡 Stretch Goals:

* [ ] Chrome extension (“Analyze with ValueLens”).
* [ ] AI-based CV tailoring suggestions.
* [ ] Multi-source analysis (e.g. LinkedIn and other portals).
