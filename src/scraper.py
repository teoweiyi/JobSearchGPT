import requests
import bs4
import logging
logging.basicConfig(level=logging.INFO)

class JobDescription:
    """
    A scraper to extract the job description of a posting based on a linkedin url.
    """
    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self) -> bs4:
        """
        A function to get a reponse object from the provided linkedin url

        Returns:
            bs4 : response object of the job posting
        """
        response = requests.get(self.url)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_job_description(self) -> str:
        """
        Retrieves job description from response content.

        Returns:
            str: job description from provided linkedin url
        """
        job_description_element = self.soup.find_all("div", class_="description__text")
        job_description = [element.get_text().strip() for element in job_description_element]
        return job_description
    
    def get_job_title(self) -> str:
        """
        Retrieves job title from response content.

        Returns:
            str: job title from provided linkedin url
        """
        job_title_element = self.soup.find("h1", class_="topcard__title")
        job_title = job_title_element.get_text().strip()
        return job_title
    