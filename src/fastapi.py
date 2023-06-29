from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Union, Annotated

import logging
import uvicorn
import validators

from src.logging_utils import setup_logging
from src.chat import run as chat_run

# Set up logging
LOGGER = logging.getLogger(__name__)
LOGGER.info("Setting up logging configuration.")
setup_logging()

app = FastAPI()

# TODO: For front end, to be built later
# templates = Jinja2Templates(directory="templates")
# @app.get("/index/", response_class = HTMLResponse)
# def index(request: Request):
#     context = {'request': request}
#     return templates.TemplateResponse("index.html", context)

@app.on_event("startup")
def startup_event():
    LOGGER.info("Starting server...")
    LOGGER.info("Start server complete")


@app.post("/jobsearchgpt/generate_cover_letter")
def generate_cover_letter(
    url: str, experience: Annotated[List[str] | None, Query()] = None,
):
    """
    Retrieve cover letter generated with job description only or job description and work experience.

    Args:
        url (str): URL that leads to the linkedin listing to be scraped
        experience (str, optional): User's work experience. Defaults to None.

    Returns:
        Dict: a dictionary with the results key, which contains the generated cover letter.
    """
    valid_url = validators.url(url)
    if not valid_url:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail = "The URL provided does not exist."
        )
    LOGGER.info(f"Scraping job description from {url} and generating cover letter")
    response_payload =  {"result":chat_run(url, experience)}
    return response_payload

if __name__ == "__main__":
    uvicorn.run(
        "src.fastapi:app",
        host="0.0.0.0",
        reload=False,
        port=8000,
        log_level=None,
    )
