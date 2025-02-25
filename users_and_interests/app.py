from flask import Flask, render_template
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    with open('users.yaml', 'r') as file:
        users = yaml.safe_load(file)
    return render_template('index.html', users)
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)