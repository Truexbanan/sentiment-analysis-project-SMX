# Sentiment Analysis Project

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Running the Program](#running-the-program)
4. [Usage](#usage)
5. [Results](#results)
6. [Authors and Acknowledgment](#authors-and-acknowledgment)
7. [License](#license)

## Overview

The goal of this project is to conduct sentiment analysis on social media posts using natural language processing (NLP) techniques. This project encompasses data processing, geospatial analysis, sentiment analysis, and visualization. By implementing two sentiment analysis tools, VADER (Valence Aware Dictionary and sEntiment Reasoner) and Hugging Face’s roBERTa model, we enable a comparative analysis of sentiment outcomes.

## Installation

1. Clone the repository:
   ```
   git clone https://git.smxtech.us/cwirks/sentiment-analysis-project.git
   ```

2. Change to the project directory:
   ```
   cd sentiment-analysis
   ```

3. (Optional) Create a virtual environment:

   Windows:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

   MacOS/Linux:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   To exit the virtual environment:
   
   Windows/MacOS/Linux:
   ```
   deactivate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Program

1. From the project directory, change to the 'src' directory.
   ```
   cd src
   ```

2. Ensure that you have an `.env` file, containing the database parameters. If you do not permit access, you will be unable to run this program. This file needs to be located outside of the sentiment-analysis-project directory.

3. Run the `main.py` file.

   Windows:
   ```
   python main.py
   ```

   MacOS/Linux:
   ```
   python3 main.py
   ```

## Usage

After running the program, a connection to the PostgreSQL database will be established, and the contents of the social media posts will be retrieved. The program will then preprocess the posts, analyze their sentiment, and update the database with the results.

1. **Console Output**: A table will be printed in the console displaying the count for the respective sentiment categories (Positive, Negative, or Neutral) for each sentiment analysis tool.
2. **Database Updates**: A new table will be created with the following columns:
   - `content_id`: The index of the processed content.
   - `content`: The processed content.
   - `vader_sentiment`: The sentiment identified using VADER sentiment analysis.
   - `roberta_sentiment`: The sentiment identified using roBERTa sentiment analysis.

The program is designed to be easily extendable. Other sentiment analysis tools can be added by following these steps:

	1.	Implement the new sentiment analysis tool: Write a function to analyze sentiment using the new tool.
	2.	Update the database schema to include a new column for the new tool’s results.
	3.	Analyze data using the new tool and insert results into the database.

### Example

Below is an example of what the updated database would look like:

| content_id | content                                                                                 |  vader_sentiment  | roberta_sentiment |
|:----------:|:---------------------------------------------------------------------------------------:|:-----------------:|:-----------------:|
| 1          | That wasn't a good movie. I found it quite boring, and there wasn't much action.        |      Negative     |      Negative     |
| 2          | Sam went shopping with her mom. They saw their Uncle Joey picking up flowers.           |      Neutral      |      Neutral      |
| 3          | The vibrant flowers and the cheerful songs of the birds create a delightful atmosphere. |      Positive     |      Positive     |

## Results

Regarding results, we are still analyzing our findings. This section will be updated accordingly.

- **VADER Sentiment Analysis:**
  - Positive: X%
  - Negative: Y%
  - Neutral: Z%

- **roBERTa Sentiment Analysis:**
  - Positive: A%
  - Negative: B%
  - Neutral: C%

## Authors and Acknowledgment

This project was led by Charles Wirks and served as Kelly Ton and Banan Truex's Data and Software Engineering Internship Capstone Project for Summer 2024. We would like to express our gratitude to:

  - Charles Wirks, for his guidance and leadership throughout the project.
  - SMX, for providing the resources and support necessary to complete this project.
  - Our mentors and colleagues, for their valuable feedback and assistance.

## License

This project is owned by [SMX](https://www.smxtech.com/)