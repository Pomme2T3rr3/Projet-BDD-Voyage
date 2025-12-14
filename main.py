from flask import (  # type: ignore
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import db

app = Flask(__name__)
app.secret_key = "secret_key_bon_voyage"

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
    login = request.form.get("num_login")
    mdp = request.form.get("mdp")

    if not login or not mdp:
        return render_template("connexion_profil.html")

    conn = db.connect()
    cur = conn.cursor()

    # employé
    cur.execute(
        """
        SELECT idEMP, nom, prenom, idA
        FROM employe
        WHERE siteLogin = %s AND mdp = %s
        """,
        (login, mdp),
    )

    emp = cur.fetchone()

    if emp:
        session["emp"] = emp
        cur.close()
        conn.close()
        return redirect(url_for("espace_pro", login=emp[0]))

    # client
    cur.execute(
        """
        SELECT idCli
        FROM client
        WHERE Clogin = %s AND Cmdp = %s
        """,
        (login, mdp),
    )

    cli = cur.fetchone()

    if cli:
        session["client"] = cli
        cur.close()
        conn.close()
        return redirect(url_for("espace_client", login=cli[0]))

    cur.close()
    conn.close()

    return render_template("connexion_profil.html")

# Affiche les détails et les étapes du voyage Pas fini et CKC 
@app.route("/voyage_<int:ID>")
def voyage(ID):
    if ID == 0:
        return "Erreur, cette page n'existe pas. ", 404
    
    """if "client" not in session and ("emp" not in session):
        return redirect(url_for("connexion"))"""
    
    conn = db.connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT idVoy, descriptif, dateDebut, dateFin, PrixPersonne
        FROM voyage
        WHERE idVoy = %s
        ORDER BY dateDebut
    """,(ID,))
    rows = cur.fetchall()

    voyages = []

    for v in rows:
        idVoy = v[0]

        # Étapes
        cur.execute("""
            SELECT idEt 
            FROM constitue
            WHERE idVoy = %s
            ORDER BY idEt
        """, (idVoy,))
        etapes = [e[0] for e in cur.fetchall()]

        # Visas (CKC)
        """"
        cur.execute(""
            SELECT v.nomVisa
            FROM visa v
            JOIN voyage_visa vv ON v.idVisa = vv.idVisa
            WHERE vv.idVoy = %s
        "", (idVoy,))
        visas = [vi[0] for vi in cur.fetchall()]"""

        voyages.append({
            "idVoy": idVoy,
            "descriptif": v[1],
            "dateDebut": v[2],
            "dateFin": v[3],
            "prix": v[4],
            "etapes": etapes
            #"visas": visas
        })

    cur.close()
    conn.close()

    return render_template("voyage.html", voyages=voyages)



####################################################################################################
#####################   Fonctions pour Espace Client   #############################################



# Fait à l'arrache mais fonctionnel
@app.route("/profil_client<string:login>")
def espace_client(login):
    if "client" not in session:
        return redirect("/connexion")
    
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM client WHERE idCli = %s;", (login,))
        tmp = cur.fetchone()
        cur.close()
    return render_template("espace_client.html", cli=tmp)

@app.route("/Mon_compte", methods=["GET", "POST"])
def compte_client():
    if "client" not in session:
        return redirect("/connexion")


    idCli = session["client"][0]
    conn = db.connect()
    cur = conn.cursor()


    # Mise à jour des infos personnelles
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        email = request.form.get("courriel")


        cur.execute(
            """
            UPDATE client
            SET nom = %s, prenom = %s, courriel = %s
            WHERE idCli = %s
            """,(nom, prenom, email, idCli),)
        conn.commit()


    # Infos client
    cur.execute("SELECT nom, prenom, courriel FROM client WHERE idCli = %s", (idCli,))
    client = cur.fetchone()


    # Réservations
    cur.execute(
    """
    SELECT f.idVoy,v.descriptif, v.PrixPersonne, v.dateDebut, v.dateFin
    FROM fait f
    JOIN voyage v ON f.idVoy = v.idVoy
    WHERE f.idCli = %s
    ORDER BY v.dateDebut DESC
    """,(idCli,),)
    reservations = cur.fetchall()


    cur.close()
    conn.close()


    return render_template("Mon_compte.html", client=client,reservations=reservations,)


#####################   Fin : Fonctions pour Espace Client   ########################################
#####################################################################################################

# Fait à l'arrache mais fonctionnel
@app.route("/profil_pro<string:login>")
def espace_pro(login):
    if "emp" not in session:
        return redirect("/connexion")

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM employe WHERE sitelogin = %s;", (login,))
        tmp = cur.fetchone()
        cur.close()
    return render_template("espace_pro.html", emp=tmp)


@app.route("/offres")
def liste_voyages():
    if "emp" not in session:
        return redirect("/connexion")

    emp = session["emp"]
    id_emp = emp[0]

    conn = db.connect()
    cur = conn.cursor()

    # Récupérer l'agence de l'employé
    cur.execute(
        """
        SELECT idA
        FROM employe
        WHERE idEmp = %s
    """,
        (id_emp,),
    )

    row = cur.fetchone()

    if row is None:
        return "Erreur, employé sans agence", 400
    idA = row[0]

    # Récupérer les voyages
    cur.execute(
        """
        SELECT v.idVoy, v.PrixPersonne, v.dateDebut, v.dateFin, v.descriptif
        FROM voyage v
        JOIN employe e ON v.planifie_par = e.idEmp
        WHERE e.idA = %s
        ORDER BY v.dateDebut
        """,
        (idA,),
    )
    voyages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("liste_voyages.html", emp=emp, voyages=voyages)


@app.route("/voyage/ajouter", methods=["Get", "POST"])
def ajouter_voyage():
    if "emp" not in session:
        return redirect("/connexion")

    emp = session["emp"]
    id_emp = emp[0]

    if request.method == "POST":
        dateDebut = request.form.get("dateDebut")
        dateFin = request.form.get("dateFin")
        prix = request.form.get("PrixPersonne")
        descriptif = request.form.get("descriptif")

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO voyage (dateDebut, dateFin, PrixPersonne, descriptif, planifie_par)
            VALUES(%s, %s, %s, %s, %s)
            """,
            (dateDebut, dateFin, prix, descriptif, id_emp),
        )

        conn.commit()
        conn.close()
        cur.close()
        return redirect("/offres")

    return render_template("ajout_edit_voyage.html", action="Ajouter")


if __name__ == "__main__":
    app.run(debug=True)
