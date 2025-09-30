import os 
from pathlib import Path 
import logging 

logging.basicConfig(
    filename='setup',
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

project_name = "Network_Security"   

list_of_file = [
    "Network_Data/",
    f"{project_name}/__init__.py",
    f"{project_name}/cloud/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logging/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/utils/__init__.py",
    "notebooks/"
    'app.py',
    'main.py',
    'setup.py',
    'requirements.txt'
]

for filepath in list_of_file:
    filepath = Path(filepath)
    file_dir,file_name = os.path.split(filepath)

    if file_dir != "":
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f'Creating Directory :{file_dir} ot the {file_name}')
    if (not os.path.exists(filepath) or os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass 
        logging.info(f'Creating {filepath} is empty')
    else:
        logging.info(f'{filepath} already exists') 


'''
NETWORKSECURITY
│
├── .github/
├── Network_Data/
├── networksecurity/
│   ├── cloud/
│   ├── components/
│   ├── constant/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── pipeline/
│   ├── utils/
│   └── __init__.py
└── notebooks/

'''