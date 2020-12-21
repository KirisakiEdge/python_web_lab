from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/contacts")
def links():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
