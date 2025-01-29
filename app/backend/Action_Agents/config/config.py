import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FAISS_PATH = "faiss_db_opt"  # Or wherever you want to store your FAISS DB
