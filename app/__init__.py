from flask import Flask, jsonify,send_from_directory,request

app = Flask(__name__)

from .kenzie import image

number = int(image.content_length())
app.config['MAX_CONTENT_LENGTH'] =  number * 1024 * 1024

#------------------------------------------------ LIST --------------------------------------

@app.get('/files')
def list_files():
    dir_list = image.list_all_files() 
    files_list = []

    for files in dir_list:
        path = image.get_path(files)
        files_list.append(image.list_files(path))

    return dict(zip(dir_list,files_list)), 200


@app.get('/files/<string:extension>')
def list_image_by_extension(extension:str):
    dir_list = image.list_all_files()
    extension = image.get_extension(extension)
    output = []

    for files in dir_list: 
        if files == extension:
            path = image.get_path(files)
            lista = image.list_files(path)
            for images in lista:
                output.append(images)
        
    try:
        return jsonify(output), 200
    except:
        return {"message":f' A extensão {extension} nao existe'}, 404


#------------------------------------------------ DOWNLOAD --------------------------------------

@app.get('/download/<string:file_name>')
def download_image(file_name):
    extension = image.get_extension(file_name)
    path = image.get_path(extension) 

    try:
        return send_from_directory(directory=f"{path}", path=file_name, as_attachment=True), 200 
    except:
        return {"message":f' O arquivo {file_name} nao existe'}, 404


@app.get('/download-zip')
def download_dir_as_zip():
    extension = request.args.get('file_extension') 
    path = image.get_path(extension) 

    image.download_zip_files(extension) , 200 

    send_from_directory(directory="/tmp", path=f"{extension}.zip", as_attachment=True), 200 

    return {"message":'download diretório .zip feito com sucesso !'}, 201


#------------------------------------------------ UPLOAD 

@app.post('/upload')
def upload_image(): 
    files_list = []
    
    for file in request.files:
        filename= image.save_image(request.files[file]) 
        files_list.append(filename)
    
    if request.content_length < 100000:
        return jsonify(files_list) , 201
    else:
        return {"msg": "tamanho nao suportado"}
