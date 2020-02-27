from flask import Flask,render_template,request
from parameters.bumble import add_mod

app= Flask(__name__)

app.config['SECRET_KEY'] = "1234"

app.register_blueprint(add_mod, url_prefix='/bumble')

@app.route('/')
def run():
    return render_template('home.html')

@app.route('/bumble', methods = ['POST'])
def bumble():
    output = request.form["login"]
    if output == "fb":
        return render_template('fb.html')
    else:
        return render_template('bumble.html')

if __name__ == '__main__':
    app.run()
