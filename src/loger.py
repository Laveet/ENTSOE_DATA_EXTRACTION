import logging
import os
from datetime import datetime


Log_file=f"{datetime.now().strftime('%m_%d_%Y_%H')}"
logs_path=os.path.join(os.getcwd(),"logs",Log_file)
os.makedirs(logs_path,exist_ok=True)
log_file_path=os.path.join(logs_path,Log_file)
logging.basicConfig(
    filename=log_file_path,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
    level=logging.INFO,
)

if __name__=="__main__":
    logging.info("logging is started")
