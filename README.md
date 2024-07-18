# Sentiment Analysis Project

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [AWS Configuration](#aws-configuration)
4. [Running the Program](#running-the-program)
5. [Usage](#usage)
6. [Extending the Project](#extending-the-project)
7. [Results](#results)
8. [Authors and Acknowledgment](#authors-and-acknowledgment)
9. [License](#license)

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

After running the program, a connection to the PostgreSQL database will be established, and the contents of the social media posts will be retrieved. The program will then preprocess the posts, analyze their sentiment, and update the database with the results. It will also run geospatial analysis using the coordinates of the posts.

1. **Console Output**:
   - A sentiment analysis model selector prompt will appear in the terminal. The user can input a value corresponding to their chosen model:
      - `1`: VADER
      - `2`: Hugging Face's roBERTa
      - Any other key: Run all models
   - The user can also exit the program by entering `q`.
2. **Database Updates**:
   - **Sentiment Analysis**:
      - If a results table for the selected model does not exist, a new table will be created with the following structure:
         - **Raw Data Models**:
            - `uk_prime_minister_content_id`: The index of the content.
            - `sentiment`: The sentiment identified using the specified model's sentiment analysis.
         - **Processed Data Models**:
            - `uk_prime_minister_content_processed_id`: The index of the processed content.
            - `sentiment`: The sentiment identified using the specified model's sentiment analysis.
      - The sentiment analysis results will be stored in the respective table.

   - **Geospatial Analysis**:
      - If a table for geospatial analysis does not exist, a new table will be created to store relevant information for analysis.
      - The program will plot the geospatial data on both a world map and a UK map using the coordinates of the posts. These plots will appear after sentiment analysis.

### Example

Below is an example of what a model's table would look like:

| content_id |   sentiment  |
|------------|--------------|
| 1          |   Negative   |
| 2          |   Neutral    |
| 3          |   Positive   |
| 4          |   Positive   |

## Extending the Project

The program is designed to be easily extendable. If you want to add new features or analysis methods, you can follow the patterns established in the current codebase.

### Adding New Tables

To add a new table, follow the pattern used in the `create_tables.py` file. For example, to create a new table for storing additional metadata:

```python
def create_metadata_table(cursor):
   create_table_query = """
   CREATE TABLE IF NOT EXISTS uk_prime_minister_metadata (
      uk_prime_minister_content_processed_id INT PRIMARY KEY,
      sentiment TEXT,
      FOREIGN KEY (uk_prime_minister_content_processed_id) REFERENCES uk_prime_minister_content_processed(uk_prime_minister_content_id)
   );
   """
   cursor.execute(create_table_query)
```

### Inserting Data into New Tables

To insert data into the new table, follow the pattern used in the `insert_data.py` file. For example, to insert data into the new metadata table:

```py
def insert_metadata(cursor, data):
   insert_query = """
      INSERT INTO uk_prime_minister_metadata (uk_prime_minister_content_processed_id, sentiment)
      VALUES (%s, %s)
      ON CONFLICT (uk_prime_minister_content_processed_id) DO UPDATE SET
      sentiment = EXCLUDED.sentiment
   """
   cursor.executemany(insert_query, data)
```

### Updating the Model Selection Process

To allow for the selection of the newly added model, update `sentiment_pipeline.py` and `pipeline_helpers.py`:

   1.	Update `sentiment_pipeline.py`: Modify the pipeline to include the new model choice and integrate its functionality.
	2.	Update `pipeline_helpers.py`: Extend the perform_selected_sentiment_analysis function to handle the new model choice and execute the appropriate analysis.

By following these steps, you can seamlessly extend the project to include new tables, insert data into them, and integrate additional sentiment analysis models.

## Results

Upon analyzing social media posts related to United Kingdom's Prime Minister Rishi Sunak, the sentiment analysis models revealed significantly differing results. These results can be compared to the corresponding sentiments provided by CobWebs.

- **CobWebs Sentiment Analysis:**
  - Positive: 56.98%
  - Negative: 16.17%
  - Neutral: 26.86%

- **VADER Sentiment Analysis:**
  - Positive: 37.06%
  - Negative: 39.83%
  - Neutral: 23.12%

- **roBERTa Sentiment Analysis:**
  - Positive: 0.09%
  - Negative: 16.50%
  - Neutral: 74.16%

## Authors and Acknowledgment

This project was led by Charles Wirks and served as Kelly Ton and Banan Truex's Data and Software Engineering Internship Capstone Project for Summer 2024. We would like to express our gratitude to:

  - **Charles Wirks**, for his guidance and leadership throughout the project.
  - **Timothy Epping and Corey Lapeyrouse**, for their invaluable feedback, technical insights, and assistance.
  - **SMX**, for providing the resources and support necessary to complete this project.
  - **Mentors and Colleagues**, for their ongoing assistance and support.

## License

This project is owned by [SMX](https://www.smxtech.com/)