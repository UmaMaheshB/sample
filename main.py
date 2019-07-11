# Another example chaining Bokeh's to Flask.

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html.j2")



if __name__ == "__main__":
    app.run(debug=True, port=5957)