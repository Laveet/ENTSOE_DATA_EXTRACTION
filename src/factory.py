from src.base import EntsoeBaseFetcher
from src.price.price import PriceFetcher
from src.load.load import LoadFetcher
from src.exception import CustomException
import sys

class DataFetcherFactory:
    """Factory to create ENTSO-E data fetchers"""
    try:

        @staticmethod
        def create(data_type: str,zone,start,end) -> EntsoeBaseFetcher:
            data_type = data_type.lower()
            if data_type == "price":
                return PriceFetcher(zone,start,end)
            elif data_type == "load":
                return LoadFetcher(zone,start,end)
            else:
                raise ValueError(f"Data type {data_type} is not supported yet.")
    except Exception as e:
        raise CustomException(e,sys)
    
class Get_Data:
    """
    Public interface for users.
    This is what main.py should use.
    """

    @staticmethod
    def price(zone: str, start: str, end: str):
        fetcher = DataFetcherFactory.create("price",zone,start,end)
        return fetcher.fetch_data()

    @staticmethod
    def load(zone: str, start: str, end: str):
        fetcher = DataFetcherFactory.create("load",zone,start,end)
        return fetcher.fetch_data()