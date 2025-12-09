from flask import Flask, redirect, render_template, request, url_for  # type: ignore

import db

app = Flask(__name__)

# Connexion à la base de données
conn = db.connect()


# Page d'accueil
@app.route("/accueil")
def accueil():
    return render_template("accueil.html")


# pas fonctionnel
@app.route("/client", methods=["GET", "POST"])
def manage_client():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO client (nom, prenom, sex, age, nat, adr, numtel, courriel)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nom, prenom),
            )

        return redirect(url_for("manage_client"))

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM client")
        client = cur.fetchall()

    return render_template("client.html", client=client)


if __name__ == "__main__":
    app.run(debug=True)
