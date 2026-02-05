# from src.base import EntsoeBaseFetcher

# class load_config(EntsoeBaseFetcher):
#     def __init__(self, zone, start, end):
#         super().__init__(zone, start, end)
#         self.zone=zone
#         self.start=start
#         self.end=end
#     def parameters(self):
#         params={"documentType": "A65",                   # Actual Total Load
#                # Actual Total Load
#             "outBiddingZone_Domain": self.zone,
#             "periodStart": self.start,
#             "periodEnd": self.end
#             }
#         return params
#     def fetch_data(self):
#         return super().fetch_data()

