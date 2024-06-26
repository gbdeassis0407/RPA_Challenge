from robocorp.tasks import task
import requests
import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@task
def site():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador = webdriver.Chrome()
    
    search = "dolar"  # o que pesquisar 

    try:
        # Abre a página desejada
        navegador.get("https://apnews.com")

        WebDriverWait(navegador, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/button'))
        )
        
        # Interage com a página
        navegador.find_element(By.XPATH, '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/button').click()
        search_input = navegador.find_element(By.XPATH, '//*[@id="Page-header-trending-zephr"]/div[2]/div[3]/bsp-search-overlay/div/form/label/input')
        search_input.send_keys(search)
        search_input.send_keys(Keys.ENTER)
        
        WebDriverWait(navegador, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/main/div[1]/span'))
        )
        
        # Captura a nova URL
        url = navegador.current_url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"}

        # Obter o conteúdo HTML da página
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas as notícias na página
        articles = soup.find_all('div', class_='PagePromo')
        timestamp_elements = soup.find_all('bsp-timestamp')
        
        print("Site carregado e pesquisa realizada com sucesso.")
    except Exception as e:
        print("Erro ao carregar o site ou encontrar elementos:", str(e))
    finally:
        navegador.quit()
        
    return articles, timestamp_elements, search

def find_dolar(texto):
    if texto is None:
        return False
    padrao = r'\$[\d,]+|\b\d+\s+dólares\b'
    res = re.findall(padrao, texto)
    return bool(res)

def date_collect(timestamp_elements):
    dates = []
    for timestamp in timestamp_elements:
        if timestamp.has_attr('data-timestamp'):
            date_element = int(timestamp['data-timestamp']) / 1000  
            date = datetime.utcfromtimestamp(date_element).strftime('%Y-%m-%d')
            dates.append(date)
        else:
            dates.append('N/A')
    return dates
    
def cont_collect(articles, search):
    titles = []
    descriptions = []
    image_urls = []
    title_counts = []
    description_counts = []
    title_dolars = []
    description_dolars = []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    
    for article in articles:
        text_elements = article.find_all('span', class_='PagePromoContentIcons-text')
        
        if len(text_elements) >= 2:
            title = text_elements[0].text.strip()
            description = text_elements[1].text.strip()
        else:
            title = text_elements[0].text.strip() if len(text_elements) > 0 else 'N/A'
            description = 'N/A'
        
        title_dolar = find_dolar(title)
        description_dolar = find_dolar(description)
        
        title_count = len(pattern.findall(title))
        description_count = len(pattern.findall(description))
        
        image_element = article.find('img', class_='Image')
        image_url = image_element.get('src') if image_element else 'N/A'
        
        titles.append(title)
        descriptions.append(description)
        image_urls.append(image_url)
        title_counts.append(title_count)
        description_counts.append(description_count)
        title_dolars.append('T' if title_dolar else 'F')
        description_dolars.append('T' if description_dolar else 'F')
        
    return titles, descriptions, image_urls, title_counts, description_counts, title_dolars, description_dolars

def download_img(url, destination_folder, cont):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            file_name = f"image_{cont}.jpg"
            file_path = os.path.join(destination_folder, file_name)
            
            with open(file_path, 'wb') as arquivo:
                arquivo.write(response.content)                
            print(f"Imagem '{file_name}' baixada e salva com sucesso em '{destination_folder}'.")
            return file_path
        else:
            print(f"Falha ao baixar a imagem '{url}': {response.status_code}")
            return 'N/A'
    except Exception as e:
        print(f"Erro ao baixar a imagem '{url}': {e}")
        return 'N/A'

def dados():
    main_folder = 'Data'
    os.makedirs(main_folder, exist_ok=True)

    articles, timestamp_elements, search = site()
    titles, descriptions, image_urls, title_counts, description_counts, title_dolars, description_dolars = cont_collect(articles, search)
    dates = date_collect(timestamp_elements)

    max_length = max(len(titles), len(dates), len(descriptions), len(image_urls), len(title_counts), len(description_counts))

    titles += ['N/A'] * (max_length - len(titles))
    dates += ['N/A'] * (max_length - len(dates))
    descriptions += ['N/A'] * (max_length - len(descriptions))
    image_urls += ['N/A'] * (max_length - len(image_urls))
    title_counts += [0] * (max_length - len(title_counts))
    description_counts += [0] * (max_length - len(description_counts))

    destination_folder = os.path.join(main_folder, 'img_news')
    os.makedirs(destination_folder, exist_ok=True)

    local_image_paths = []

    cont = 1
    for image_url in image_urls:
        if image_url != 'N/A':
            local_image_path = download_img(image_url, destination_folder, cont)
            local_image_paths.append(local_image_path)
            cont += 1
        else:
            local_image_paths.append('N/A')

    df = pd.DataFrame({
        'Title': titles,
        'Date': dates,
        'Description': descriptions,
        'Image URL': image_urls,
        'Local Image Path': local_image_paths,
        'Title Count': title_counts,
        'Description Count': description_counts,
        'Has Dollars in Title': title_dolars,  
        'Has Dollars in Description': description_dolars 
    })

    excel_file = os.path.join(main_folder, 'news_data.xlsx')
    df.to_excel(excel_file, index=False)

    print(f'Dados coletados e salvos em {excel_file} e imagens na pasta {destination_folder}')

dados()