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
@app.route("/connexion")
def connexion():
    return render_template("connexion_profil.html") 

# Verifie le login et le mot de passe  
@app.route("/verification", methods=["GET", "POST"])
def verification():
    lst_client = []
    lst_employe = []
    
    login = request.form.get("num_login")
    mdp = request.form.get("mdp")

    if not login or not mdp:
        return render_template("connexion_profile.html")

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
        return redirect(url_for('profil_client', login=login))
    
    elif [login, mdp] in lst_employe:
        return redirect(url_for('espace_pro', login=login))
    else : 
        return render_template("connexion_profile.html")

# Fait à l'arrache mais fonctionnel  
@app.route("/profil_client<string:login>")
def espace_client(login):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM client WHERE Clogin = %s;',(login,))
        tmp = cur.fetchone()
        cur.close()
    return render_template("espace_client.html", cli = tmp)

# Fait à l'arrache mais fonctionnel
@app.route("/profil_pro<string:login>")
def espace_pro(login):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM employe WHERE sitelogin = %s;',(login,))
        tmp = cur.fetchone()
        cur.close()
    return render_template("espace_pro.html", emp = tmp)

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
