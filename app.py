# Main Flask App for To-Do-Gether
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Todo
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== Authentication Routes ====================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()
        
        # Validation
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already taken'}), 400
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Account created! Please login.'}), 201
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Validation
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Login user
        login_user(user, remember=True)
        return jsonify({'success': True, 'message': 'Logged in successfully!'}), 200
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('login'))


# ==================== Dashboard Routes ====================

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - shows all users and their todos"""
    users = User.query.all()
    return render_template('dashboard.html', users=users)


@app.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    """API endpoint to get all todos grouped by user"""
    users = User.query.all()
    
    dashboard_data = {}
    for user in users:
        todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.order).all()
        dashboard_data[user.username] = {
            'user_id': user.id,
            'todos': [todo.to_dict() for todo in todos],
            'count': len(todos),
            'completed_count': sum(1 for todo in todos if todo.completed)
        }
    
    return jsonify({
        'success': True,
        'data': dashboard_data,
        'current_user': current_user.username
    })


# ==================== Todo Routes ====================

@app.route('/api/todo', methods=['POST'])
@login_required
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    task = data.get('task', '').strip()
    user_id = data.get('user_id')
    
    # Validation
    if not task:
        return jsonify({'success': False, 'message': 'Task cannot be empty'}), 400
    
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID required'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    # Get max order for this user
    max_order = db.session.query(db.func.max(Todo.order)).filter_by(user_id=user_id).scalar() or 0
    
    # Create todo
    todo = Todo(
        task=task,
        user_id=user_id,
        created_by=current_user.username,
        order=max_order + 1
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({'success': True, 'data': todo.to_dict()}), 201


@app.route('/api/todo/<int:todo_id>', methods=['PUT'])
@login_required
def update_todo(todo_id):
    """Update a todo"""
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({'success': False, 'message': 'Todo not found'}), 404
    
    data = request.get_json()
    
    # Update task if provided
    if 'task' in data:
        task = data.get('task', '').strip()
        if task:
            todo.task = task
    
    # Update completed status if provided
    if 'completed' in data:
        todo.completed = data.get('completed', False)
    
    todo.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True, 'data': todo.to_dict()})


@app.route('/api/todo/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    """Delete a todo"""
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({'success': False, 'message': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Todo deleted'})


@app.route('/api/todo/<int:todo_id>/reorder', methods=['PATCH'])
@login_required
def reorder_todo(todo_id):
    """Reorder todos"""
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({'success': False, 'message': 'Todo not found'}), 404
    
    data = request.get_json()
    new_order = data.get('order')
    
    if new_order is None:
        return jsonify({'success': False, 'message': 'Order value required'}), 400
    
    todo.order = new_order
    db.session.commit()
    
    return jsonify({'success': True, 'data': todo.to_dict()})


# ==================== Utility Routes ====================

@app.route('/api/time')
def get_time():
    """API endpoint to get current date/time"""
    now = datetime.now()
    return jsonify({
        'date': now.strftime('%B %d, %Y'),
        'day': now.strftime('%A'),
        'time': now.strftime('%I:%M %p'),
        'timestamp': now.isoformat()
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Server error'}), 500


# ==================== Database Initialization ====================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")


# ==================== Main ====================

if __name__ == '__main__':
    # Initialize database on first run
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
