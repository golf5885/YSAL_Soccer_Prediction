from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your CSV file
df = pd.read_csv('C:/Users/user/Desktop/YSAL/Score_Time/filtered_four_leagues_data.csv')

def find_similar_rows(home_betting_odds, away_betting_odds, tolerance):
    similar_rows = df[
        ((df['B365H'] >= home_betting_odds - tolerance) & (df['B365H'] <= home_betting_odds + tolerance)) &
        ((df['B365A'] >= away_betting_odds - tolerance) & (df['B365A'] <= away_betting_odds + tolerance))
    ]
    return similar_rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    input_home_odds = float(request.form['home_odds'])
    input_away_odds = float(request.form['away_odds'])

    result_rows = find_similar_rows(input_home_odds, input_away_odds, 0.25)
    
    result_rows = result_rows.fillna('')

    if not result_rows.empty:
        return render_template('result.html', rows=result_rows)
    else:
        return render_template('result.html', message="No similar results found.")

if __name__ == '__main__':
    app.run(debug=True)
