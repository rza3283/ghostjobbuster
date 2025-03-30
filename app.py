import requests
import time
import random
import pandas as pd
import streamlit as st

# Define the base URL for the API
base_url = "https://api.theirstack.com/v1/jobs/search"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyZW1zd29ybGRiZWF0c0BnbWFpbC5jb20iLCJwZXJtaXNzaW9ucyI6InVzZXIiLCJjcmVhdGVkX2F0IjoiMjAyNS0wMy0zMFQxNzoxOToyNS4xMjg2NjQrMDA6MDAifQ.NpGSpReSEPAatgcRoj8qMHAFlVr_H0_sMuImslOkgrs"

# Function to fetch job listings based on search term, location, and filters
def fetch_jobs(search_term, location):
    job_listings = []

    # Construct the payload with the correct fields
    payload = {
        "posted_at_max_age_days": 15,  # Filter jobs posted within the last 15 days
        "posted_at_gte": "2025-03-01",  # Optional: Add the 'posted_at_gte' filter
        "posted_at_lte": "2025-03-30",  # Optional: Add the 'posted_at_lte' filter
        "job_country_code_or": ["US"],  # Filter for job listings in the US
        "job_title_or": [search_term],  # Use job_title_or for the search term
        "company_location_pattern_or": [location],  # Use location_or for the location
        "order_by": [{"desc": True, "field": "date_posted"}],  # Order by date posted
        "limit": 10,  # Limit the number of job listings to 10
        "page": 0,  # Start from the first page of results
        "blur_company_data": False,  # Do not blur company data
    }

    # Set the headers including the API key and content type
    headers = {
        'Authorization': f'Bearer {api_key}',  # Use the api_key variable here
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Send a POST request to fetch the job listings
    response = requests.post(base_url, json=payload, headers=headers)

    # Add a sleep delay between requests to avoid hitting the server too quickly
    time.sleep(random.uniform(1.5, 3.0))  # Random delay between 1.5 and 3 seconds

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        job_data = response.json()
        # Display job listings as a simple table
        # Display job listings in a grid format using columns

        st.write(job_data)  # Render HTML


        # Debugging: Uncomment the line below to see the job data structure
        #st.write(job_data)  # Display the raw API response

        # Extract and store information for each job listing from the API response
        #for job in job_data.get('jobs', []):  # Ensure 'jobs' key exists
         #   job_listings.append({
          #      'Job Title': job.get('job_title', 'N/A'),
           #     'Company': job.get('company_name', 'N/A'),
            #    'Location': job.get('location', 'N/A'),
             #   'Posted Date': job.get('date_posted', 'N/A')  # Add posted date
            #})
    else:
        st.write(f"Error: {response.status_code} - {response.text}")

    return job_listings



# Streamlit UI to collect user inputs for search term and location
st.title("Job Search")

# User inputs for search term and location
search_term = st.text_input("Enter job title or keyword", "software engineer")
location = st.text_input("Enter job location", "New York")

# Button to start fetching jobs
if st.button("Fetch Jobs"):
    # Display a loading spinner
    with st.spinner('Fetching jobs from the API...'):
        job_listings = fetch_jobs(search_term, location)
        
        if job_listings:
            # Use HTML to display the job listings
            col1, col2 = st.columns([1, 1])  # Two columns for better visual layout

            for job in job_listings:
                with col1:
                    st.markdown(f"### {job['Job Title']}")
                with col2:
                    st.markdown(f"**Company:** {job['Company']}")
            
                st.write(f"**Location:** {job['Location']}")
                st.write(f"**Posted Date:** {job['Posted Date']}")
                st.markdown("---")  # Separator for better readability