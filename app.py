from flask import Flask, Blueprint, render_template, request
from kmeans import *
import os

train()

app = Flask(__name__)

main = Blueprint('main', __name__, static_folder='static', static_url_path='/lifestyleprediction/static')

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        sleep_enough = request.form.get('sleep_enough', '').strip()
        sleep_hours = request.form.get('sleep_hours', '').strip()
        phone_reach = request.form.get('phone_reach', '').strip()
        phone_use = request.form.get('phone_time', '').strip()
        tiredness = request.form.get('tiredness', '').strip()
        eat_breakfast = request.form.get('eat_breakfast', '').strip()

        # check if all fields are filled
        if not all([sleep_enough, sleep_hours, phone_reach, phone_use, tiredness, eat_breakfast]):
            error_message = 'Please fill all fields in the form.'
            return render_template('index.html', prediction_text=error_message)

        list = [int(sleep_hours), int(tiredness), int(sleep_enough), int(phone_reach), int(phone_use), int(eat_breakfast)]

        prediction = predicts(list)

        if prediction == 0:
            result_page = 'result1.html'
        elif prediction == 1:
            result_page = 'result2.html'
        elif prediction == 2:
            result_page = 'result3.html'
        elif prediction == 3:
            result_page = 'result4.html'
        else:
            result_page = 'landing.html'

        return render_template('index.html', prediction_text=prediction, result_page=result_page)

app.register_blueprint(main, url_prefix='/lifestyleprediction')

if __name__ == '__main__':
    # Use environment variable to specify the port number
    port = int(os.environ.get('PORT', 5000))
    # Use environment variable to specify whether to run in production mode
    is_production = os.environ.get('FLASK_ENV') == 'production'
    # Start the application
    app.run(host='0.0.0.0', port=port, debug=False)
