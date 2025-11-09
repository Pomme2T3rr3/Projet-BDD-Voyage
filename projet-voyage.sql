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



CREATE TABLE agence{
    idA serial primary key,
    nom varchar(25),
    adresse text
};

CREATE TABLE pays{
    codeP char(3) primary key,
    nom varchar(25) 
};

CREATE TABLE ville{
    idVille serial primary key,
    nom varchar(20),
    pays char(3) references pays(codeP), 
    descriptif text 
};

CREATE TABLE visa{
    idVisa serial primary key,
    typev varchar(10),
    prixVisa int, 
};

CREATE TABLE client{
    idCli serial primary key,
    nom varchar(20),
    prenom varchar(15),
    sexe char(1),
    age int,
    nat char(3),
    adr varchar(30),
    numtel varchar(13),
    courriel varchar(25)
};

CREATE TABLE employe{
    idEmp serial primary key,
    nom varchar(20),
    prenom varchar(15),
    siteLogin varchar(10),
    mdp varchar(8),
    Travaille int references agence(idA),
    est_resp int references agence(idA)
};

CREATE TABLE etape{
    idEt serial primary key,
    TyP varchar(20),
    transport varchar(15),
    depart int idVille references ville(idVille),
    arrivee int idVille references ville(idVille),
    dateDepart date NOT NULL,
    dateArrivee date NOT NULL
};

CREATE TABLE voyage{
    idVoy serial primary key,
    dateDebut date ,
    dateFin date ,
    PrixPersonne numeric(6,2),
    descriptif text,
    planifie_par int references employe(idEmp)
};
/*
 --- Creation de tables des associations ---
*/
CREATE TABLE fait{
    idCli int references client(idCli), 
    idVoy int references voyage(idVoy),
    primary key(idCli, idVoy) 
};

CREATE TABLE constitue{
    idVoy int references voyage(idVoy), 
    idEt int references etape(idEt),
    primary key(idVoy, idEt) 
};

CREATE TABLE obtient{
    idCli int references client(idCli), 
    codeP char(3) references pays(codeP),
    idVisa int references visa(idVisa),
    primary key(idCli, codeP , idVisa) 
};

CREATE TABLE parle{
    codeP int references pays(codeP),
    langue varchar(15),
    primary key(idCli, idVoy) 
};
