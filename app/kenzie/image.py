import os

import dotenv

from app.kenzie import ALLOWED_EXTENSIONS

dotenv.load_dotenv() 

from app.kenzie.exceptions import NotAllowedExtensionError , FileBiggerThan1MBError,FileAlreadyExistError

from flask.helpers import safe_join
from werkzeug.datastructures import FileStorage
from datetime import datetime , timezone
from werkzeug.utils import secure_filename


FILES_DIRECTORY = os.environ.get("FILES_DIRECTORY") 
MAX_CONTENT_LENGTH=os.environ.get("MAX_CONTENT_LENGTH") 
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")



def get_path(filename):
    return safe_join(FILES_DIRECTORY,filename)


def list_files(path):
    return  os.listdir(path)
    

def list_all_files():
    files_list = []

    for extensions_dir in os.listdir(FILES_DIRECTORY): 
        path = get_path(extensions_dir) 
        if list_files(path) != []:
            files_list.append(os.listdir(path))
            
    return files_list 


def list_by_extension(extension):
    allowed_extensions = ALLOWED_EXTENSIONS.split('.') 
    files_list = [] 


    if extension in allowed_extensions:
      for extensions_dir in os.listdir(FILES_DIRECTORY): 
        if extensions_dir == extension:
            path = get_path(extensions_dir)
            files_list.append(os.listdir(path))
    else:
        raise NotAllowedExtensionError("Extensão não permitida, tente outra!")

    return files_list 


def allowed_extensions():
    extensoes_permitidas = ALLOWED_EXTENSIONS.split('.')
    return list(extensoes_permitidas)


def get_extension(filename:str):
    extension = filename.split(".")[-1] 
    return extension 


def verify_extension(file:FileStorage):
    file_extension = file.filename.split(".")[-1]
    return file_extension


def check_if_empty_repo_exist():
    all_directories = os.listdir(FILES_DIRECTORY) 
    verify = [ ]

    for directories in all_directories:
        verify.append(os.path.isfile(directories))

    return all(verify)   


def save_image(file: FileStorage , length): 
    allowed_extensions = ALLOWED_EXTENSIONS.split('.') 
    file_extension = file.filename.split(".")[-1] 
    filename = str(file.filename) 
    lista = []

    for files in list_all_files(): 
        lista.append(files) 
    
    if length < 100000:
        path = safe_join(FILES_DIRECTORY, f'{file_extension}/{filename}') 
        file.save(path)
    if length > 100000:
        raise FileBiggerThan1MBError('Arquivo maior que 1MB')
    if file_extension  not in allowed_extensions:
        raise NotAllowedExtensionError("Extensão não permitida, tente outra!")
    if filename in lista[0]:
            raise FileAlreadyExistError('Arquivo com nome já existente')
    

    return filename


def download_zip_files(extension):   
    os.system(f'zip -r /tmp/{extension}.zip images/{extension}')

       
def content_length():
    return MAX_CONTENT_LENGTH
    
    

