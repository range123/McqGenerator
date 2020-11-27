# Final Year Engineering Undergrad Project

## Installation:
1. Download and unzip saved_models.zip in the root folder.
2. Create virtual environment using virtualenv and activate it.
```
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies.
..2.1. Install required pytorch package (cuda or cpu) from [PyTorch](https://pytorch.org/).
..2.2. Then install the rest of the requirements in requirements.txt.
```
pip install -r requirements.txt
```
..2.3. Download punkt using
```
python3 -m nltk.downloader punkt
```
3. Run the api and the frontend.
