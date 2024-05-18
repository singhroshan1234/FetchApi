import streamlit as st
import requests
import time
import logging
import difflib

logging.basicConfig(level=logging.INFO)


def fetch_page_data(session, base_url, page):
    """Fetch data from a specific page."""
    response = session.get(base_url, params={"page": page})
    if response.status_code != 200:
        logging.error(f"HTTP error occurred: {response.status_code} {response.reason}")
        return []

    return response.json().get('data', {}).get('data', [])


def fetch_all_data():
    """Fetch all paginated data from the API."""
    base_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    page = 1
    all_data = []

    with requests.Session() as session:
        while True:
            data = fetch_page_data(session, base_url, page)
            if not data:
                break
            all_data.extend(data)
            page += 1
            time.sleep(1)  # to prevent hitting rate limits

    return all_data


def match_response_to_sources(response_text, sources):
    """Match response text to its sources using difflib."""
    citations = []
    for source in sources:
        context = source['context']
        if difflib.SequenceMatcher(None, response_text, context).ratio() > 0.5:
            citations.append({
                "id": source["id"],
                "link": source.get("link", "")
            })
    return citations


def process_item(item):
    """Process a single data item to match responses with their sources."""
    response_text = item['response']
    sources = item['source']
    return {"citations": match_response_to_sources(response_text, sources)}


def process_data(data):
    """Process all data items."""
    return [process_item(item) for item in data]


def main():
    """Main function to fetch, process data and display in Streamlit."""
    st.title("Data Fetching and Citation Matching")

    fetch_button = st.button("Fetch Data")

    if fetch_button:
        st.info("Fetching data from API...")
        data = fetch_all_data()
        if data:
            st.success("Data fetched successfully!")
            st.info("Processing data...")
            results = process_data(data)
            citations = [citation for result in results for citation in result["citations"]]
            st.success("Data processed successfully!")

            if citations:
                st.write("Citations:")
                for citation in citations:
                    st.write(f"ID: {citation['id']}, Link: {citation['link']}")
            else:
                st.write("No citations found.")
        else:
            st.error("No data fetched from the API.")


if __name__ == "__main__":
    main()
