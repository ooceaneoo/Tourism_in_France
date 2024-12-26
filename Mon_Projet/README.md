# Analyse des Fréquentations Touristiques en France

## Introduction & Objectifs
Ce tableau de bord interactif vise à fournir une analyse approfondie des dynamiques et tendances du tourisme en France, en exploitant les données publiques de l’INSEE sur la fréquentation des hébergements touristiques. 

### Les principaux objectifs incluent :

- L'exploration des données : permettre aux utilisateurs d’explorer les données sur les flux touristiques de manière intuitive et efficace. 

- La visualisation des tendances : offrir des graphiques dynamiques mettant en évidence les évolutions et tendances clés du tourisme français.

- Les comparaisons entre départements : fournir une interface permettant de comparer l'ensemble des départements français à travers l'indicateur de notre choix. 

Cette application permet ainsi de rendre les données accessibles et exploitables dans une interface simple d'utilisation, mais également de visualiser les points et tendances clés du tourisme français.

### À noter : 
Une grande partie de l'application est consacrée à l'exploration des données pour des raisons pratiques. Contrairement à l’interface d'exploration de l’INSEE, souvent complexe en raison du grand nombre d’indicateurs et de filtres présentés de manière peu lisible, cette application adopte une logique simplifiée.

Les filtres sont conçus pour être à la fois interactifs et intelligents :

- Chaque filtre présenté à l’utilisateur est directement relié à des données disponibles. Contrairement à l’INSEE, où certains choix de filtrage mènent souvent à des résultats vides ("aucune donnée disponible"), notre application vérifie en amont la pertinence des options de filtrage. Ainsi, si un filtre est proposé, cela signifie que des données correspondantes sont présentes dans le système.

- La conception intuitive permet d’explorer les données sans être confronté à des impasses, améliorant l’expérience utilisateur.

- Les données sont présentées dans un format clair et compréhensible, à travers des tableaux et visualisations qui évitent les redondances et surcharges d’informations.

Cette approche garantit une expérience utilisateur simple d'utilisation.

## Source des données
Les données utilisées proviennent de l'API de l’INSEE sur les fréquentations touristiques :
https://catalogue-donnees.insee.fr/fr/catalogue/recherche/DS_TOUR_FREQ

## Les indicateurs

- Nombre d’arrivées (en milliers) : nombre total de touristes arrivant dans les hébergements/hotels.
- Nombre de jours du séjour (en unités) : durée des séjours des touristes dans les hébergements/hotels.
- Part des nuitées provenant de touristes étrangers (%) : proportion des nuitées réalisées par des touristes étrangers.
- Nombre de nuitées (en milliers) : total des nuits passées dans les hébergements/hotels par tout les touristes.
- Taux d’occupation des places (%) : pourcentage des places réellement occupées par rapport au nombre total de places offertes.

Tous concernent la fréquentation des hotels et hébergements.

## Les différentes sections
L'application est organisée en plusieurs sections intuitives pour une exploration optimale des données et une personnalisation des visualisations selon les besoins de l'utilisateur :

- Présentation : une introduction au projet présentant les objectifs.

- Visualisation du tourisme : cette section permet aux utilisateurs d'appliquer des filtres dynamiques pour explorer et récupérer les données de son choix.
  
- Comparaison inter-régions : cette section propose une comparaison géographique en mettant en évidence les disparités entre départements selon l'indicateur sélectionné. 
  
- Tendances : cette section affiche des graphiques interactifs pour analyser les évolutions et tendances clés du tourisme pour chaque indicateurs.
  
- Données : cette section offre une vue d’ensemble des indicateurs utilisés.

## Nettoyage des données et problèmes rencontrés
- Gestion des erreurs : Nous avons anticipé et pris en compte tous les cas de figure pouvant conduire à l’absence de données affichées. Cela garantit que chaque filtre ou critère propose uniquement des options associées à des données disponibles.

- Indicateur unique de mesure : Pour harmoniser les analyses, nous avons choisi de conserver uniquement un indicateur qui était disponible pour l’ensemble des données, ce qui a permis de garantir la cohérence des tendances, graphiques et comparaisons interrégions.

- Configuration des filtres : Certains filtres ont nécessité une configuration spécifique pour rendre certaines données accessibles. Cette étape a été complexe et a ajouté des détails supplémentaires au code, mais elle était essentielle pour garantir une exploration fluide.

- Traduction des noms des données : Les noms initialement fournis étant sous forme de codes, nous avons fait le choix de les traduire en termes clairs et compréhensibles pour les utilisateurs.

- Association des départements : Les départements étaient initialement présentés sous forme d’URL avec un identifiant INSEE. Nous avons résolu ce problème en créant un dictionnaire associant chaque identifiant à son nom de département correspondant. Cependant, cette partie a considérablement augmenté la complexité et la longueur du code.

## Axes d'amélioration
Il pourrait être intéressant de rajouter des analyses concernant le type d’hébergement, le type d’activité ou le type de territoire. 
Malheureusement, beaucoup de données sont manquantes, ce qui rend impossible, pour l’instant, d’effectuer des comparaisons annuelles ou entre départements. 
Les configurations sont également complexes pour certains indicateurs. Éviter les erreurs d’affichage et garantir un accès aux données nécessiteraient des configurations poussées, impliquant un travail de développement supplémentaire. 
Cela reste néanmoins une piste envisageable pour enrichir l’application.
