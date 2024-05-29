# Fetch data from Api

Introduction
This project fetches data from a given API, processes it to identify sources for each response, and returns the citations. A  streamlit  UI is provided to display the results.


Setup
Clone the repository.
git clone <repository_url>
cd Python-API-Citations-Fetcher


Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:
pip install -r requirements.txt


Usage
Run the code in pycharm
streamlit run app.py


code overview:
app.py: streamlit application to serve the citations through a web interface.
requirements.txt: Lists the required Python packages.
