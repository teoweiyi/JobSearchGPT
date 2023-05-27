from typing import Union
import logging

from .coverletter import GeneralCoverLetter, ExperienceCoverLetter
from .scraper import JobDescription

logging.basicConfig(level=logging.INFO)

def run(url: str, 
        experience: Union[str, None] = None) -> str:
    """
    This function generates the cover letter based on:
    1. Job description scraped from the provided linkedin listing
    2. OR job description scraped from the provided linkedin listing, and user's work experience.

    Args:
        url (str): URL that leads to the linkedin listing to be scraped
        experience (Union[str, None]): User's work experience. Defaults to None.
    """ 
    # Get job description and title
    jd_getter = JobDescription(url)
    job_description = jd_getter.get_job_description()
    job_title = jd_getter.get_job_title()

    # Get cover letter based on job description only
    if experience == None:
        cover_letter = jd_generate(job_title, job_description)
    # Get cover letter based on both job description and work experience
    else:
        cover_letter = jd_exp_generate(job_title, job_description, experience)

    return cover_letter

def jd_generate(job_title, job_description):
    logging.info("running jd_generate")
    general_cover_letter = GeneralCoverLetter()
    cover_letter = general_cover_letter.chat(job_description, job_title)
    return cover_letter

def jd_exp_generate(job_title, job_description, experience):
    logging.info("running jd_exp_generate")
    experience_cover_letter = ExperienceCoverLetter()
    cover_letter = experience_cover_letter.chat(job_title, job_description, experience)
    return cover_letter

if __name__ == "__main__":
    run()