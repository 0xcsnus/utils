import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading

class Downloader(threading.Thread):
    def __init__(self, url, directory):
        threading.Thread.__init__(self)
        self.url = url
        self.directory = directory
    
    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_links = soup.find_all('a', href=lambda href: href.endswith('.pdf'))
            os.makedirs(self.directory, exist_ok=True)
            
            for link in pdf_links:
                pdf_url = urljoin(self.url, link['href'])
                pdf_name = pdf_url.split('/')[-1]
                pdf_path = os.path.join(self.directory, pdf_name)
                
                pdf_response = requests.get(pdf_url)
                
                with open(pdf_path, 'wb') as file:
                    file.write(pdf_response.content)
                
                print(f"Downloaded: {pdf_name}")
        else:
            print(f"Failed to access URL: {self.url}")

def download_pdfs(base_url, directory):
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print(f"Error accessing URL: {base_url}")
        return
    
    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href.endswith('.pdf'))
    
    if not pdf_links:
        print("No PDF files found.")
        return
    
    os.makedirs(directory, exist_ok=True)
    
    threads = []
    for link in pdf_links:
        pdf_url = urljoin(base_url, link['href'])
        thread = Downloader(pdf_url, directory)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print("Download completed successfully.")

base_url = 'url'
directory = 'dir'

download_pdfs(base_url, directory)
