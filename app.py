
# Importing necessary libraries
from flask import Flask, render_template, request,redirect, url_for
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

client=MongoClient('mongodb://localhost:27017/')
db=client['ssss']
collection=db['aa']
@app.route('/')

def jk():
    return render_template('z.html')

@app.route('/submit', methods=['POST'])

@app.route('/submit', methods=['POST'])
def submit():
    if request.form['submit_button'] == 'LOG IN':
        return login()
    elif request.form['submit_button'] == 'SIGN UP':
        return signup()

# Signup
def signup():
    user = request.form['user']
    password = request.form['password']
    # Check if user already exists
    if collection.find_one({'user': user, 'password':password}):
        return "User already exists go to log in"
    else:
        collection.insert_one({'user': user, 'password': password})
        return render_template('ml.html')

# Login
def login():
    user = request.form['user']
    password = request.form['password']
    user_data = collection.find_one({'user': user, 'password': password})
    if user_data:
        return render_template('ml.html')
    else:
        return "Invalid credentials"
# Load the dataset from CSV file
data = pd.read_csv('House Price India.csv')

# Separate features (X) and target variable (y)
X = data[['number of bedrooms', 'Area of the house(excluding basement)', 'Area of the basement', 'number of views']]
y = data['Price']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model
model = LinearRegression()
model.fit(X_train, y_train)

# Define route to render HTML page
@app.route('/')
def index():
    return render_template('ml.html')

# Define route to handle form submission and make prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from form
    How_Many_No_Of_Rooms = int(request.form['room'])
    Area_of_the_house_excluding_basement = int(request.form['b'])
    Area_of_the_basement = int(request.form['c'])
    Direction_Of_House = int(request.form['d'])

    # Make prediction
    predicted_price = model.predict([[How_Many_No_Of_Rooms, Area_of_the_house_excluding_basement, Area_of_the_basement, Direction_Of_House]])
    predicted_price = int(predicted_price[0])

    # Render result template with predicted price
    return render_template('sss.html', predicted_price=predicted_price)

if __name__ == '__main__':
    app.run(debug=True)
