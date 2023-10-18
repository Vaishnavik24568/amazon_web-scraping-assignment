import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the product URLs from the CSV file
product_urls = pd.read_csv('amazon_products.csv')['Product URL']

# Initialize an empty list to store the data
product_data = []

# Loop through product URLs and scrape details
for url in product_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product details
    product_description = soup.find('div', {'id': 'productDescription'})
    if product_description:
        product_description = product_description.text.strip()
    else:
        product_description = "N/A"
    
    asin_element = soup.find('th', text='ASIN')
    if asin_element:
        asin = asin_element.find_next('td').text.strip()
    else:
        asin = "N/A"
    
    manufacturer_element = soup.find('th', text='Manufacturer')
    if manufacturer_element:
        manufacturer = manufacturer_element.find_next('td').text.strip()
    else:
        manufacturer = "N/A"
    
    product_data.append([url, product_description, asin, manufacturer])

# Create a DataFrame
product_df = pd.DataFrame(product_data, columns=['Product URL', 'Description', 'ASIN', 'Manufacturer'])

# Save the data to a CSV file
product_df.to_csv('amazon_product_details.csv', index=False)
