from dotenv import load_dotenv
import os

def env():
    print("Load environment . . . ")
    load_dotenv()  
    environment = {}
    environment["PROFILE"] = os.getenv("PROFILE")
    environment["DB_HOST"] = os.getenv("DB_HOST")
    environment["DB_USERNAME"] = os.getenv("DB_USERNAME")
    environment["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
    environment["DB_DATABASE"] = os.getenv("DB_DATABASE")
    return environment