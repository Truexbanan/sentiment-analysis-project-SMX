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

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Program

1. Run the `dbeaverToJson.py` script located in the scripts directory to generate `content.json`, the data file to be analyzed.

   Windows:
   ```
   cd scripts
   python dbeaverToJson.py
   ```

   MacOS/Linux:
   ```
   cd scripts
   python3 dbeaverToJson.py
   ```

2. From the scripts directory, change to the src directory and run main.py.

   Windows:
   ```
   cd ..
   cd src
   python main.py
   ```

   MacOS/Linux:
   ```
   cd ..
   cd src
   python3 main.py
   ```

## Usage

After running the program, `content.json` will be analyzed for sentiment. The following will occur:

1. **Console Output**: A table will be printed in the console displaying the count for the respective sentiment categories (Positive, Negative, or Neutral) for each sentiment analysis tool.
2. **Generated Files**: Three JSON files will be created in the `data` directory:
   - `vader_processed_content.json`: Contains processed content analyzed by the VADER model.
   - `roberta_processed_content.json`: Contains processed content analyzed by Hugging Face’s roBERTa model.
   - `duplicate_content.json`: Stores any duplicate content identified during analysis.

### Example
Below is an example of what the json files would look like.

 `content.json`:
   ```json
   {
       "index": [
           [
               1,
               "I really like this movie!"
           ]
       ]
   }
   ```

`vader_processed_content.json` and `roberta_processed_content.json`:
   ```json
   {
       "index": [
           [
               1,
               "I really like this movie!",
               "Positive"
           ]
       ]
   }
   ```

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

This project is owned by SMX.