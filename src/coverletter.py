import openai
import os
import logging

# get the API key from the environment variable
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# set the API key for the openai authentication
openai.organization = OPENAI_ORGANIZATION_ID
openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

class CoverLetter:
    def __init__(self) -> None:
        self.message_history = [{"role":"user","content":"You are a bot that generates cover letters when given a job description. \
                                    Reply only with a generated cover letter to further input. If you understand, say OK"},
                                    {"role":"assistant","content":"OK"}]

    def chat(self, job_title, job_description, experience = None, role="user") -> str:
        inp = f"The job title is: {job_title}. The job description is: {job_description}"
        self.message_history.append({"role": role, "content": inp})
        if experience:
            self.message_history.append({"role":role, "content": f"My experience is as follows: {experience}"})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_history
        )

        reply_content = completion.choices[0].message.content
        self.message_history.append({"role": "assistant", "content":reply_content})
        return reply_content

class GeneralCoverLetter(CoverLetter):
    def __init__(self) -> None:
        super().__init__()

class ExperienceCoverLetter(CoverLetter):
    def __init__(self) -> None:
        super().__init__()
        self.message_history = [{"role":"user","content":"You are a bot that generates cover letters when given a job description, followed by a resume. \
                            Include only experiences from the resume that are relevant to the job description. \
                            Reply only with a generated cover letter to further input. If you understand, say OK"},
                            {"role":"assistant","content":"OK"}]
        