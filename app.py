import requests
import time
import random
import pandas as pd
import streamlit as st

# Define the base URL for the API
base_url = "https://api.theirstack.com/v1/jobs/search"
api_key = "apikey"

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

        st.write(job_data)  # Raw data output
        for job in job_data.get('jobs', []):  # Ensure 'jobs' key exists
            job_title = job.get('job_title', 'N/A')
            company_name = job.get('company_name', 'N/A')
            job_location = job.get('location', 'N/A')
            job_description = job.get('job_description', 'N/A')
            date_posted = job.get('date_posted', 'N/A')
            job_url = job.get('job_url', '#')

             # Ghost job detection criteria
            is_ghost_job = False

            # Ghost job detection criteria:
             
                # Likely ghost job if company or location is missing, or description is too short
            if 'reposted': True
            continue
                

            # Add additional checks for outdated listings, unrealistic titles, etc.
            if len(job_title.split()) < 3 or int(date_posted.split("-")[0]) < 2025:
                continue

             # Highlight ghost jobs with red color
            if is_ghost_job:
                job_listings.append(f"""
                    <div style="background-color: red; color: white; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                        <strong>Job Title:</strong> {job_title} <br>
                        <strong>Company:</strong> {company_name} <br>
                        <strong>Location:</strong> {job_location} <br>
                        <strong>Date Posted:</strong> {date_posted} <br>
                        <a href="{job_url}" target="_blank" style="color: white; text-decoration: underline;">Apply here</a>
                    </div>
                """)
            else:
                # Normal job listings without ghost job criteria
                job_listings.append(f"""
                    <div style="background-color: lightgray; color: blue; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                        <strong>Job Title:</strong> {job_title} <br>
                        <strong>Company:</strong> {company_name} <br>
                        <strong>Location:</strong> {job_location} <br>
                        <strong>Date Posted:</strong> {date_posted} <br>
                        <a href="{job_url}" target="_blank" style="color: black; text-decoration: underline;">Apply here</a>
                    </div>
                """)



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