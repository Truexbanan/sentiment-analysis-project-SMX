# Sentiment Analysis Project

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [AWS Configuration](#aws-configuration)
4. [Running the Program](#running-the-program)
5. [Usage](#usage)
6. [Results](#results)
7. [Authors and Acknowledgment](#authors-and-acknowledgment)
8. [License](#license)

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

## AWS Configuration

To use the AWS Translate service, you need to configure your AWS credentials. Follow these steps to set up your credentials:

### Windows

#### Using Environment Variables

1. Open Environment Variables:
   - Right-click on `This PC` or `Computer` on your desktop or in File Explorer.
   - Click on `Properties`.
   - Click on `Advanced system settings`.
   - Click on the `Environment Variables` button.

2. Add AWS Credentials:
   - In the `System variables` section, click `New`.
   - Add the following variables:
     - `AWS_ACCESS_KEY_ID` with your access key.
     - `AWS_SECRET_ACCESS_KEY` with your secret key.
     - (Optional) `AWS_SESSION_TOKEN` if you're using temporary credentials.

### macOS

#### Using the AWS CLI

1. Install the AWS CLI:
   - If you haven't installed the AWS CLI yet, you can install it using Homebrew:
     ```
     brew install awscli
     ```
   - Alternatively, follow the instructions on the [AWS CLI installation page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

2. Configure the AWS CLI:
   - Open your terminal.
   - Run the following command to configure your AWS credentials:
     ```
     aws configure
     ```
   - Follow the prompts to enter your AWS access key, secret key, and default region:
     ```
     AWS Access Key ID [None]: your_access_key
     AWS Secret Access Key [None]: your_secret_key
     Default region name [None]: us-east-1
     Default output format [None]: your_format
     ```

### Linux

#### Using the AWS CLI

1. Install the AWS CLI:
   - If you haven't installed the AWS CLI yet, you can install it using your package manager. For example, on Ubuntu, you can use:
     ```sh
     sudo apt-get update
     sudo apt-get install awscli
     ```
   - Alternatively, you can follow the instructions on the [AWS CLI installation page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

2. Configure the AWS CLI:
   - Open your terminal.
   - Run the following command to configure your AWS credentials:
     ```sh
     aws configure
     ```
   - Follow the prompts to enter your AWS access key, secret key, and default region:
     ```sh
     AWS Access Key ID [None]: your_access_key
     AWS Secret Access Key [None]: your_secret_key
     Default region name [None]: us-east-1
     Default output format [None]: your_format
     ```

## Running the Program 

1. Ensure that you have an `.env` file, containing the database parameters. If you do not permit access, you will be unable to connect to the database and run this program. This file needs to be located outside of the sentiment-analysis-project directory.

2. Run the `main.py` file in the project directory.

   Windows:
   ```
   py main.py
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
|------------|-----------------------------------------------------------------------------------------|-------------------|-------------------|
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