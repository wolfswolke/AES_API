from flask_definitions import *


@app.route('/', methods=['GET'])
def home():
    # File at src/static/html/index.html
    return render_template('index.html')
