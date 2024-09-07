# Importing releavnt libraries
import requests
from bs4 import BeautifulSoup

def scraping_alg(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all divs with the class I will specify
            divs = soup.find_all('div', class_='prose')
            # Write the content to a text file on my local computer
            destination = ''
            # This will open the file and write to it
            with open(destination, 'w') as file:
                for div in divs:
                    file.write(str(div))
                    file.write('\n')
            # Success message
            print(f'Content successfully scraped and saved to {destination}')
            return destination
        else:
            # Print an error message for responsiveness so I know if something went wrong
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
            return None
    # An exception to handle if the URL is invalid
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

# Call the function and pass the URL of the website I want to scrape
scraped_file = scraping_alg('')
