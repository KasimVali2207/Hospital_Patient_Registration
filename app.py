from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MongoDB connection with secure TLS config
MONGO_URI = "mongodb+srv://dudekulak43:22BCB7285@cluster0.evbk2xf.mongodb.net/"
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())

# Database and collection
db = client["Hospital"]
patients = db["patients"]

# File upload config
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route - show all patients
@app.route('/')
def index():
    all_patients = list(patients.find())
    return render_template('index.html', patients=all_patients)

# Add patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = {
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "disease": request.form['disease'],
            "email": request.form.get('email', ''),
            "phone": request.form.get('phone', ''),
            "address": request.form.get('address', ''),
            "photo_url": ""
        }

        # Upload photo
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                patient["photo_url"] = url_for('static', filename=f'uploads/{filename}')

        patients.insert_one(patient)
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit patient form
@app.route('/edit/<id>')
def edit_form(id):
    patient = patients.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', patient=patient)

# Update patient
@app.route('/update/<id>', methods=['POST'])
def update_patient(id):
    updated = {
        "name": request.form['name'],
        "age": request.form['age'],
        "gender": request.form['gender'],
        "disease": request.form['disease'],
        "email": request.form.get('email', ''),
        "phone": request.form.get('phone', ''),
        "address": request.form.get('address', '')
    }

    # Upload new photo
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            updated["photo_url"] = url_for('static', filename=f'uploads/{filename}')

    patients.update_one({"_id": ObjectId(id)}, {"$set": updated})
    return redirect(url_for('index'))

# Delete patient
@app.route('/delete/<id>')
def delete_patient(id):
    patients.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
