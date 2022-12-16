from functools import lru_cache
from fastapi import FastAPI
import config
import logging
import subprocess
import json
from pydantic import BaseModel
import openai


class Message(BaseModel):
    SubscriptionId: str
    Description: str

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

@lru_cache()
def get_settings():
    return config.AzSettings()

settings = get_settings()
openai.api_key = settings.openai_key

@app.get("/subscriptions")
async def get_subs():
    az_login_command = f"az login --service-principal -u {settings.azure_client_id} -p {settings.azure_client_secret} --tenant {settings.azure_tenant_id}"
    p = subprocess.Popen(az_login_command, stdout=subprocess.PIPE,
                         shell=True, universal_newlines=True)
    response = ""
    for line in p.stdout:
        response += line
    return json.loads(response)

@app.post("/message")
async def message(message: Message):
    try:
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f"az cli command to {message.Description} out format json",
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        logger.info(response._previous["choices"][0]
              ["text"].splitlines()[1].replace("+", ""))

        tmp_command = list(
            filter(None, response._previous["choices"][0]["text"].splitlines()))
        tmp_command = list(filter(lambda k: "az" in k, tmp_command))

        command = tmp_command[0].replace("+", "")

        logger.info(f"RUN: {command}\n")

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        response = ""
        for line in p.stdout:
            response += line
        
        return json.loads(response)

    except Exception as ex:
        logger.exception(str(ex))
        response = ex
        return response
