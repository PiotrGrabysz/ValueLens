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
* `SpaCy` for content filtering
* `trafilatura` and `BeautifulSoup4` for scraping
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

### Phase 2 – Crawler
* [x] Option to run the application in debug mode (no OpenAI call)
* [x] Search company's website subpages

### Phase 3 – History & Export

* [x] Save analyzed companies (SQLite + SQLAlchemy)
* [x] History view inside dashboard
* [ ] Export summaries (Markdown/PDF)
* [x] Tests for persistence and export

### Phase 4 – Smart Analysis

* [x] NLP-based filtering improvements (spaCy)
* [ ] Extract & tag company values (e.g. Innovation, Sustainability)

### Phase 5 – Production-grade Polish

* [ ] CI/CD with GitHub Actions (linting, tests, coverage)
* [ ] Dockerfile for reproducibility
* [ ] Deploy the application
* [ ] Add logo, demo GIF, and project badges to README

### 💡 Stretch Goals:

* [ ] Side-by-side company comparison
* [ ] Chrome extension (“Analyze with ValueLens”).
* [ ] AI-based CV tailoring suggestions.
* [ ] Multi-source analysis (e.g. LinkedIn and other portals).

## Installation

This project is managed by `uv`, so you need to [install](https://docs.astral.sh/uv/getting-started/installation/)
it first.

Then you can install project's dependencies with

```
uv sync
```

It is highly advisable to use SpaCy for filtering relevant text.
It requires downloading additional language dictionaries, which take around 40 MB.
You can install the project with this extra dependency with

```
uv sync --extra spacy
```

If you also want to install dev dependencies (pytest, linters), you can do so by running

```
uv sync --group lint --group tests
```
