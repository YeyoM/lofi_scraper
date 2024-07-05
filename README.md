# Lofi Music Web Scraper

This is a web scraper that scrapes lofi music from multiple sources and saves
the urls to a firebase database. The scraper is written in Python and uses the
BeautifulSoup library to scrape the web pages.

## Installation

To install the scraper, you need to have Python installed on your machine. You
can download Python from the official website [here](https://www.python.org/).

You will also need to have virtualenv installed on your machine. You can
install virtualenv using the following command:

```bash
pip install virtualenv
```

After that you can clone the repository and install the required packages using
the following commands:

```bash
git clone
cd lofi-music-web-scraper

# Create a virtual environment
virtualenv lofi

# Activate the virtual environment
source lofi/bin/activate

# Install the required packages
pip install -r requirements.txt
```

## Available commands

The scraper has the following commands:

1. Run the scraper and save the songs to a json file:

```bash
python src/scraper.py
```

2. Running the tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

3. Save the songs to a firebase database:

```bash
python src/firebase.py
```

4. Run the scraper and save the songs to a firebase database:

```bash

```

## Project structure

The project has the following structure:

```
lofi_scraper/
├── data/
│   └── scrapped_songs.json
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── firebase.py
│   └── test_scraper.py
├── README.md
├── requirements.txt
└── .gitignore
```
