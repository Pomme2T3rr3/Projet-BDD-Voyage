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
    if ID <= 0:
        return "Erreur, cette page n'existe pas. ", 404

    if "client" not in session and ("emp" not in session):
        return redirect(url_for("connexion"))

    conn = db.connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT idVoy, descriptif, dateDebut, dateFin, PrixPersonne
        FROM voyage
        WHERE idVoy = %s
        ORDER BY dateDebut
    """,
        (ID,),
    )
    v = cur.fetchone()

    if v is None:
        return "Voyage introuvable", 404

    # Étapes
    cur.execute(
        """
        SELECT
            e.idEt,
            e.TyP,
            e.transport,
            vd.nom AS ville_depart,
            va.nom AS ville_arrivee,
            e.dateDepart,
            e.dateArrivee
        FROM etape e
        JOIN constitue c ON e.idEt = c.idEt
        JOIN ville vd ON e.depart = vd.idVille
        JOIN ville va ON e.arrivee = va.idVille
        WHERE c.idVoy = %s
        ORDER BY e.dateDepart
    """,
        (ID,),
    )
    etapes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "voyage.html",
        voyage={
            "idVoy": v[0],
            "descriptif": v[1],
            "dateDebut": v[2],
            "dateFin": v[3],
            "prix": v[4],
            "etapes": etapes,
        },
    )


@app.route("/voyage/<int:ID>/etape/ajouter", methods=["GET", "POST"])
def ajouter_etape(ID):
    if "emp" not in session:
        return redirect(url_for("/connexion.html"))

    conn = db.connect()
    cur = conn.cursor()

    # on check l'existence du voyage
    cur.execute("SELECT idVoy FROM voyage WHERE idVoy = %s", (ID,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return "Voyage inexistant", 404

    # on récupère les villes
    cur.execute("SELECT idVille, nom FROM ville ORDER BY nom")
    villes = cur.fetchall()

    if request.method == "POST":
        typ = request.form.get("typ")
        transport = request.form.get("transport")
        depart = request.form.get("depart")
        arrivee = request.form.get("arrivee")
        dateDepart = request.form.get("dateDepart")
        dateArrivee = request.form.get("dateArrivee")

        # on insère l'étape
        cur.execute(
            """
            INSERT INTO etape (TyP, transport, depart, arrivee, dateDepart, dateArrivee)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING idEt
            """,
            (typ, transport, depart, arrivee, dateDepart, dateArrivee),
        )

        e = cur.fetchone()
        if e is None:
            conn.rollback()
            cur.close()
            conn.close()
            return "Erreur à la création de l'étape", 500

        idEt = e[0]

        # on fait la liaison avec le voyage
        cur.execute("INSERT INTO constitue (idVoy, idEt) VALUES (%s, %s)", (ID, idEt))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(f"/voyage_{ID}")

    cur.close()
    conn.close()

    return render_template("ajouter_etape.html", idVoy=ID, villes=villes)


####################################################################################################
#####################   Fonctions pour Espace Client   #############################################


# fonctionnel
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
            """,
            (nom, prenom, email, idCli),
        )
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
    """,
        (idCli,),
    )
    reservations = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "Mon_compte.html",
        client=client,
        reservations=reservations,
    )


@app.route("/offres_client")
def offres_client():
    if "client" not in session:
        redirect("/connexion")

    cli = session["client"]
    conn = db.connect()
    cur = conn.cursor()
    # Récupérer les voyages
    cur.execute(
        """
        SELECT v.idVoy, v.PrixPersonne, v.dateDebut, v.dateFin, v.descriptif, a.nom
        FROM voyage v
        JOIN employe e ON v.planifie_par = e.idEmp
        JOIN agence a ON e.idA = a.idA
        WHERE v.dateDebut >= CURRENT_DATE
        ORDER BY v.dateDebut
        """
    )
    voyages = cur.fetchall()
    print(voyages)

    cur.close()
    conn.close()

    return render_template("offres_client.html", cli=cli, voyages=voyages)


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
    if "emp" not in session and "client" not in session:
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
