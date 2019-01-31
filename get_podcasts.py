from bs4 import BeautifulSoup 
import requests 

landing_page = f"https://www.scientificamerican.com/podcast/60-second-science/?page=1"
source = requests.get(landing_page).text
soup = BeautifulSoup(source, 'lxml')

def download_mp3(mp3_link, title):
    title = "./downloads/" + title
    print(f"Downloading: {title}")
    doc = requests.get(mp3_link)
    with open(title, 'wb') as f:
        f.write(doc.content)


def scrape_page(): 

    for item in soup.find_all('div', class_='grid__col'):
        print("found something....trying to get link")

        try: 
            print(item['data-podcast-count'])
            mp3_link = item.section.a['href']
            title = item.section.h3.a['href'].split("/")[-2] + ".mp3"

            print(f"DEBUG: mp3_link={mp3_link}, title={title}")

            download_mp3(mp3_link, title)

        except Exception as e: 
            print(f"That one didn't work... {e}")

def get_total_pages():

    pages_soup = soup.find('ol', class_="pagination__nums")
    last_page =  pages_soup.find_all('li')[-1]
    total_pages = int(last_page.text)
    return total_pages

for page in (range(1, get_total_pages())):
    print(f"Scraping page: {page}")

    url = f"https://www.scientificamerican.com/podcast/60-second-science/?page={page}"

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')


    scrape_page()