from src.factory import Get_Data

# add data_type : either price pr load 
# zone
# start
# end

df = Get_Data.generation(zone="10YAT-APG------L",
    start="202502022000",
    end="202502022300")  # object created



print(df.shape)
