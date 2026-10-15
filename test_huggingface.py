import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()

token = os.getenv("HF_TOKEN")

if not token:
    print("ERROR: HF_TOKEN was not found in .env")
else:
    try:
        api = HfApi(token=token)
        user = api.whoami()

        print("Hugging Face connection successful!")
        print("Logged in as:", user["name"])

    except Exception as error:
        print("Connection failed.")
        print("Error type:", type(error).__name__)
        print("Check your token and permissions.")