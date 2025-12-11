from flask import Flask, redirect, render_template, request, url_for  # type: ignore

import db

app = Flask(__name__)

# Connexion à la base de données
conn = db.connect()


# Page d'accueil
@app.route("/accueil")
def accueil():
    return render_template("accueil.html")

# Page de connexion
@app.route("/profil")
def connexion():
    return render_template("connexion_profil.html") 

# Pas fonctionnel pour l'instant
@app.route("/verification", methods=["GET", "POST"])
def verification():
    lst_client = []
    lst_employe = []
    
    login = request.form.get["num_login"]
    mdp = request.form.get["mdp"]

    if not login or not mdp:
        return redirect(url_for("connexion_profile.html"))

    with conn.cursor() as cur:
        cur.execute("SELECT Clogin, Cmdp FROM client;")
        for i in cur.fetchall():
            lst_client.append([i[0],i[1]])
        cur.close()
    
    with conn.cursor() as cur:
        cur.execute("SELECT sitelogin, mdp FROM employe;")
        for i in cur.fetchall():
            lst_employe.append([i[0],i[1]])
        cur.close()

    if [login, mdp] in lst_client:
        return render_template("espace_client.html")
    
    elif [login, mdp] in lst_employe:
        return render_template("espace_pro.html")
    else : 
        return redirect(url_for("connexion_profile.html"))


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
