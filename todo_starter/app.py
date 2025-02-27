from uuid import uuid4
from functools import wraps
import os

from flask import (Flask, 
                   render_template, 
                   redirect, 
                   url_for,
                   session,
                   request,
                   flash)

from todos.utils import (error_for_list_title, 
                         find_list_by_id, 
                         error_for_todo_title,
                         todos_remaining,
                         is_list_completed,
                         is_todo_completed,
                         sort_items,
                         )

app = Flask(__name__)
app.secret_key='secret1'

def require_list(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        list_id = kwargs.get('list_id')
        lst = find_list_by_id(list_id, session['lists'])
        if not lst:
            return 'Not Found'
        return f(lst=lst, *args, **kwargs)
    return decorated_function

def require_todo(f):
    @wraps(f)
    @require_list
    def decorated_function(lst, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo = find_list_by_id(todo_id, lst['todos'])
        if not todo:
            return 'Not Found'
        return f(lst=lst, todo=todo, *args, **kwargs)
    return decorated_function

@app.context_processor
def list_utilities_processor():
    return dict(
        is_list_completed=is_list_completed
    )

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route('/lists')
def get_lists():
    lists = sort_items(session['lists'], is_list_completed)
    return render_template('lists.html', 
                           lists=lists,
                           todos_remaining=todos_remaining)

@app.route('/lists/new')
def add_todo_list():
    return render_template('new_list.html')

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form['list_title'].strip()

    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, 'error')
        return render_template('new_list.html', title=title)


    session['lists'].append({
        'id': str(uuid4()), 
        'title': title, 
        'todos': []
        })
    
    flash('The list has been created.', 'success')
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>')
@require_list
def show_list(lst, list_id):
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst)

@app.route('/lists/<list_id>/todos', methods=['POST'])
@require_list
def create_todo(lst, list_id):
    todo = request.form['todo'].strip()

    error = error_for_todo_title(todo)
    if error:
        flash(error, 'error')
        return render_template('list.html', lst=lst)

    lst['todos'].append({
        'completed': False,
        'title': todo,
        'id': str(uuid4()),
    })

    flash('The todo has been created', 'success')
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=['POST'])
@require_todo
def toggle_todo(lst, todo, list_id, todo_id):
    value = request.form['completed']

    if value == 'True':
        todo['completed'] = True
        flash('You marked the todo.', 'success')
    else:
        todo['completed'] = False
        flash('You unmarked the todo.', 'success')

    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=['POST'])
@require_todo
def delete_todo(lst, todo, list_id, todo_id):
    lst['todos'].remove(todo)

    flash('You have deleted the todo.', 'success')
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/complete_all', methods=['POST'])
@require_list
def complete_all(lst, list_id):
    for todo in lst['todos']:
        todo['completed'] = True

    flash('Everything has been marked as done.', 'success')
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/edit')
@require_list
def show_edit_list(lst, list_id):
    return render_template('edit_list.html', lst=lst)

@app.route('/lists/<list_id>/delete', methods=['POST'])
@require_list
def delete_list(lst, list_id):
    session['lists'].remove(lst)

    flash('List was removed', 'success')
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>', methods=['POST'])
@require_list
def edit_list_name(lst, list_id):
    new_name = request.form['list_title']

    error = error_for_list_title(new_name, session['lists'])
    if error:
        flash(error, 'error')
        return render_template('edit_list.html', lst=lst, title=new_name)
    
    lst['title'] = new_name

    flash('List was renamed', 'success')
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)