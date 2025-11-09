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
    adresse text
);

CREATE TABLE pays(
    codeP char(3) primary key,
    nom varchar(25)
);

CREATE TABLE ville(
    idVille serial primary key,
    nom varchar(20),
    pays char(3) references pays(codeP),
    descriptif text
);

CREATE TABLE visa(
    idVisa serial primary key,
    typev varchar(10),
    prixVisa int,
);

CREATE TABLE client(
    idCli serial primary key,
    nom varchar(20),
    prenom varchar(15),
    sexe char(1),
    age int,
    nat char(3),
    adr varchar(30),
    numtel varchar(13),
    courriel varchar(25)
);

CREATE TABLE employe(
    idEmp serial primary key,
    nom varchar(20),
    prenom varchar(15),
    siteLogin varchar(10),
    mdp varchar(8),
    Travaille int references agence(idA),
    est_resp int references agence(idA)
);

CREATE TABLE etape( 
    idEt serial primary key,
    TyP varchar(20),
    transport varchar(15),
    depart int idVille references ville(idVille),
    arrivee int idVille references ville(idVille),
    dateDepart date NOT NULL,
    dateArrivee date NOT NULL
);

CREATE TABLE voyage(
    idVoy serial primary key,
    dateDebut date ,
    dateFin date ,
    PrixPersonne numeric(6,2),
    descriptif text,
    planifie_par int references employe(idEmp)
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
    primary key(idCli, codeP , idVisa)
);

CREATE TABLE parle(
    codeP int references pays(codeP),
    langue varchar(15),
    primary key(idCli, idVoy)
);


-- TABLE agence
INSERT INTO agence (nom, adresse) VALUES
('GlobeTrotter', '12 rue de la Paix, Paris'),
('Voyage2000', '7 avenue de la Liberté, Lyon'),
('Evasion360', '25 boulevard du Port, Marseille');

-- TABLE pays
INSERT INTO pays (codeP, nom) VALUES
('FRA', 'France'),
('ESP', 'Espagne'),
('ITA', 'Italie'),
('USA', 'États-Unis'),
('JPN', 'Japon'),
('MAR', 'Maroc');

-- TABLE ville
INSERT INTO ville (nom, pays, descriptif) VALUES
('Paris', 'FRA', 'Capitale française'),
('Lyon', 'FRA', 'Ville gastronomiqu'),
('Madrid', 'ESP', 'Capitale espagnole'),
('Barcelone', 'ESP', 'Ville côtière avec la Sagrada Familia'),
('Rome', 'ITA', 'Capitale italienne, sympa'),
('Venise', 'ITA', 'Ville romantique'),
('New York', 'USA', 'Métropole mondiale, gratte-ciels'),
('Los Angeles', 'USA', 'Ville du cinéma'),
('Tokyo', 'JPN', 'Capitale moderne du Japon'),
('Kyoto', 'JPN', 'Ancienne capitale, temples et traditions'),
('Marrakech', 'MAR', 'Ville rouge, médina animée'),
('Casablanca', 'MAR', 'Capitale économique du Maroc');

-- TABLE visa
INSERT INTO visa (typev, prixVisa) VALUES
('Tourisme', 80),
('Affaires', 120),
('Études', 150),
('Transit', 40);

-- TABLE client
INSERT INTO client (nom, prenom, sexe, age, nat, adr, numtel, courriel) VALUES
('Durand', 'Alice', 'F', 28, 'FRA', '5 rue Victor Hugo, Paris', '+33645121212', 'alice.durand@mail.fr'),
('Martin', 'Lucas', 'M', 35, 'FRA', '12 avenue Foch, Lyon', '+33688223344', 'lucas.martin@mail.fr'),
('Garcia', 'Sofia', 'F', 42, 'ESP', '8 calle Mayor, Madrid', '+34915554444', 'sofia.garcia@mail.es'),
('Rossi', 'Marco', 'M', 31, 'ITA', 'Via Roma 10, Rome', '+39066555123', 'marco.rossi@mail.it'),
('Smith', 'John', 'M', 45, 'USA', '123 5th Ave, New York', '+12125551234', 'john.smith@mail.com'),
('Tanaka', 'Yuki', 'F', 26, 'JPN', '2-3-5 Shibuya, Tokyo', '+81345551212', 'yuki.tanaka@mail.jp'),
('Bennani', 'Sara', 'F', 33, 'MAR', '45 rue Mohamed V, Marrakech', '+212655123123', 'sara.bennani@mail.ma'),
('Nguyen', 'Linh', 'F', 29, 'FRA', '3 rue de Provence, Lyon', '+33655887799', 'linh.nguyen@mail.fr'),
('Dupont', 'Julien', 'M', 38, 'FRA', '1 rue de la Gare, Paris', '+33677554411', 'julien.dupont@mail.fr'),
('Lopez', 'Carlos', 'M', 41, 'ESP', 'Calle del Sol 25, Barcelone', '+34911223355', 'carlos.lopez@mail.es');

-- TABLE employe
INSERT INTO employe (nom, prenom, siteLogin, mdp, Travaille, est_resp) VALUES
('Deneuville', 'Damian', 'ddamian', 'azerty12', 1, 1),
('Moreau', 'Jean', 'jmoreau', 'voyage1', 1, NULL),
('Lefevre', 'Paul', 'plefevre', 'passe123', 2, 2),
('Dubois', 'Emma', 'edubois', 'soleil99', 2, NULL),
('Petit', 'Nina', 'npetit', 'monde01', 3, 3);

-- TABLE voyage
INSERT INTO voyage (dateDebut, dateFin, PrixPersonne, descriptif, planifie_par) VALUES
('2025-02-10', '2025-02-20', 1500.00, 'Circuit culturel en Italie', 1),
('2025-03-01', '2025-03-10', 2300.00, 'Découverte du Japon', 5),
('2025-04-15', '2025-04-25', 1800.00, 'Voyage gastronomique en Espagne', 3),
('2025-05-05', '2025-05-15', 2100.00, 'Road trip aux États-Unis', 4),
('2025-06-10', '2025-06-17', 1200.00, 'Séjour au Maroc', 2);

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
(10, 5);

-- TABLE obtient
-- Quels clients ont obtenu quels visas
INSERT INTO obtient (idCli, idVisa) VALUES
(1, 1),
(2, 2),
(3, 1),
(4, 1),
(5, 2),
(6, 3),
(7, 1),
(8, 1),
(9, 2),
(10, 1);

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
