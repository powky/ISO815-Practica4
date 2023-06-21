import datetime
import random
import json
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['unapec']
empls_collection = db['payments']

@app.route('/api/students/<college_name>', methods=['GET'])
def get_students(college_name):
    try:
        empls = list(empls_collection.find({'paid': True, 'college': college_name}))

        if not empls:
            return jsonify({'error': 'No existen datos.'}), 404

        report = {}
        report["students"] = []

        current_month = datetime.datetime.now().month
        if current_month <= 4:
            term = "202301"
        elif 5 <= current_month <= 8:
            term = "202302"
        else:
            term = "202303"

        total_amount = 0.0
        for emp in empls:
            student = {}
            student["name"] = emp["name"]
            student["id"] = emp["nationalId"]
            student["career"] = emp["career"]
            student["amount"] = float(emp["amount"])
            student["date"] = datetime.datetime.now().strftime('%Y-%m-%d')
            student["credits"] = emp["credits"]
            student["term"] = term

            total_amount += emp["amount"]
            report["students"].append(student)

        report["totalAmount"] = round(total_amount, 2)
        report["referenceNumber"] = str(random.randint(100000000, 999999999))

        return jsonify(report)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
