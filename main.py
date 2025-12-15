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
app.secret_key = "9f3a8c6e1d4b2a8f7c9d0e4f1a6b2c8d9e3f7a1c4b6d8e0f2a5c9b7d1e"

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

# Vraiment pas sur que ça marche
@app.route("/deconnexion")
def deconnexion():
    if "emp" in session:
        session.pop("emp", None)
        return redirect(url_for("accueil"))
    session.pop("client", None)
    return redirect(url_for("accueil"))    


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

# Effectue l'inscription du client
@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        # récupération des données du formulaire
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        courriel = request.form.get("courriel")
        nat = request.form.get("nationalite")
        adr = request.form.get("adresse")
        numtel = request.form.get("telephone")
        age = request.form.get("age")
        sexe = request.form.get("sexe")
        login = request.form.get("login")
        mdp = request.form.get("mdp")

        # validation minimale
        if not nom or not prenom or not courriel or not nat or not adr or not numtel or not age or not sexe or not login or not mdp :
            return "Champs manquants" , 404

        # insertion en base
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO client (nom, prenom, courriel, nat, adr, numtel, age, sexe, Clogin, Cmdp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """, (nom, prenom, courriel, nat, adr, numtel, age, sexe, login, mdp))
        conn.commit()

        return redirect(url_for("connexion"))

    # GET → affichage du formulaire
    return "RTFM brotha !!!" , 404


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
        courriel = request.form.get("courriel")
        nat = request.form.get("nationalite")
        adr = request.form.get("adresse")
        numtel = request.form.get("telephone")
        age = request.form.get("age")
        sexe = request.form.get("sexe")
        login = request.form.get("login")
        mdp = request.form.get("mdp")
        
        cur.execute(
            """
            UPDATE client
            SET nom = %s, prenom = %s, courriel = %s, nat = %s, adr = %s, numtel = %s, age = %s, sexe = %s, Clogin = %s, Cmdp = %s
            WHERE idCli = %s
            """,
            (nom, prenom, courriel, nat, adr, numtel, age, sexe, login, mdp, session["client"][0]),
        )
        conn.commit()

    # Infos client
    cur.execute("SELECT nom, prenom, courriel, nat, adr, numtel, age, sexe, Clogin, Cmdp FROM client WHERE idCli = %s", (idCli,))
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

####################################################################################################
#####################   Fonctions pour Espace Pro   #############################################


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

@app.route("/voyage/<int:idVoy>/delete")
def supprimer_voyage(idVoy):
    # Vérification : uniquement un employé connecté
    if "emp" not in session:
        return redirect("/connexion")

    emp = session["emp"]
    id_emp = emp[0]

    conn = db.connect()
    cur = conn.cursor()

    # Vérifier que le voyage appartient bien à l'agence de l'employé
    cur.execute(
        """
        SELECT v.idVoy
        FROM voyage v
        JOIN employe e ON v.planifie_par = e.idEmp
        WHERE v.idVoy = %s AND e.idEmp = %s
        """,
        (idVoy, id_emp),
    )

    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return "Suppression non autorisée", 403

    # ⚠️ Supprimer les dépendances d'abord (FK)
    cur.execute(
        """
        DELETE FROM constitue
        WHERE idVoy = %s
        """,
        (idVoy,),
    )

    # Supprimer le voyage
    cur.execute(
        """
        DELETE FROM voyage
        WHERE idVoy = %s
        """,
        (idVoy,),
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/offres")

#####################   Fin : Fonctions pour Espace Pro   ########################################
#####################################################################################################

if __name__ == "__main__":
    app.run(debug=True)
