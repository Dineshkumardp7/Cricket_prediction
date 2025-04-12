from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi',
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        current_score = int(request.form['current_score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])
        last_five = int(request.form['last_five'])

        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs

        # Using try-except for handling missing form data
        try:
            batting_team_strength = float(request.form['batting_team_strength'])
        except KeyError:
            batting_team_strength = 0.0  # Default value if field is missing

        try:
            bowling_team_strength = float(request.form['bowling_team_strength'])
        except KeyError:
            bowling_team_strength = 0.0  # Default value if field is missing

        try:
            venue_avg_runs = float(request.form['venue_avg_runs'])
        except KeyError:
            venue_avg_runs = 0.0  # Default value if field is missing

        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
             'current': [current_score], 'no_of_balls_left': [balls_left],
             'wickets_left': [wickets_left], 'current_run_rate': [crr], 'last_30_runs': [last_five],
             'batting_team_strength': [batting_team_strength], 'bowling_team_strength': [bowling_team_strength],
             'venue_avg_runs': [venue_avg_runs]}
        )

        result = pipe.predict(input_df)
        prediction = int(result[0])

    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
