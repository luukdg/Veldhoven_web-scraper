# importeer de benodigde libraries
import csv
import requests
from bs4 import BeautifulSoup
import time

# functie om de data van de website te scrapen
def scrape_pitt(url):
    
    # Een user agent om te zorgen dat je niet geblokkeerd wordt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Haal de HTML inhoud op van de website
    response = requests.get(url, headers=headers)
    time.sleep(2)

# controleer of de website goed bereikbaar is
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # zoek de titel naar de pagina
        title = soup.title.string
        print(f"De titel van de pagina is: {title}")

        address_tags = soup.find_all('h2', class_='objecttitle')
        addresses = [tag.text.strip() for tag in address_tags]

        price_tags = soup.find_all('strong')
        prices = [tag.text.strip() for tag in price_tags]
        
        image_tags = soup.find_all('img', class_='img-responsive')
        images = [img.get('src') for img in image_tags if '2025' in img.get('src', '')]

        combined_data = []
        for address, price, image in zip(addresses, prices, images):
            combined_data.append({
                'address': address,
                'price': price,
                'image': image
            })
        
        for item in combined_data:
            print(f"Address: {item['address']}, Price: {item['price']}, Image: {item['image']}")

        with open('pittmakelaars_aanbod.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["address", "price", "image"])
            writer.writeheader()
            writer.writerows(combined_data)
            print("Data saved to real_estate_data.csv")

    else:
        print(f"Het is niet gelukt. Status code: {response.status_code}")

# Dit zorgt ervoor dat de functie wordt
# uitgevoerd als je het script start    
if __name__ == "__main__":
    # hier geef je 'url' een betekenis
    url = "https://www.pitmakelaars.com/actueel-aanbod/"
    scrape_pitt(url)