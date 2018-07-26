# now-serving-text-classifications

## Setup

### Git

If the repo has not already been installed, use the following commands to clone the repository and change to the directory.

    git clone git@github.com:orlmlds/now-serving-text-classifications.git
    cd now-serving-text-classifications/

### Python

This project requires python 3.6+. Confirm your python version by running:

    python --version
    
Use the requirements file to download project dependencies.
    
    pip install -r requirements.txt
    
Use the embeddings library to download the embeddings. **NOTE:** This command downloads a large file ~2GB and may take a while to complete. If the command does not begin a download, the file already exists.

    python NowServing/scripts/create_embeddings.py  

### Downloads 
Download the Consumer Complaint Database (589.4 MB) file from [here](https://catalog.data.gov/dataset/consumer-complaint-database). This will be used in the bag of words classifier. 

## Run

WIP