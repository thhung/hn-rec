# Hacker News Recommendation

The report for this project is in [Report](./report.md)

Demo to the web version is: [Demo](https://huggingface.co/spaces/CelDom/hn-rec)

This repository contains a simle recommendation system built for Hacker News articles using Python. The system suggests articles based on a user's bio. It leverages natural language processing (NLP) to provide personalized recommendations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

This recommendation system is designed to suggest the most relevant articles on Hacker News based on user preferences, article similarity. The goal is to recommend articles that a user may find interesting based on users' bio they provided.

## Features

- **User bio**: Suggests articles based on the similarity of article's title to user's bio, using sentence embeddings.
  
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/thhung/hn-rec.git
    cd hn-rec
    ```
2. Create virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use venv\Scripts\activate
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage
2. Launch app 
    ```bash
    streamlit run app.py # launch app
    ```

## License
Check [License](./LICENSE)