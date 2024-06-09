import logging
import os, sys
from pathlib import Path

# logging
__LOGFILE_PATH = Path('backup_dir/logs.txt')
if not os.path.exists(__LOGFILE_PATH):
    os.makedirs(__LOGFILE_PATH.parent,exist_ok=True)
    open(__LOGFILE_PATH,"w").close()

__logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

logging.basicConfig(
    level= logging.INFO,
    format= __logging_str,

    handlers=[
        logging.FileHandler(__LOGFILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
