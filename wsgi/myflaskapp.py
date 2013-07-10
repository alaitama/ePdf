import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
#import metadata

UPLOAD_FOLDER = "./data"
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROPAGATE_EXCEPTIONS'] = True 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#@app.route('/')
#def hello_world():
#    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #metadata.printMeta(UPLOAD_FOLDER + '/' + filename)
            
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    
#@app.route('/metadata')
#def metadata_file(filename):
#    return metadata.printMeta(UPLOAD_FOLDER + '/' + filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
