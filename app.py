from flask import Flask, render_template, redirect, url_for, request, jsonify
import json
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Store current status and description
current_status = None
current_description = ""

def load_statuses():
    try:
        with open('statuses.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_statuses(statuses):
    with open('statuses.json', 'w') as f:
        json.dump(statuses, f)

def load_description():
    # Implement this based on your storage method
    pass

def save_description(description):
    # Implement this based on your storage method
    pass

@app.route('/')
def index():
    global current_status, current_description
    statuses = load_statuses()
    return render_template('index.html', 
                         statuses=statuses,
                         current_status=current_status,
                         current_description=current_description)

@app.route('/manage')
def manage_statuses():
    statuses = load_statuses()
    return render_template('manage_statuses.html', extra_statuses=statuses)

@app.route('/add_status', methods=['POST'])
def add_status():
    statuses = load_statuses()
    new_status = {
        'name': request.form['name'],
        'color': request.form['color']
    }
    statuses.append(new_status)
    save_statuses(statuses)
    return redirect(url_for('manage_statuses'))

@app.route('/update_status/<int:status_id>', methods=['POST'])
def update_status(status_id):
    statuses = load_statuses()
    if 0 <= status_id - 1 < len(statuses):
        statuses[status_id - 1]['name'] = request.form['name']
        statuses[status_id - 1]['color'] = request.form['color']
        save_statuses(statuses)
    return redirect(url_for('manage_statuses'))

@app.route('/move_status/<int:status_id>/<direction>', methods=['POST'])
def move_status(status_id, direction):
    statuses = load_statuses()
    idx = status_id - 1
    if direction == 'up' and idx > 0:
        statuses[idx], statuses[idx-1] = statuses[idx-1], statuses[idx]
    elif direction == 'down' and idx < len(statuses) - 1:
        statuses[idx], statuses[idx+1] = statuses[idx+1], statuses[idx]
    save_statuses(statuses)
    return redirect(url_for('manage_statuses'))

@app.route('/delete_status/<int:status_id>', methods=['POST'])
def delete_status(status_id):
    statuses = load_statuses()
    if 0 <= status_id - 1 < len(statuses):
        statuses.pop(status_id - 1)
        save_statuses(statuses)
    return redirect(url_for('manage_statuses'))

@app.route('/set_status/<int:status_id>', methods=['GET'])
def set_status(status_id):
    global current_status
    statuses = load_statuses()
    if 0 <= status_id - 1 < len(statuses):
        current_status = statuses[status_id - 1]
        socketio.emit('status_update', {
            'status': current_status,
            'description': current_description
        })
    return redirect(url_for('index'))

@app.route('/update_description', methods=['POST'])
def update_description():
    global current_description
    current_description = request.form.get('description', '')
    if current_status:  # Only emit if we have a status
        socketio.emit('status_update', {
            'status': current_status,
            'description': current_description
        })
    return redirect(url_for('index'))

# API endpoint for display to get current status
@app.route('/api/current_status', methods=['GET'])
def get_current_status():
    return jsonify({
        'status': current_status,
        'description': current_description
    })

@app.route('/clear_status')
def clear_status():
    global current_status, current_description
    current_status = None
    current_description = ""
    
    # Emit the cleared status to the display
    socketio.emit('status_update', {
        'status': None,
        'description': ""
    })
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)


