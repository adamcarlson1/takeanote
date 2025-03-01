from flask import Flask, render_template

# Create Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Serve index.html
@app.route('/')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
