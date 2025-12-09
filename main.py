from flask import Flask, redirect, render_template, request, url_for  # type: ignore

import db

app = Flask(__name__)

# Connexion à la base de données
conn = db.connect()


# Page d'accueil
@app.route("/accueil")
def accueil():
    return render_template("accueil.html")


if __name__ == "__main__":
    app.run(debug=True)
