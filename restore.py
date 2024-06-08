from dotenv import load_dotenv
load_dotenv()
from huggingface_hub import snapshot_download
from pathlib import Path
import os

dataset_name = "shivam-kala/price-drop-detective-storage"
work_dir = "backup_dir"
dataset_save_path = "."

# snapshot_download(
#                     repo_id=dataset_name,
#                     repo_type="dataset",
#                     local_dir=work_dir,
#                 )

import git

# Clone a remote repository 
repo_url = "https://USERNAME:${{HF_TOKEN}}@huggingface.co/datasets/{dataset_name}".format(dataset_name=dataset_name)
print(repo_url)
repo = git.Repo.clone_from(repo_url, work_dir) 
print(f'Repository Cloned at location: {work_dir}')