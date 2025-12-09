# Bon Voyage :
## Plateforme de gestion et de réservation



### 1 Présentation générale
La compagnie de voyage Bon Voyage souhaite construire une plateforme permettant à ses employés de planifier des voyages complets (comprenant les trajets et permettant de visiter une ou plusieurs destinations) pour les proposer à la réservation sur son site web. Le présent document recense les besoins et attentes du client.


### 2 Les utilisateurs
La compagnie a plusieurs agences sur le territoire français. Chaque agence a plusieurs employés, dont un (et un seul) responsable. Chaque employé possède un login et un mot de passe qui donne certains droits d'administrations du site, comme l'ajout et la modification ou l'annulation des voyages de son agence. Le responsable peut en plus créer, modifier et supprimer les comptes des employés de son agence.
Pour chaque client, on connaît son nom, son prénom, son sexe, son âge, sa nationalité, son adresse, son numéro de téléphone et son courriel, tous obligatoires à l'inscription.


### 3 Les voyages et leurs étapes
Les voyages sont constitués de plusieurs étapes. Chaque étape peut être d'un type différent (croisière, hôtel, etc.) et comprendre un moyen de transport (train, avion, etc.) qui sert à relier deux villes. Pour chaque étape, il est possible de préciser la durée, la date de départ et la date d'arrivée.
Par exemple, un voyage peut être planifié ainsi :
- départ de Londres le 2 octobre en train jusqu'à Brindisi et arrivée le 8 octobre, départ de Brindisi à Suez en ferry du 9 octobre au 10 octobre,
-  croisière de Suez à Bombay du 11 au 23 octobre,
 retour à Londres en avion le 25 octobre.

On notera qu'il existe plusieurs hôtels, auberges et campings dans une même ville.
Pour chaque voyage on connaît le coût par personne, la date du début et celle de fin.
Un client peut aussi être intéressé par une brève description du pays, ses langues parlées, etc. Certains voyages nécessitent différents visas (parfois payant) selon les pays visités et la nationalité des voyageurs.


### 4 Le site web
Le site web de Bon Voyage sera découpé en deux parties : l'une privée pour les
employés de la compagnie, et l'autre publique pour les clients.

#### 4.1 Côté employé
- Une page de gestion des comptes utilisateurs, permettant aux responsables de gérer les comptes des employés de son agence.
- Une page de liste de voyages, permettant aux employés de lister, de créer, de modifier et de supprimer des voyages dans son agence.
- Une page de gestion par voyage, permettant de d'éditer ses détails et ses étapes, et de gérer les réservations des clients sur le voyage en question.

#### 4.2 Côté client
- Une page de connexion, proposant à un client déjà inscrit de rentrer son identifiant et mot de passe pour s'identifier, ou à un nouveau client de remplir un formulaire pour créer son compte.
Une page de recherche de voyages, affichant la liste des voyages à venir disponibles à la réservation. Cette page doit permettre au client de pouvoir rechercher et filtrer sur les destinations et dates de son choix.
Une page par voyage, permettant de voir ses détails, ses étapes et les coordonnées de l'agence qui l'organise. Elle permet au client de réserver, à condition qu'il ou elle ne soit pas inscrit à un autre voyage dont les dates se chevaucheraient.
— Une page compte utilisateur, permettant au client de modifier ses informations personnelles et de voir toutes ses réservations actuelles et passées.
