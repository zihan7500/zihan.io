#! C:\Users\arahm\AppData\Local\Programs\Python\Python311\python.exe
from flask import Flask, render_template, request, redirect
import mysql.connector
import webbrowser

app = Flask(__name__)

# Function to calculate tuition fee
def calculate_tuition_fee(cgpa, credits, address):
    # Replace with your actual tuition fee calculation logic
    base_fee = 1000
    is_west_virginia = (address == 'West Virginia')
    credit_multiplier = 200 if is_west_virginia else 400
    cgpa_discount = 200 if cgpa >= 3.0 else 0

    tuition_fee = base_fee + (credit_multiplier * credits) - cgpa_discount
    return tuition_fee

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        student_id = request.form['ID']

        mydb =  mysql.connector.connect(
            host = "Localhost",
            user = 'root',
            password = "Themistocles1!",
            database = "tutionfee"

        )
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM student_info WHERE ID = '{student_id}' AND first_name='{first_name}' AND last_name= '{last_name}'")
        myresult = mycursor.fetchall()

        print(myresult)

        if myresult:
            # Fetch the data
            student_data = myresult[0]

            # Calculate tuition fee
            tuition_fee = calculate_tuition_fee(student_data[6], student_data[7], student_data[5])

            # Display the result
            return render_template('result.html', 
                first_name=first_name, last_name=last_name,
                cgpa=student_data[6], credits=student_data[7],
                address=student_data[5], tuition_fee=tuition_fee)
        else:
            return "No matching record found in the database."

    return render_template('index.html')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)


