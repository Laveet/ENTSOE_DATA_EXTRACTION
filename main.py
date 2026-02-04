from src.factory import Get_Data

# add data_type : either price pr load 
# zone
# start
# end

df = Get_Data.load(zone="10YAT-APG------L",
    start="202602022200",
    end="202602032200")   # object created



print(df.shape)
