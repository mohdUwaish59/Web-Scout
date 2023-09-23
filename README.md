# Web-Scout

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## About
WebScout is a powerful web scraping and data visualization tool built using Django. It allows users to extract data from website [source](https://books.toscrape.com/index.html), store it in a MongoDB database, and generate detailed reports with visualizations.

Web scraping is a common technique used for various purposes, such as market research, competitive analysis, or data collection for research projects. WebScout simplifies the process by providing an easy-to-use web interface for scraping data from websites. Users can simply input the URL of the target website, and WebScout will handle the rest.

Key features of WebScout include:

- **Web Scraping**: WebScout utilizes Scrapy, a popular Python web crawling framework, to scrape data from websites efficiently.

- **Data Storage**: Scraped data is stored in a MongoDB database, making it easy to retrieve and analyze.

- **Data Visualization**: WebScout offers various data visualization options using Plotly, allowing users to gain insights from the collected data.

- **Report Generation**: Users can generate comprehensive reports that include charts, graphs, and word clouds based on the scraped data.

## Technologies Used

WebScout is built using the following technologies and libraries:

- Django: A Python web framework for building web applications.
- Scrapy: A Python web crawling and scraping framework.
- MongoDB: A NoSQL database for storing scraped data.
- Plotly: A data visualization library for creating interactive charts and graphs.
- Pandas: A data manipulation library for Python.
- ReportLab: A library for generating PDF reports.
- Other Python libraries for web development and data processing.

WebScout combines the power of these technologies to provide a seamless web scraping and data analysis experience.
## Installation

To get started with WebScout, follow these installation steps:

1. **Clone the Repository:**

   Clone the WebScout repository to your local machine using Git:

   ```bash
   git clone https://github.com/mohdUwaish59/Web-Scout.git
   ```bash
   cd Web-Scout
   ```bash
   virtualenv WebScout_Env
   ```bash
   For Windows
   WebScout_Env/Scripts/Activate
  ```bash
   pip install -r requirements.txt
  ```bash
   python manage.py runserver
