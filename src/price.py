import xml.etree.ElementTree as ET
import pandas as pd
from src.base import EntsoeBaseFetcher

class PriceFetcher(EntsoeBaseFetcher):
    
    def params(self):
        """Build ENTSO-E API parameters for price"""
        return {
            "documentType": "A44",
            "in_Domain": self.zone,
            "out_Domain": self.zone,
            "periodStart": self.start,
            "periodEnd": self.end,
            "contract_MarketAgreement.type": "A01"
        }
    def read_xml(self, root: ET.Element):
        all_points = []
        for ts in root.findall(".//{*}TimeSeries"):
            period = ts.find("{*}Period")
            period_start_str = period.find("{*}timeInterval/{*}start").text
            period_start = pd.to_datetime(period_start_str)
            
            resolution_str = period.find("{*}resolution").text
            minutes = int(resolution_str[2:-1])
            
            for point in period.findall("{*}Point"):
                position = int(point.find("{*}position").text)
                price = float(point.find("{*}price.amount").text)
                timestamp = period_start + pd.Timedelta(minutes=(position - 1) * minutes)
                all_points.append({
                    "datetime_utc": timestamp,
                    "price_EUR_MWh": price
                })
        
        df = pd.DataFrame(all_points)
        df = df.sort_values("datetime_utc").reset_index(drop=True)
        return df

    def output_file(self):
        return "price.csv"
    

# zone = "10YAT-APG------L"
# start = "202407272200"
# end   = "202407282200"


# price=PriceFetcher(zone,start,end)
# df=price.fetch_data()
# print(df.shape)