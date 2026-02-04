# entsoe/load.py

import pandas as pd
from src.base import EntsoeBaseFetcher
import xml.etree.ElementTree as ET
from src.load.load_config import load_config


class LoadFetcher(load_config):
    """
    Fetches Actual Total Load (A65) from ENTSO-E for a given zone and time period.
    Only includes 15-min resolution data (PT15M).
    """

    def params(self):
        """Build ENTSO-E API parameters for actual total load"""
        params=self.parameters()
        params["processType"]="A16"
        return params


        # return {
        #     "documentType": "A65",                   # Actual Total Load
        #     "processType": "A16",        # Actual Total Load
        #     "outBiddingZone_Domain": self.zone,
        #     "periodStart": self.start,
        #     "periodEnd": self.end,
        #      # Actual Load
        # }

    def read_xml(self, root: ET.Element) -> pd.DataFrame:
        """Parse XML response and return DataFrame with timestamps and load values"""
        all_points = []

        for ts in root.findall(".//{*}TimeSeries"):
            period = ts.find("{*}Period")
            period_start_str = period.find("{*}timeInterval/{*}start").text
            period_start = pd.to_datetime(period_start_str)

            resolution_str = period.find("{*}resolution").text
            minutes = int(resolution_str[2:-1])  # PT60M -> 60, PT15M -> 15

            for point in period.findall("{*}Point"):
                position = int(point.find("{*}position").text)
                value = float(point.find("{*}quantity").text)
                timestamp = period_start + pd.Timedelta(minutes=(position - 1) * minutes)

                all_points.append({
                    "datetime_utc": timestamp,
                    "load_MW": value
                })

        if all_points:
            df = pd.DataFrame(all_points)
            df = df.sort_values("datetime_utc").reset_index(drop=True)
            return df
                
        else:
            pd.DataFrame(columns=["datetime_utc", "load_MW"])
            return df


    def output_file(self):
        return "load.csv"
    
# zone = "10YAT-APG------L"
# start = "202407272200"
# end   = "202407282200"

# Load=LoadFetcher(zone,start,end)
# df=Load.fetch_data()
# print(df.shape)
