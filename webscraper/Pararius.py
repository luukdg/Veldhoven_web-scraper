# Importeer de benodigde libraries
import requests
from bs4 import BeautifulSoup
import csv
import time

# Functie om de data van de website te scrapen
def scrape_pitt():
    base_url = "https://www.pararius.nl/koopwoningen/veldhoven/p"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    all_data = []  # Hier slaan we alle verzamelde data op

    for page in range(1, 6):  # Scrape pagina 1 t/m 5
        url = f"{base_url}{page}"
        response = requests.get(url, headers=headers)
        time.sleep(2)  # Voorkom blokkering door te wachten tussen requests

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Zoek en verzamel data
            address_tags = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')
            addresses = [tag.text.strip() for tag in address_tags]

            price_tags = soup.find_all('div', class_='listing-search-item__price')
            prices = [tag.text.strip() for tag in price_tags]

            image_tags = soup.find_all('img', class_='picture__image')
            images = [img.get('src') for img in image_tags if img.get('src', '')]

            for address, price, image in zip(addresses, prices, images):
                all_data.append({'address': address, 'price': price, 'image': image})
            
            print(f"Pagina {page} verwerkt, {len(addresses)} woningen gevonden.")
        
        else:
            print(f"Fout bij pagina {page}, status code: {response.status_code}")

    # Sla de verzamelde data op in een CSV-bestand
    with open('pararius_aanbod.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["address", "price", "image"])
        writer.writeheader()
        writer.writerows(all_data)

    print("Alle data opgeslagen in pararius_aanbod.csv")

# Voer de functie uit als het script wordt gestart
if __name__ == "__main__":
    scrape_pitt()
