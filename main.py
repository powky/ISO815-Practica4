import requests
import cx_Oracle
import json
import os

# Conexión DB
os.environ['TNS_ADMIN'] = '/Users/fernandez/instantclient_19_8/network/admin'
connection = cx_Oracle.connect('ADMIN', 'Iso815810unapec', 'iso8xx_high')

# URL WebService
url = 'http://127.0.0.1:5001/api/students/unapec'

# Consumir con GET
response = requests.get(url)

# Reviso si recibo HTTP 200
if response.status_code == 200:
    data = response.json()

    # Parsear la info del JSON retornado
    students = data['students']
    reference_number = data['referenceNumber']

    # Iterando sobre el JSON para hacer insert
    for student in students:
        name = student['name']
        doc_num = student['id']
        career = student['career']
        terms = student['term']
        credits = student['credits']
        amount = student['amount']
        insert_date = student['date']

        # Insert a la DB
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO fundapec_pymts (NAME, DOC_NUM, CAREER, TERMS, CREDITS, AMOUNT, REF_NUM, INSERT_DATE)
            VALUES (:1, :2, :3, :4, :5, :6, :7, TO_DATE(:8, 'YYYY-MM-DD'))
        """, (name, doc_num, career, terms, credits, amount, reference_number, insert_date))
        connection.commit()
        cursor.close()

    # Cerrar la DB
    connection.close()

    print("Consumido e insertado correctamente.")
else:
    print("El WebService no responde.")
