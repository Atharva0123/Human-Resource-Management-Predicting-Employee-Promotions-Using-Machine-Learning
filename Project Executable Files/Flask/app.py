import pickle
from flask import Flask, render_template, request
from sklearn.preprocessing import LabelEncoder

# Load the model
model = pickle.load(open(r'Flask\model.pkl', 'rb'))

le = LabelEncoder()
departments = ['Sales & Marketing', 'Operations', 'Technology', 'Analytics', 'R&D', 'Procurement', 'Finance', 'HR', 'Legal']
le.fit(departments)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def home1():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    return render_template('predict.html', department_options=departments)

def preprocess_department(department):
    # Transform the department using the pre-trained LabelEncoder
    return le.transform([department])[0]

@app.route('/pred', methods=['POST'])
def pred():
    department = preprocess_department(request.form['department'])
    education = int(request.form['education'])
    no_of_trainings = int(request.form['no_of_trainings'])
    age = int(request.form['age'])
    previous_year_rating = float(request.form['previous_year_rating'])
    length_of_service = float(request.form['length_of_service'])
    KPIs = int(request.form['KPIs'])
    awards_won = int(request.form['awards_won'])
    avg_training_score = float(request.form['avg_training_score'])

    total = [[department, education, no_of_trainings, age, previous_year_rating, length_of_service,
              KPIs, awards_won, avg_training_score]]
    
    prediction = model.predict(total)
    
    if prediction == 0:
        text = "Oops! It looks like this time, the stars have other plans for you.Hold tight for the next opportunity!"
    else:
        text = "Woo-hoo! Your career trajectory is about to take off like a rocket.Congratulations on earning your well-deserved promotion!🚀🚀🚀"

    
    return render_template('submit.html', predictionText=text)

@app.route('/submit')
def submit():
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
