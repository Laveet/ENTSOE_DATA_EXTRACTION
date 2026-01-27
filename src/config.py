import os
from dotenv import load_dotenv
from src.exception import CustomException
import sys


load_dotenv()

try:
    url="https://web-api.tp.entsoe.eu/api"
    api_key=os.getenv("ENTSOE_API_KEY")
    data_path=os.path.join("data")
    os.makedirs(data_path,exist_ok=True)
    print(data_path)
except Exception as e:
    raise CustomException(e,sys)

