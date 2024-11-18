# LinkedIn Job Scraper

This project is a **Flask-based web application** that allows users to scrape job postings from LinkedIn based on job titles and location. The scraped data is visualized using graphs and displayed in a user-friendly interface.

---

## Features

- **User Login:** Enter LinkedIn credentials securely.
- **Job Search:** Input job titles and location to scrape job postings.
- **Data Visualization:** 
  - Graphs for job roles distribution.
  - Graphs for job location distribution.
- **Tabular View:** Detailed job data in a tabular format.

---

## Technologies Used

### Backend
- **Python**:
  - `Flask` for web framework.
  - `Selenium` for web scraping.
  - `BeautifulSoup` for parsing HTML.
  - `Pandas` for data manipulation.
  - `Matplotlib` for data visualization.

### Frontend

- **HTML**:
  - `Bootstrap` for styling (optional for enhancing UI).
- **CSS** for custom styling.

---

## Prerequisites

1. **Python** (3.x recommended): Install from [python.org](https://www.python.org/downloads/).
2. **Google Chrome** and its compatible **ChromeDriver**:
   - Download ChromeDriver: [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/).
   - Ensure `chromedriver` is added to your `PATH` or placed in the project directory.

3. Install required Python libraries:
   ```bash
   pip install flask selenium pandas matplotlib beautifulsoup4


LinkedIn_Job_Analysis/
├── app.py             # Main Flask app
├── templates/         # HTML templates
│   ├── login.html     # Login page
│   ├── results.html   # Results page
├── static/            # Static files (CSS, JS, images)
│   └── style.css      # Custom styles
├── chromedriver       # ChromeDriver for Selenium
└── README.md          # Project documentation
