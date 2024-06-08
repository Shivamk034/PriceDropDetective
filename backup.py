from dotenv import load_dotenv
load_dotenv()
from datasets import load_dataset
from huggingface_hub import CommitScheduler
from huggingface_hub import HfApi
import os
import argparse

dataset_name = "shivam-kala/price-drop-detective-storage"
work_dir = "backup_dir"
dataset_save_path = "."

from git import Repo
import time

def push_to_hub():
    
    local_repo = Repo(work_dir)
    local_repo.git.add(all=True)
    print('Files Added Successfully') 
    local_repo.index.commit('Automatic backup commit')
    print('Commited successfully')
    origin = local_repo.remote(name='origin')
    origin.push()
    print('Pushed successfully')

def commit_scheduler(minutes=10):
    while(True):
        push_to_hub()
        time.sleep(minutes*60)


if __name__=="__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--schedule", help="push to hub scheduler every n minutes",type=int)
    args = parser.parse_args()

    if not args.schedule:
        push_to_hub()
    else:
        commit_scheduler(args.schedule)