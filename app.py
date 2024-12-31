from flask import Flask, render_template
import vlc  # VLC Python bindings

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # The HTML page for the frontend

if __name__ == "__main__":
    app.run(debug=True)
