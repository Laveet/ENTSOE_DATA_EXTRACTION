from src.factory import DataFetcherFactory

# add data_type : either price pr load 
# zone
# start
# end

fetcher = DataFetcherFactory.create(data_type="price",zone="10YAT-APG------L",
    start="202307252200",
    end="202307252300")   # object created
df = fetcher.fetch_data()   


print(df.shape)
