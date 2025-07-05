# Vibe AI Newsletter

An AI-powered newsletter system that sources, processes, and delivers curated content.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Current Features

### VAI-1: Basic Web Scraper
- Extracts article title and content from a given URL
- Saves content to JSON format
- Handles network errors gracefully

**Usage:**
```bash
python fetch_article.py <URL>
```

**Example:**
```bash
python fetch_article.py https://example.com/article
```

The script will save the extracted content to `article.json` with the following structure:
```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "content": "Article content..."
}
```

## Development Progress

- [x] VAI-1: Basic web scraper implementation
- [ ] VAI-2: arXiv API client
- [ ] VAI-3: robots.txt compliance
- [ ] VAI-4: Database persistence
- [ ] VAI-5: Embedding pipeline
- [ ] VAI-6: Text summarization
- [ ] VAI-7: MapReduce summarization
- [ ] VAI-8: Human-in-the-loop review
- [ ] VAI-9: Beehiiv template setup
- [ ] VAI-10: Beehiiv API integration
- [ ] VAI-11: Scheduler implementation
