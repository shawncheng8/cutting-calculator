from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract data from form
    current_weight = float(request.form['current_weight'])
    current_bf_perc = float(request.form['current_bf_perc'])
    goal_bf_perc = float(request.form['goal_bf_perc'])
    
    # Handle optional input with a default value
    perc_weight_lost_as_fat_input = request.form.get('perc_weight_lost_as_fat', '75')  # Use a string '75' as default
    perc_weight_lost_as_fat = float(perc_weight_lost_as_fat_input if perc_weight_lost_as_fat_input else '75')
    
    rate_of_weight_loss_input = request.form.get('rate_of_weight_loss', '1')  # Use a string '1' as default
    rate_of_weight_loss = float(rate_of_weight_loss_input if rate_of_weight_loss_input else '1')

    # Your calculation logic
    weight_to_lose = (current_weight * current_bf_perc / 100.0 - goal_bf_perc / 100.0 * current_weight) / (perc_weight_lost_as_fat / 100.0 - goal_bf_perc / 100.0)
    
    today = datetime.date.today()
    days_to_lose_weight = weight_to_lose / (rate_of_weight_loss / 7)
    finish_date = today + datetime.timedelta(days=days_to_lose_weight)

    final_weight = round(current_weight - weight_to_lose, 1)
    weight_to_lose = round(weight_to_lose, 1)

    # Prepare values to send back
    values = {
        'current_weight': current_weight,
        'current_bf_perc': current_bf_perc,
        'goal_bf_perc': goal_bf_perc or 75,  # Ensure there's a default if goal_bf_perc is empty
        'perc_weight_lost_as_fat': perc_weight_lost_as_fat,
        'rate_of_weight_loss': rate_of_weight_loss,
        'finish_date': finish_date,
        'weight_to_lose': weight_to_lose,
        'final_weight': final_weight
    }

    return render_template('index.html', **values)

if __name__ == '__main__':
    app.run(debug=True)
