from flask import Flask, render_template, g
import yaml

app = Flask(__name__)

@app.before_request
def load_data():
    with open('users.yaml', 'r') as file:
        g.user_data = yaml.safe_load(file)
    
    g.total_users, g.total_interests = total_stats()

@app.route('/')
def home():
    user_names = [name for name in g.user_data.keys()]

    return render_template('home.html', user_names=user_names, user_data=g.user_data)

@app.route('/<user>')
def user_page(user):
    user_email = g.user_data[user]['email']
    user_interests_lst = g.user_data[user]['interests']
    user_interests = ', '.join(user_interests_lst)

    other_users = [name for name in g.user_data.keys() if name != user]

    return render_template('user_page.html', 
                           user=user, 
                           user_email=user_email,
                           user_interests=user_interests,
                           other_users=other_users)

def total_stats():

    total_users = len(g.user_data)
    total_interests = 0
    for data in g.user_data.values():
        total_interests += len(data['interests'])
    
    return (total_users, total_interests)

if __name__ == '__main__':
    app.run(debug=True, port=5003)