import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize an empty list to store the data
data = []

# Define the number of pages you want to scrape 
num_pages = 20

# Define headers with a user-agent to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Loop through each page
for page in range(1, num_pages + 1):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP request errors
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product information
    products = soup.find_all('div', class_='s-result-item')
    for product in products:
        product_url_element = product.find('a', class_='s-link-normal')
        if product_url_element:
            product_url = "https://www.amazon.in" + product_url_element['href']
            product_name = product.find('span', class_='a-text-normal').text.strip()
            product_price = product.find('span', class_='a-price-whole').text.strip()
            rating = product.find('span', class_='a-icon-alt').text.strip()
            num_reviews = product.find('span', class_='a-size-base').text.strip()

            # Part 2: Scrape additional details from the product URL
            try:
                response_product = requests.get(product_url, headers=headers)
                response_product.raise_for_status()
                soup_product = BeautifulSoup(response_product.content, 'html.parser')
                product_description = soup_product.find('div', {'id': 'productDescription'})
                asin_element = soup_product.find('th', text='ASIN')
                manufacturer_element = soup_product.find('th', text='Manufacturer')

                if product_description:
                    product_description = product_description.text.strip()
                else:
                    product_description = "N/A"

                if asin_element:
                    asin = asin_element.find_next('td').text.strip()
                else:
                    asin = "N/A"

                if manufacturer_element:
                    manufacturer = manufacturer_element.find_next('td').text.strip()
                else:
                    manufacturer = "N/A"

                data.append([product_url, product_name, product_price, rating, num_reviews, product_description, asin, manufacturer])

            except Exception as e:
                print(f"Error while processing {product_url}: {str(e)}")

    # Implement rate limiting to avoid overloading the server
    time.sleep(2)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Manufacturer'])

# Save the data to a CSV file
df.to_csv('amazon_product_data.csv', index=False)
