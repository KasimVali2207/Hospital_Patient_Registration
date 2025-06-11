from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Correct MongoDB Atlas URI
client = MongoClient("mongodb+srv://dudekulak43:Vali%406303per@cluster0.uecjcas.mongodb.net/?retryWrites=true&w=majority")

db = client["Hospital"]
patients = db["patients"]

@app.route('/')
def index():
    all_patients = list(patients.find())
    return render_template('index.html', patients=all_patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = {
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "disease": request.form['disease']
        }
        patients.insert_one(patient)
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<id>')
def edit_form(id):
    patient = patients.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', patient=patient)

@app.route('/update/<id>', methods=['POST'])
def update_patient(id):
    updated = {
        "name": request.form['name'],
        "age": request.form['age'],
        "gender": request.form['gender'],
        "disease": request.form['disease']
    }
    patients.update_one({"_id": ObjectId(id)}, {"$set": updated})
    return redirect('/')

@app.route('/delete/<id>')
def delete_patient(id):
    patients.delete_one({"_id": ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
