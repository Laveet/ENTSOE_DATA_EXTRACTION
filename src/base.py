import requests
import pandas as pd
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from src.config import api_key,url,data_path
from src.exception import CustomException
from src.loger import logging
import sys
import os

class EntsoeBaseFetcher(ABC):
    def __init__(self,zone:str,start:str,end:str):
        self.zone=zone
        self.start=start
        self.end=end
    @abstractmethod
    def params(self)->dict:
        pass
    @abstractmethod
    def read_xml(self, root: ET.Element)->pd.DataFrame:
        pass
    @abstractmethod
    def output_file(self)->str:
        pass


    def fetch_data(self)->pd.DataFrame:
        try:

            params=self.params()
            params['securityToken']=api_key
            response=requests.get(url=url,params=params)
            root=ET.fromstring(response.content)
            df=self.read_xml(root)
            file_path=os.path.join(data_path,self.output_file())
            
            df.to_csv(file_path, index=False)
            logging.info(f"Data saved to {file_path}")

            return df
        except Exception as e:
            raise CustomException(e,sys)
        
        