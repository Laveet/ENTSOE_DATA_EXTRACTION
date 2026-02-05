import xml.etree.ElementTree as ET
import pandas as pd
from src.base import EntsoeBaseFetcher
from datetime import timedelta

class GenerationFetcher(EntsoeBaseFetcher):
    
    def params(self):
        """Build ENTSO-E API parameters for price"""

        return {
            "documentType": "A75",
            "processType": "A16",

            "in_Domain": self.zone,
            "periodStart": self.start,
            "periodEnd": self.end,
            
        }
    def read_xml(self, root):
        PSR_MAP = {
            "B01": "biomass",
            "B02": "lignite",
            "B04": "gas",
            "B05": "hard_coal",
            "B10": "hydro_pumped",
            "B11": "hydro_ror",
            "B12": "hydro_reservoir",
            "B14": "nuclear",
            "B16": "solar",
            "B18": "wind_offshore",
            "B19": "wind_onshore",
            "B25": "storage"
        }
        NS = "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"

        def ns_tag(tag):
            return f"{{{NS}}}{tag}"
        
        records = []

        for ts in root.findall(f".//{ns_tag('TimeSeries')}"):

            psr_elem = ts.find(f"{ns_tag('MktPSRType')}/{ns_tag('psrType')}")
            if psr_elem is None:
                continue

            psr_code = psr_elem.text
            psr_name = PSR_MAP.get(psr_code, psr_code)

            period = ts.find(ns_tag("Period"))
            resolution = period.find(ns_tag("resolution")).text

            if resolution != "PT15M":
                continue

            start_time = pd.to_datetime(
                period.find(f"{ns_tag('timeInterval')}/{ns_tag('start')}").text
            )

            step = timedelta(minutes=15)

            for point in period.findall(ns_tag("Point")):
                position = int(point.find(ns_tag("position")).text)
                value = float(point.find(ns_tag("quantity")).text)

                timestamp = start_time + (position - 1) * step

                records.append({
                    "datetime_utc": timestamp,
                    "psr": psr_name,
                    "value": value
                })

        df_wide = (
                    pd.DataFrame(records)
                    .pivot_table(
                        index="datetime_utc",
                        columns="psr",
                        values="value",
                        aggfunc="sum"
                    )
                    .reset_index()
                )
        return df_wide
         



    def output_file(self):
        return "generation.csv"
    




# zone = "10YAT-APG------L"
# start = "20240727200"
# end   = "202407272300"


# Generation=GenerationFetcher(zone,start,end)
# df=Generation.fetch_data()
# print(df.shape)