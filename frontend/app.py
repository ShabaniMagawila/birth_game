from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")


@app.route('/')
def index():
    """Main page with user form"""
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_user():
    """Submit user data to FastAPI backend"""
    try:
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        
        # Validate input
        if not all([first_name, last_name, date_of_birth]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        # Send data to FastAPI backend
        response = requests.post(
            f"{API_URL}/users/",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth
            }
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return render_template('result.html', user=user_data)
        else:
            flash(f'Error: {response.text}', 'error')
            return redirect(url_for('index'))
            
    except requests.exceptions.ConnectionError:
        flash('Cannot connect to backend API. Make sure it is running!', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/users')
def list_users():
    """Display all users"""
    try:
        response = requests.get(f"{API_URL}/users/")
        
        if response.status_code == 200:
            users = response.json()
            return render_template('users.html', users=users)
        else:
            flash('Error fetching users', 'error')
            return redirect(url_for('index'))
            
    except requests.exceptions.ConnectionError:
        flash('Cannot connect to backend API. Make sure it is running!', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    debug_flag = os.getenv("DEBUG", "False").strip().lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=5000, debug=debug_flag)
