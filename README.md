# 🕷️ Web Scraper Dashboard

A real-time web scraping dashboard that pulls the latest tech stories from Hacker News and visualizes them with interactive charts. Built with Python and Streamlit.

## What does it do?

This dashboard scrapes Hacker News every time you load it and shows you:
- Top trending tech stories
- Which posts are getting the most engagement
- Visual breakdowns of points and comments
- Search functionality to find specific topics

It's basically a prettier way to browse Hacker News with analytics built in.

## Getting Started

You'll need Python 3.8 or newer installed on your machine.

**1. Clone this repo**
```bash
git clone https://github.com/nulli83/web-scraper-dashboard-.git
cd web-scraper-dashboard-
```

**2. Install the required packages**
```bash
pip install -r requirements.txt
```

**3. Run it**
```bash
streamlit run scraper_dashboard.py
```

Your browser should open automatically to `http://localhost:8501`. If it doesn't, just paste that URL in your browser.

## How to use it

### Stories Tab
Browse all the scraped stories. Use the search box at the top to filter by keywords. Click any title to read the full article.

### Analytics Tab
See the data visualized:
- **Points Distribution** - Histogram showing how stories perform
- **Comments vs Points** - Scatter plot to see engagement patterns
- **Top 10 by Engagement** - The most discussed and upvoted stories

### Top Stories Tab
Quick view of the 10 highest-scoring stories with all their stats in one place.

### Settings (Sidebar)
- Adjust how many stories to fetch (10-100)
- Turn on auto-refresh to update every 30 seconds
- Download all data as CSV with a timestamp

## What's it built with?

- **Streamlit** - For the web interface
- **BeautifulSoup** - To scrape the data
- **Pandas** - For data handling
- **Plotly** - For the interactive charts
- **Requests** - To fetch web pages

## Ideas for improvements

- Add more sources (Reddit, Product Hunt, tech news sites)
- Store historical data in a database
- Email alerts for trending topics you care about
- Sentiment analysis on headlines
- Deploy it online so anyone can use it

## Contributing

If you want to add features or fix bugs, feel free to open a pull request. For major changes, open an issue first so we can discuss it.

## License

MIT

## Author

Built by Jonathan Holm ([@nulli83](https://github.com/nulli83))

---

If this project helped you, give it a ⭐ on GitHub!
