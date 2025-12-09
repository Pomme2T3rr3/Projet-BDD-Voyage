DROP TABLE IF EXISTS agence CASCADE;
DROP TABLE IF EXISTS employe CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS voyage CASCADE;
DROP TABLE IF EXISTS etape CASCADE;
DROP TABLE IF EXISTS ville CASCADE;
DROP TABLE IF EXISTS pays CASCADE;
DROP TABLE IF EXISTS visa CASCADE;

DROP TABLE IF EXISTS fait CASCADE;
DROP TABLE IF EXISTS constitue CASCADE;
DROP TABLE IF EXISTS obtient CASCADE;
DROP TABLE IF EXISTS parle CASCADE;



CREATE TABLE agence(
    idA serial primary key,
    nom varchar(25),
    adresse text,
    idEmp int references employe(idEmp) UNIQUE,
    CONSTRAINT est_employe_agence CHECK ( idResp IS NULL OR idResp IN (
                                        SELECT idEmp FROM employe WHERE employe.idA = agence.idA ))
);

CREATE TABLE pays(
    codeP char(3) primary key,
    nom varchar(25),
    descriptif text
);

CREATE TABLE ville(
    idVille serial primary key,
    nom varchar(20),
    pays char(3) references pays(codeP)
);

CREATE TABLE visa(
    idVisa serial primary key,
    typev varchar(10),
    prixVisa int
);

CREATE TABLE client(
    idCli serial primary key,
    nom varchar(25) NOT NULL,
    prenom varchar(25) NOT NULL,
    sexe char(1) NOT NULL,
    age int NOT NULL,
    nat char(3) NOT NULL,
    adr varchar(50) NOT NULL,
    numtel varchar(13) NOT NULL,
    courriel varchar(25) NOT NULL,
    Clogin varchar(50) NOT NULL,
    Cmdp varchar(25) NOT NULL,
    CONSTRAINT check_courriel CHECK (courriel LIKE '%@%.%'),
    CONSTRAINT check_age CHECK (age >= 18)
);

CREATE TABLE employe(
    idEmp serial primary key,
    nom varchar(25) NOT NULL,
    prenom varchar(25) NOT NULL,
    siteLogin varchar(25),
    mdp varchar(50),
    idA int references agence(idA),
    CONSTRAINT check_longueur_mdp CHECK (LENGHT(mdp) >= 8),

);

CREATE TABLE etape(
    idEt serial primary key,
    TyP varchar(20),
    transport varchar(15),
    depart int references ville(idVille) NOT NULL,
    arrivee int references ville(idVille) NOT NULL,
    dateDepart date NOT NULL,
    dateArrivee date NOT NULL,
    CONSTRAINT check_dates_etape CHECK (dateArrivee >= dateDepart)
);

CREATE TABLE voyage(
    idVoy serial primary key,
    dateDebut date NOT NULL,
    dateFin date NOT NULL,
    PrixPersonne numeric(6,2),
    descriptif text,
    planifie_par int references employe(idEmp),
    CONSTRAINT check_dates_voyage CHECK (dateFin > dateDebut)
);
/*
 --- Creation de tables des associations ---
*/
CREATE TABLE fait(
    idCli int references client(idCli),
    idVoy int references voyage(idVoy),
    primary key(idCli, idVoy)
);

CREATE TABLE constitue(
    idVoy int references voyage(idVoy),
    idEt int references etape(idEt),
    primary key(idVoy, idEt)
);

CREATE TABLE obtient(
    idCli int references client(idCli),
    codeP char(3) references pays(codeP),
    idVisa int references visa(idVisa),
    dateObt date NOT NULL,
    dateExp date NOT NULL,
    primary key(idCli, codeP , idVisa),
    CONSTRAINT check_dates_obtient CHECK (dateExp > dateObt)
);

CREATE TABLE parle(
    codeP char(3) references pays(codeP),
    langue varchar(15),
    primary key(codeP, langue)
);


-- TABLE agence
INSERT INTO agence (nom, adresse, idEmp) VALUES
('GlobeTrotter', '12 rue de la Paix, Paris', 1),
('Voyage2000', '7 avenue de la Liberté, Lyon',3),
('Evasion360', '25 boulevard du Port, Marseille',5);

-- TABLE pays
INSERT INTO pays (codeP, nom, descriptif) VALUES
('FRA', 'France', 'Pays de la gastronomie'),
('ESP', 'Espagne', 'Beaucoup de soleil et beau temps'),
('ITA', 'Italie', 'Pays de la pizza et des pâtes'),
('USA', 'États-Unis', 'Pays du cinéma'),
('JPN', 'Japon', 'Pays des nouvelles technologies'),
('MAR', 'Maroc', 'Architectures originales et deserts à perte de vue');

