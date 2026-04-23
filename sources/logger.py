import os
import logging
from datetime import datetime

LOG_File = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_Path = os.path.join(os.getcwd(), "logs", LOG_File)
os.makedirs(LOG_Path, exist_ok=True)

LOG_File_Path = os.path.join(LOG_Path, LOG_File)

logging.basicConfig(
    filename=LOG_File_Path,
    format="[%(asctime)s] %(lineno)d %(name)s %(levelname)s - %(message)s",
    level=logging.INFO,
)
