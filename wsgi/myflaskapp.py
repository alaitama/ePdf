import os
from flask import Flask, request, redirect, url_for, \
render_template, flash
from werkzeug import secure_filename
from flask import send_from_directory
import hashlib
import metadata

if not os.environ.has_key('OPENSHIFT_TMP_DIR'):
    UPLOAD_FOLDER = "./data"
else:
    UPLOAD_FOLDER = os.environ['OPENSHIFT_TMP_DIR']
    
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
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #flash('Ficheros procesado con exito.')
            
            docInfo = metadata.getMeta(app.config['UPLOAD_FOLDER'] + '/' + filename)
            
            return render_template('show_metadata.html', docInfo=docInfo)
        else:
            error = "Extension no permitida"
            
    return render_template('show_metadata.html', error=error)

    
@app.route('/metadata/<filename>')
def metadata_file(filename):
    metadata.printMeta(app.config['UPLOAD_FOLDER'] + '/' + filename)
    return 'hola'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
                               
@app.route('/generate', methods=['POST'])
def generate_file():
    #print request.form
    filenameInput = None
    filenameOutput = None
    file = request.files['file']
    if file and allowed_file(file.filename):
        filenameInput = secure_filename(file.filename) 
        # MD5 conversion name   
        m = hashlib.md5()    
        m.update(filenameInput)
        filenameOutput = m.hexdigest() + ".pdf" 
        
        #Save file in HD
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenameInput))
        
        #Modify metadadata file saves
        metadata.modifyMeta(app.config['UPLOAD_FOLDER'],filenameInput, filenameOutput, request.form)
        
    return redirect(url_for('uploaded_file', filename=filenameOutput))
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    #return render_template('show_metadata.html')

if __name__ == '__main__':
    app.run()