-- TABLE ville
INSERT INTO ville (nom, pays) VALUES
('Paris', 'FRA'),
('Lyon', 'FRA'),
('Madrid', 'ESP'),
('Barcelone', 'ESP'),
('Rome', 'ITA'),
('Venise', 'ITA'),
('New York', 'USA'),
('Los Angeles', 'USA'),
('Tokyo', 'JPN'),
('Kyoto', 'JPN'),
('Marrakech', 'MAR'),
('Casablanca', 'MAR');

-- TABLE visa
INSERT INTO visa (typev, prixVisa) VALUES
('Tourisme', 80),
('Affaires', 120),
('Études', 150),
('Transit', 40);

-- TABLE client
INSERT INTO client (nom, prenom, sexe, age, nat, adr, numtel, Clogin, Cmdp, courriel) VALUES
('Durand', 'Alice', 'F', 28, 'FRA', '5 rue Victor Hugo, Paris', '+33645121212', 'adurand', 'Alice2024!', 'alice.durand@mail.fr'),
('Martin', 'Lucas', 'M', 35, 'FRA', '12 avenue Foch, Lyon', '+33688223344', 'lmartin', 'Lucas#2024', 'lucas.martin@mail.fr'),
('Garcia', 'Sofia', 'F', 42, 'ESP', '8 calle Mayor, Madrid', '+34915554444', 'sgarcia', 'Sofia@Madrid', 'sofia.garcia@mail.es'),
('Rossi', 'Marco', 'M', 31, 'ITA', 'Via Roma 10, Rome', '+39066555123', 'mrossi', 'Marco!Roma31', 'marco.rossi@mail.it'),
('Smith', 'John', 'M', 45, 'USA', '123 5th Ave, New York', '+12125551234', 'jsmith', 'John$NY2024', 'john.smith@mail.com'),
('Tanaka', 'Yuki', 'F', 26, 'JPN', '2-3-5 Shibuya, Tokyo', '+81345551212', 'ytanaka', 'Yuki@Tokyo26', 'yuki.tanaka@mail.jp'),
('Bennani', 'Sara', 'F', 33, 'MAR', '45 rue Mohamed V, Marrakech', '+212655123123', 'sbennani', 'Sara#Maroc33', 'sara.bennani@mail.ma'),
('Nguyen', 'Linh', 'F', 29, 'FRA', '3 rue de Provence, Lyon', '+33655887799', 'lnguyen', 'Linh!Lyon29', 'linh.nguyen@mail.fr'),
('Dupont', 'Julien', 'M', 38, 'FRA', '1 rue de la Gare, Paris', '+33677554411', 'jdupont', 'Julien@2024', 'julien.dupont@mail.fr'),
('Lopez', 'Carlos', 'M', 41, 'ESP', 'Calle del Sol 25, Barcelone', '+34911223355', 'clopez', 'Carlos#BCN41', 'carlos.lopez@mail.es');

-- TABLE employe
INSERT INTO employe (nom, prenom, siteLogin, mdp, idA) VALUES
('Deneuville', 'Damian', 'ddamian', 'azerty12', 1),
('Moreau', 'Jean', 'jmoreau', 'voyage1', 1),
('Lefevre', 'Paul', 'plefevre', 'passe123', 2),
('Dubois', 'Emma', 'edubois', 'soleil99', 2),
('Petit', 'Nina', 'npetit', 'monde01', 3);

-- TABLE voyage
INSERT INTO voyage (dateDebut, dateFin, PrixPersonne, descriptif, planifie_par) VALUES
('2025-02-10', '2025-02-20', 1500.00, 'Circuit culturel en Italie', 1),
('2025-03-01', '2025-03-10', 2300.00, 'Découverte du Japon', 5),
('2025-04-15', '2025-04-25', 1800.00, 'Voyage gastronomique en Espagne', 3),
('2025-05-05', '2025-05-15', 2100.00, 'Road trip aux États-Unis', 4),
('2025-06-10', '2025-06-17', 1200.00, 'Séjour au Maroc', 5),
('2025-06-10', '2026-06-17', 1300.00, 'Séjour en France', 2),
('2026-06-10', '2027-06-17', 1800.00, 'Séjour en Papouasie', 1),
('2026-07-23', '2026-08-03', 900.00, 'Séjour au Groënland', 4),
('2026-07-23', '2026-08-03', 900.00, 'Séjour en italie', 5),
('2025-09-23', '2026-10-03', 4900.00, 'Séjour en Allemagne', 5),
('2025-06-10', '2026-09-17', 1300.00, 'Séjour en France', 5),
('2025-11-01', '2025-11-10', 2000.00, 'Mini-séjour test pour revenus agence 3', 5);

