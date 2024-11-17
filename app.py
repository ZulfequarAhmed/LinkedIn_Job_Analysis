import time
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, redirect, url_for
import io
import base64

app = Flask(__name__)
scraped_data = None  # To store scraped data globally

# Function to set up Chrome WebDriver
def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_service = Service("C:/Users/SYED ZULFEQUAR AHMED/chromedriver.exe")  # Ensure chromedriver path is correct
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Function to log into LinkedIn
def linkedin_login(driver, linkedin_username, linkedin_password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(linkedin_username)
    driver.find_element(By.ID, "password").send_keys(linkedin_password + Keys.RETURN)
    time.sleep(5)

# Function to scrape jobs
def scrape_jobs(linkedin_username, linkedin_password, job_titles, location):
    driver = create_webdriver()
    linkedin_login(driver, linkedin_username, linkedin_password)
    job_roles = [title.strip().replace(' ', '%20') for title in job_titles.split(',')]
    job_data = []

    for role in job_roles:
        base_url = f'https://www.linkedin.com/jobs/search/?keywords={role}&location={location}&start='
        for page in range(0, 75, 25):  # Adjust pages as needed
            url = base_url + str(page)
            driver.get(url)
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'job-card-list__title--link'))
                )
            except:
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            jobs = soup.find_all('div', class_='job-card-container')
            for job in jobs:
                title_tag = job.find('a', class_='job-card-list__title--link')
                title = (
                    title_tag.text.replace('\n', ' ').strip() if title_tag else 'Title not specified'
                )
                company_tag = job.find('span', class_='job-card-container__primary-description')
                company = company_tag.text.strip() if company_tag else 'Company not specified'
                location_tag = job.find('ul', class_='job-card-container__metadata-wrapper')
                location = (
                    location_tag.find('li', class_='job-card-container__metadata-item').text.strip()
                    if location_tag
                    else 'Location not specified'
                )
                job_data.append(
                    {'Role': role.replace('%20', ' '), 'Title': title, 'Company': company, 'Location': location}
                )

    driver.quit()
    return pd.DataFrame(job_data)

# Route for Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        linkedin_username = request.form['linkedin_username']
        linkedin_password = request.form['linkedin_password']
        job_titles = request.form['job_titles']
        location = request.form['location']

        global scraped_data
        scraped_data = scrape_jobs(linkedin_username, linkedin_password, job_titles, location)

        return redirect(url_for('results'))

    return render_template('login.html')

# Route for Results Page
@app.route('/results')
def results():
    global scraped_data
    if scraped_data is None:
        return redirect(url_for('login'))

    # Generate Role Distribution Plot
    role_counts = scraped_data['Role'].value_counts()
    plt.figure(figsize=(8, 5))
    role_counts.plot(kind='bar', color='skyblue')
    plt.title('Job Roles Distribution')
    plt.xlabel('Job Role')
    plt.ylabel('Number of Jobs')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    role_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # Generate Location Distribution Plot
    location_counts = scraped_data['Location'].value_counts()
    plt.figure(figsize=(8, 5))
    location_counts.plot(kind='bar', color='lightgreen')
    plt.title('Jobs by Location')
    plt.xlabel('Location')
    plt.ylabel('Number of Jobs')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    location_plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template(
        'results.html',
        tables=[scraped_data.to_html(classes='data')],
        titles=scraped_data.columns.values,
        role_plot_url=role_plot_url,
        location_plot_url=location_plot_url,
    )

if __name__ == '__main__':
    app.run(debug=True)
