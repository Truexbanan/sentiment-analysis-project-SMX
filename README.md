# Sentiment Analysis Project

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [AWS Configuration](#aws-configuration)
4. [Running the Program](#running-the-program)
5. [Usage](#usage)
6. [Extending the Project](#extending-the-project)
7. [Contributions](#contributions)
8. [Results](#results)
9. [Authors and Acknowledgment](#authors-and-acknowledgment)
10. [License](#license)

## Overview

The goal of this project is to conduct sentiment analysis on social media posts using natural language processing (NLP) techniques. This project encompasses data processing, geospatial plotting, sentiment analysis, and visualization. By implementing two sentiment analysis tools, VADER (Valence Aware Dictionary and sEntiment Reasoner) and Hugging Face’s RoBERTa model, we enable a comparative analysis of sentiment outcomes.

## Installation

1. Clone the repository:
   ```
   git clone https://git.smxtech.us/cwirks/sentiment-analysis-project.git
   ```

2. Change to the project directory:
   ```
   cd sentiment-analysis
   ```

3. (Optional) Create and activate a virtual environment:

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

2. Ensure that your AWS credentials are configured for translation services. This can be done by setting up your environment variables or configuring the AWS CLI as described in the [AWS Configuration](#aws-configuration) section. These credentials are necessary for using the AWS Translate service for language translation during the preprocessing step.

3. Run the `main.py` file in the project directory.

   Windows:
   ```
   py main.py
   ```

   MacOS/Linux:
   ```
   python3 main.py
   ```

## Usage

After running the program, it will establish a connection to the PostgreSQL database and retrieve the contents of the social media posts. The program will then preprocess the posts, analyze their sentiment, and update the database with the results. Additionally, it will perform geospatial plotting using the coordinates of the posts.

1. **Console Output**:
   - The user will be prompted to enter the base table name the program will work with, which will undergo verification. The user can quit the program by entering `quit`.
   - A sentiment analysis model selector prompt will appear in the terminal. The user can input a value corresponding to their chosen model:
      - `1`: VADER
      - `2`: Hugging Face's RoBERTa
      - Any other key: Run all models
   - The user can also exit the program by entering `quit`.
2. **Database Updates**:
   - **Sentiment Analysis**:
      - If a results table for the selected model does not exist, a new table will be created with the following structure:
         - **Raw Data Models**:
            - `{table_name}_content_id`: The index of the content.
            - `sentiment`: The sentiment identified using the specified model's sentiment analysis.
         - **Processed Data Models**:
            - `{table_name}_content_processed_id`: The index of the processed content.
            - `sentiment`: The sentiment identified using the specified model's sentiment analysis.
      - The sentiment analysis results will be stored in the respective table.

   - **Geospatial Analysis**:
      - The program dynamically handles the creation of tables for geospatial analysis. If a table for geospatial analysis does not exist, a new table will be created to store relevant information for analysis.
		- The program will plot the geospatial data on both a world map and a UK map using the coordinates of the posts. These plots will appear after sentiment analysis.

### Example

Below is an example of what a model's table would look like:

Table name: example

**For VADER (Processed Data)**:
| example_content_processed_id |   sentiment  |
|------------------------------|--------------|
| 1                            |   Negative   |
| 2                            |   Neutral    |
| 3                            |   Positive   |
| 4                            |   Positive   |

**For RoBERTa (Raw Data)**:
| example_content_id |   sentiment  |
|--------------------|--------------|
| 1                  |   Negative   |
| 2                  |   Neutral    |
| 3                  |   Neutral    |
| 4                  |   Positive   |

## Extending the Project

The program is designed to be easily extendable. If you want to add new features or analysis methods, you can follow the patterns established in the current codebase.

### Adding New Tables

To add a new table for storing sentiment analysis results for a specific model, follow the pattern used in the `create_tables.py` file. In the function names, replace 'model' with the sentiment model’s name (e.g., create_vader_sentiment_table for VADER). The approach differs based on whether you’re using processed or raw data.

Using processed data:
```python
def create_model_sentiment_table(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_sentiment_model (
        {table_name}_content_processed_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY ({table_name}_content_processed_id) REFERENCES {table_name}_content_processed({table_name}_content_id)
    );
    """
    cursor.execute(create_table_query)
```

OR Using raw data:
```py
def create_model_sentiment_table(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_sentiment_model (
        {table_name}_content_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY ({table_name}_content_id) REFERENCES {table_name}_content({table_name}_id)
    );
    """
    cursor.execute(create_table_query)
```

### Inserting Data into New Tables

To insert data into the new table, follow the pattern used in the `insert_data.py` file. The approach differs based on whether you're using processed or raw data.

Using processed data:
```py
def insert_model_sentiment_data(cursor, data, table_name):
    insert_query = f"""
        INSERT INTO {table_name}_sentiment_model ({table_name}_content_processed_id, sentiment)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_processed_id) DO UPDATE SET
        sentiment = EXCLUDED.sentiment;
    """ 
    # Convert to list of tuples for executemany
    formatted_data = [(item[0], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)
```

OR Using raw data:
```py
def insert_model_sentiment_data(cursor, data, table_name):
    insert_query = f"""
        INSERT INTO {table_name}_sentiment_model ({table_name}_content_id, sentiment)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_id) DO UPDATE SET
        sentiment = EXCLUDED.sentiment;
    """ 
    # Convert to list of tuples for executemany
    formatted_data = [(item[0], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)
```

### Updating the Model Selection Process

To allow for the selection of the newly added model, update `sentiment_pipeline.py` and `pipeline_helpers.py`:

   1.	Update `sentiment_pipeline.py`: Modify the pipeline to include the new model choice and integrate its functionality.
   2.	Update `pipeline_helpers.py`: Extend the perform_selected_sentiment_analysis function to handle the new model choice and execute the appropriate analysis.

By following these steps, you can seamlessly extend the project to include new tables, insert data into them, and integrate additional sentiment analysis models.

## Contributions

Thank you for your interest in contributing to our sentiment analysis tool. We appreciate your efforts in helping us enhance our application.

- **Contributing Opportunities**
  - **Bug Reporting**: Please report bugs through our GitLab issue tracker.
  - **Feature Suggestions**: Suggest new features/improvements by creating an issue in our GitLab repository.
  - **Code Contributions**: Employees and approved partners can contribute code through our GitLab repository.
- **Guidelines for Contributions**
  - **Coding Standards**: Maintain modularity, and ensure the code is uniform to the existing code.
  - **Commit Protocols**: Use clear and concise commit messages.
  - **Testing Requirements**: Ensure all tests pass before submitting your changes.
- **Development Environment Setup**
  - **Clone the repository**:
  ```
  git clone https://git.smxtech.us/cwirks/sentiment-analysis-project.git
  ```
  - Install dependencies: pip install -r requirements.txt
- **Pull Request Guidelines**
  1. Fork the repository and create a new branch for your new feature.
      a. **Example)** feature/geospatial-analysis
  2. Make and test your changes.
  3. Push to your branch and submit a merge request on GitLab.
  4. Include a detailed description of your changes.

## Results

Upon analyzing social media posts related to United Kingdom's Prime Minister Rishi Sunak, the sentiment analysis models revealed significantly differing results. These results can be compared to the corresponding sentiments provided by CobWebs.

- **CobWebs Sentiment Analysis:**
  - Positive: 57.79%
  - Negative: 15.88%
  - Neutral: 26.33%

- **VADER Sentiment Analysis:**
  - Positive: 37.06%
  - Negative: 39.66%
  - Neutral: 23.28%

- **RoBERTa Sentiment Analysis:**
  - Positive: 11.71%
  - Negative: 20.40%
  - Neutral: 67.89%

## Authors and Acknowledgment

This project was led by Charles Wirks and served as Kelly Ton and Banan Truex's Data and Software Engineering Internship Capstone Project for Summer 2024. We would like to express our gratitude to:

  - **Charles Wirks**, for his guidance and leadership throughout the project.
  - **Timothy Epping and Corey Lapeyrouse**, for their invaluable feedback, technical insights, and assistance.
  - **SMX**, for providing the resources and support necessary to complete this project.
  - **Mentors and Colleagues**, for their ongoing assistance and support.

## License

This project is owned by [SMX](https://www.smxtech.com/)