-- TABLE etape
INSERT INTO etape (TyP, transport, depart, arrivee, dateDepart, dateArrivee) VALUES
('Découverte', 'Avion', 1, 5, '2025-02-10', '2025-02-11'),
('Visite', 'Train', 5, 6, '2025-02-12', '2025-02-14'),
('Culture', 'Avion', 7, 9, '2025-03-01', '2025-03-02'),
('Tradition', 'Train', 9, 10, '2025-03-03', '2025-03-05'),
('Gastronomie', 'Bus', 3, 4, '2025-04-15', '2025-04-20'),
('Aventure', 'Voiture', 7, 8, '2025-05-05', '2025-05-10'),
('Détente', 'Avion', 11, 12, '2025-06-10', '2025-06-11');

-- TABLE constitue
INSERT INTO constitue (idVoy, idEt) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5),
(4, 6),
(5, 7);

-- TABLE fait
INSERT INTO fait (idCli, idVoy) VALUES
(1, 1),
(2, 1),
(3, 3),
(4, 1),
(5, 4),
(6, 2),
(7, 5),
(8, 3),
(9, 4),
(10, 5),
(1, 6),
(2, 7),
(3, 7),
(1, 8),
(2, 8),
(3, 8),
(1, 12),
(2, 12),
(1, 11),
(2, 10);

-- TABLE obtient
-- Quels clients ont obtenu quels visas
INSERT INTO obtient (idCli, codeP, idVisa, dateObt, dateExp) VALUES
(1, 'ITA', 1, '2025-01-15', '2025-07-15'),
(2, 'USA', 2, '2025-02-01', '2026-02-01'),
(3, 'ESP', 1, '2024-12-10', '2025-06-10'),
(4, 'ITA', 1, '2025-01-20', '2025-07-20'),
(5, 'JPN', 2, '2025-03-01', '2026-03-01'),
(6, 'JPN', 3, '2025-01-10', '2026-01-10'),
(7, 'MAR', 1, '2025-02-05', '2025-08-05'),
(8, 'ESP', 1, '2025-01-12', '2025-07-12'),
(9, 'USA', 2, '2025-02-25', '2026-02-25'),
(10, 'ITA', 1, '2025-01-18', '2025-07-18');


-- TABLE parle
INSERT INTO parle (codeP, langue) VALUES
('FRA', 'Français'),
('ESP', 'Espagnol'),
('ITA', 'Italien'),
('USA', 'Anglais'),
('JPN', 'Japonais'),
('MAR', 'Arabe'),
('MAR', 'Français'), -- deux langues
('USA', 'Espagnol'); -- même chose



-- ==VUES==
CREATE OR REPLACE VIEW activite_agence AS
SELECT
    a.idA,
    a.nom AS agence,

    -- Nombre de voyages en cours
    COUNT(DISTINCT CASE
        WHEN CURRENT_DATE BETWEEN v.dateDebut AND v.dateFin THEN v.idVoy
    END) AS nb_voyages_en_cours,

    -- Nombre de voyages ouverts à la réservation
    COUNT(DISTINCT CASE
        WHEN v.dateDebut > CURRENT_DATE THEN v.idVoy
    END) AS nb_voyages_ouverts_resa,

    -- Nombre de clients actuellement en voyage
    COUNT(DISTINCT CASE
        WHEN CURRENT_DATE BETWEEN v.dateDebut AND v.dateFin THEN f.idCli
    END) AS nb_clients_en_voyage,

    -- Nombre de réservations en cours
    COUNT(DISTINCT CASE
        WHEN v.dateDebut > CURRENT_DATE THEN f.idCli
    END) AS nb_reservations_en_cours,

    -- Revenu total de l'agence sur les 3 derniers mois
    COALESCE(SUM(
        CASE
            WHEN v.dateDebut >= CURRENT_DATE - INTERVAL '3 months'
            THEN v.PrixPersonne * (
                SELECT COUNT(*) FROM fait f2 WHERE f2.idVoy = v.idVoy
            )
        END
    ), 0) AS revenus_3_derniers_mois

FROM agence a
LEFT JOIN employe e ON e.idA = a.idA
LEFT JOIN voyage v ON v.planifie_par = e.idEmp
LEFT JOIN fait f ON f.idVoy = v.idVoy

GROUP BY a.idA, a.nom
ORDER BY a.nom;
