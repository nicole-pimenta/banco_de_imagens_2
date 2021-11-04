import os 

import dotenv 

dotenv.load_dotenv() 

FILES_DIRECTORY = os.environ.get("FILES_DIRECTORY") 
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY) 


for extension in ALLOWED_EXTENSIONS.split("."): 
    if not os.path.isdir(f'{FILES_DIRECTORY}/{extension}'):
      os.mkdir(f'{FILES_DIRECTORY}/{extension}')
