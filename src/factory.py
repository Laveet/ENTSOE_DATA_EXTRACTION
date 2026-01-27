from src.base import EntsoeBaseFetcher
from src.price import PriceFetcher
from src.load import LoadFetcher
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