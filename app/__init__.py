
from flask import Flask, jsonify,send_from_directory,request,BadRequestError

app = Flask(__name__)


from .kenzie.exceptions  import NotAllowedExtensionError, FileBiggerThan1MBError, FileAlreadyExistError

from .kenzie import image

number = int(image.content_length())
app.config['MAX_CONTENT_LENGTH'] =  number * 1024 * 1024

#------------------------------------------------ LIST --------------------------------------

@app.get('/files')
def list_files():
    files_list = image.list_all_files()   
    return jsonify({'data': files_list}) , 200
    

@app.get('/files/<string:extension>')
def list_image_by_extension(extension:str):
    try:
        return jsonify(image.list_by_extension(extension)), 200
    except NotAllowedExtensionError as err:
        return {"message": f'{err}' } , 404


#------------------------------------------------ DOWNLOAD --------------------------------------
@app.get('/download/<string:file_name>')
def download_image(file_name): 
    extension = image.get_extension(file_name)

    try:
        return send_from_directory(directory=f"../images/{extension}", path=file_name, as_attachment=True) , 201 
    except BadRequestError:
        return {"message": 'arquivo não existe, tente outro ' } , 404
   

@app.get('/download-zip')
def download_dir_as_zip():
    extension = request.args.get('file_extension') 
    image.download_zip_files(extension) 

    try:
        return send_from_directory(directory="/tmp", path=f"{extension}.zip", as_attachment=True), 201 
    except BadRequestError :
        return {"message": 'extensão não existe, tente uma válida ' } , 404

#------------------------------------------------ UPLOAD 

@app.post('/upload')
def upload_image(): 
   
    try:
        for file in request.files:
            filename= image.save_image(request.files[file] , request.content_length) 

            return {"message": f"Uploade de {filename} com sucesso"} , 201
    except FileBiggerThan1MBError as err:
        return {"message": f'{err}' } , 413 
    except NotAllowedExtensionError as err:
        return {"message": f'{err}' } , 415 
    except FileAlreadyExistError as err:
        return {"message": f'{err}' } , 409
    
   
