# Literature Paper Project

## Table of Contents
1. [Installation Instructions](#installation-instructions)
2. [Functions](#Functions)

---

## Installation Instructions

### Required Applications
- **Git Bash**: [Download Link](https://gitforwindows.org/)
- **Visual Studio Code**: [Download Link](https://code.visualstudio.com/download)
- **Python 3.11.5**: [Download Link](https://www.python.org/downloads/)

### Clone the GitHub Repository
Open Git Bash and run the following command:
\```
git clone https://github.com/Robert-T119/Literature_Paper.git
\```

### Set Up the Project Environment
Open Command Prompt in Windows and navigate to the project directory:
\```
cd Literature_Paper
\```
Create a virtual environment and activate it:
\```
python -m venv myenv
.\myenv\Scripts\activate
\```

### Install Packages and Add Configuration
Install the required packages:
\```
pip install -r requirements.txt
\```
Create a `.env` file in the project directory and paste your API keys inside:
\```
OPENAI_API_KEY='your_api_key'
\```

### Launch the Application Locally
Run migrations and start the development server:
\```
python manage.py migrate
python manage.py runserver
\```
You can now access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Functions

### Tool Overview
The Literature Paper Project is designed to streamline the management and interaction with a growing collection of scientific papers. It offers the following functionalities:

#### Advanced Academic Paper Search
- Provides a search interface for users to find papers based on various criteria such as title, publication date, and more.

#### SOFC Literature Paper Finder
- A specialized tool for finding and recommending solid oxide fuel cell relevant papers based on user inputs and predefined research areas.

#### Automated Paper Data Extractor
- A dedicated module for uploading and managing PDFs, equipped with the capability to extract DOIs and fetch additional paper information.

#### Smart PDF Query Chat
- An innovative tool that leverages the power of OpenAI's GPT-3.5 model to interact with uploaded PDFs, potentially performing Q&A based on the content.

For more detailed information on each tool, please contact: tangbohui296@gmail.com
