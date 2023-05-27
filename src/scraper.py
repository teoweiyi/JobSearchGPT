import requests
from bs4 import BeautifulSoup

class JobDescription:
    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self) -> None:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_job_description(self) -> str:
        job_description_element = self.soup.find_all("div", class_="description__text")
        job_description = [element.get_text().strip() for element in job_description_element]
        return job_description
    
    def get_job_title(self) -> str:
        job_title_element = self.soup.find("h1", class_="topcard__title")
        job_title = job_title_element.get_text().strip()
        return job_title
    