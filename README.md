# Literature Paper Project

A one-stop solution for managing and interacting with your collection of scientific papers.

## Table of Contents
1. [Installation Instructions](#installation-instructions)
2. [Features](#features)
3. [Contact](#contact)

---

## Installation Instructions

### Prerequisites

- **Git Bash**: [Download Here](https://gitforwindows.org/)
- **Visual Studio Code**: [Download Here](https://code.visualstudio.com/download)
- **Python 3.11.5**: [Download Here](https://www.python.org/downloads/)

### Clone the Repository

1. Open Git Bash.
2. Run the following command:

    ```bash
    git clone https://github.com/Robert-T119/Literature_Paper.git
    ```

### Setup the Development Environment

1. Open Command Prompt and navigate to the project directory:

    ```bash
    cd Literature_Paper
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python -m venv myenv
    .\myenv\Scripts\activate
    ```

### Install Dependencies and Configuration

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file in the project directory and add your API keys:

    ```bash
    OPENAI_API_KEY='your_api_key'
    ```

### Run the Application

1. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

2. Start the development server:

    ```bash
    python manage.py runserver
    ```

3. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Features

### Overview

The Literature Paper Project aims to simplify the process of managing and researching scientific papers. It offers the following features:

#### Advanced Academic Paper Search
- Offers a robust search interface for finding papers based on criteria such as title, publication date, and more.

#### SOFC Literature Paper Finder
- A specialized tool for discovering and recommending papers related to solid oxide fuel cells, tailored to specific research interests.

#### Automated Paper Data Extractor
- Allows users to upload and manage PDFs, with the added feature of extracting DOIs and fetching supplementary paper information.

#### Smart PDF Query Chat
- Utilizes OpenAI's GPT-3.5 to interact with uploaded PDFs, enabling Q&A sessions based on the paper's content.

For further details or support, please contact: [tangbohui296@gmail.com](mailto:tangbohui296@gmail.com)

---

## Contact

For any queries or support, feel free to reach out at [tangbohui296@gmail.com](mailto:tangbohui296@gmail.com).

