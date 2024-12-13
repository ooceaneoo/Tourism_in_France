import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px


def render_visualisation():

    #Disposition de la page en 2 colonnes : 
    col1, col2 = st.columns([1, 3]) #Agrandir la deuxième colonne

    #Ma colonne 1 :
    with col1:

        #Création d'un selectbox pour choisir la mesure :
        mesure = st.selectbox(
            "Sélectionnez une mesure :",
            ("Nombre d'arrivées", "Nombre de jours du séjour",
            "Part des nuitées provenant de touristes étrangers (%)", "Nombre de nuitées", "Taux d'occupation des places (%)"),
            key="mesure"
        )

        #Création d'un selectbox pour choisir le département :
        departement = st.selectbox(
            "Sélectionnez une zone géographique :",
            ("Aucun", "France", "01 - Ain", "02 - Aisne", "03 - Allier", "04 - Alpes-de-Haute-Provence",
            "05 - Hautes-Alpes", "06 - Alpes-Maritimes", "07 - Ardèche", "08 - Ardennes", "09 - Ariège", "10 - Aube",
            "11 - Aude", "12 - Aveyron", "13 - Bouches-du-Rhône", "14 - Calvados", "15 - Cantal", "16 - Charente",
            "17 - Charente-Maritime", "18 - Cher", "19 - Corrèze", "21 - Côte-d'Or", "22 - Côtes-d'Armor",
            "23 - Creuse", "24 - Dordogne", "25 - Doubs", "26 - Drôme", "27 - Eure", "28 - Eure-et-Loir",
            "29 - Finistère", "30 - Gard", "31 - Haute-Garonne", "32 - Gers", "33 - Gironde", "34 - Hérault",
            "35 - Ille-et-Vilaine", "36 - Indre", "37 - Indre-et-Loire", "38 - Isère", "39 - Jura", "40 - Landes",
            "41 - Loir-et-Cher", "42 - Loire", "43 - Haute-Loire", "44 - Loire-Atlantique", "45 - Loiret",
            "46 - Lot", "47 - Lot-et-Garonne", "48 - Lozère", "49 - Maine-et-Loire", "50 - Manche", "51 - Marne",
            "52 - Haute-Marne", "53 - Mayenne", "54 - Meurthe-et-Moselle", "55 - Meuse", "56 - Morbihan",
            "57 - Moselle", "58 - Nièvre", "59 - Nord", "60 - Oise", "61 - Orne", "62 - Pas-de-Calais",
            "63 - Puy-de-Dôme", "64 - Pyrénées-Atlantiques", "65 - Hautes-Pyrénées", "66 - Pyrénées-Orientales",
            "67 - Bas-Rhin", "68 - Haut-Rhin", "69 - Rhône", "70 - Haute-Saône", "71 - Saône-et-Loire",
            "72 - Sarthe", "73 - Savoie", "74 - Haute-Savoie", "75 - Paris", "76 - Seine-Maritime", "77 - Seine-et-Marne",
            "78 - Yvelines", "79 - Deux-Sèvres", "80 - Somme", "81 - Tarn", "82 - Tarn-et-Garonne", "83 - Var",
            "84 - Vaucluse", "85 - Vendée", "86 - Vienne", "87 - Haute-Vienne", "88 - Vosges", "89 - Yonne",
            "90 - Territoire de Belfort", "91 - Essonne", "92 - Hauts-de-Seine", "93 - Seine-Saint-Denis",
            "94 - Val-de-Marne", "95 - Val-d'Oise", "971 - Guadeloupe", "972 - Martinique", "973 - Guyane",
            "974 - La Réunion", "976 - Mayotte", "2A - Corse du sud", "2B - Haute-Corse"),
            key="departement"
        )

        #Variable qui désigne les mesures excluant l'année 2024 : 
        ##Pour certaines mesures, les données de l'année 2024 ne sont pas disponible##
        mesures_excluant_2024 = [
            "Nombre de jours du séjour",
            "Part des nuitées provenant de touristes étrangers (%)",
            "Taux d'occupation des places (%)"
        ]

        #Création d'un selectbox pour choisir l'année en prenant en compte la mesure selectionnée :
        ##Pour certaines mesures, les données de l'année 2024 ne sont pas disponible##
        annee = st.selectbox(
            "Sélectionnez une année :",
            [str(i) for i in range(2011, 2024)] if mesure in mesures_excluant_2024 else [str(i) for i in range(2011, 2025)],
            key="annee"
        )
        
        #Variable qui désigne les mesures où le choix du mois est obligatoire car pas de données annuelles : 
        mesures_mois_obligatoire = [
        "Nombre d'arrivées", 
        "Nombre de nuitées", 
        "Nombre d'établissements", 
        "Taux d'occupation des places (%)"
        ]

        #Variable qui désigne les mesures où le choix du mois est désactivé car pas de données mensuelles :
        mesures_sans_mois = [
            "Nombre de jours du séjour",
            "Part des nuitées provenant de touristes étrangers (%)",
        ]

        #Variable qui désigne les mesures où le choix du mois doit exclure octobre, novembre et décembre car pas de données (logique) :
        mesures_excluant_derniers_mois = [
            "Nombre d'arrivées", "Nombre de nuitées"
        ]

        #Boucle qui prend en compte les paramètres précédents pour créer le SelectBox "Mois" :
        if mesure in mesures_sans_mois:
            mois = "Aucun"  # Aucun choix possible pour ces mesures
        else:
            if mesure == "Taux d'occupation des places (%)":  # Si la mesure est spécifique, ne pas permettre "Aucun"
                mois_options = ["01 - Janvier", "02 - Février", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin", 
                                "07 - Juillet", "08 - Août", "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Décembre"]
            else:
                if annee == "2024" and mesure in mesures_excluant_derniers_mois:
                    # Si l'année est 2024 et la mesure est "Nombre d'arrivées" ou "Nombre de nuitées", on exclut octobre, novembre, décembre
                    mois_options = ["01 - Janvier", "02 - Février", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin", 
                                    "07 - Juillet", "08 - Août", "09 - Septembre"]
                else:
                    # Si la mesure exige un mois obligatoire (autres contraintes)
                    if mesure in mesures_mois_obligatoire:
                        mois_options = ["Aucun", "01 - Janvier", "02 - Février", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin", 
                                        "07 - Juillet", "08 - Août", "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Décembre"]
                    else:
                        # Sinon, on inclut l'option "Aucun"
                        mois_options = ["Aucun", "01 - Janvier", "02 - Février", "03 - Mars", "04 - Avril", "05 - Mai", "06 - Juin",
                                        "07 - Juillet", "08 - Août", "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Décembre"]

            mois = st.selectbox(
                "Sélectionnez un mois :",
                mois_options,
                key="mois"
            )

        
        #Apparence des SelectBox :
        st.markdown(
        """
        <style>
            .stSelectbox {
                width: 10px;
                background-color: #FBFCFA;
                color: BLACk;
                padding: 0px;
                font-size: 15px;
                border-radius: 10px;
                margin-top: 10px;

            }
        </style>
        """, unsafe_allow_html=True
        )

        #---------------------------------------------- DICTIONNAIRE DONNÉES ET CONTRAINTES POUR CONSTRUCTION API ----------------------------------------------#

        #Dictionnaire de données des mesures :
        mesure_mapping = {
            "Nombre d'arrivées": "ARR",
            "Nombre de jours du séjour": "DAYS_STAY",
            "Part des nuitées provenant de touristes étrangers (%)": "NON_RESIDENT_NIGHTSPENT_RATIO",
            "Nombre de nuitées": "NUI",
            "Nombre de places offertes": "PLACE_AVAIL",
            "Taux d'occupation des places (%)": "PLACE_OCCUPANCY_RATE",
            "Nombre de places occupées": "PLACE_USED",
            "Nombre d'établissements": "UNIT_LOC"
        }

        #Variable qui récupére le mois sélectionné et le code du mois
        mois_code = mois.split(" - ")[0] if mois != "Aucun" else ""

        #Définir la fréquence (A pour Annuel si "Aucun", M pour Mensuel sinon)
        frequence = "A" if mois == "Aucun" else "M"

        #Définir la période de temps (année ou année-mois)
        time_period = f"{annee}-{mois_code}" if mois_code else annee

        #Boucle qui permet de récupérer l'élément GEO dans l'API : 
        if departement == "France":
            #Si "France" est sélectionnée, on utilise GEO=FRANCE
            geo = "GEO=FRANCE"
        elif departement != "Aucun":
            #Sinon, on utilise le code du département
            departement_code = departement.split(" - ")[0]  #Récupère le code département
            geo = f"GEO=2023-DEP-{departement_code}"  #Format attendu par l'API
        else:
            #Si aucun département n'est sélectionné
            geo = "GEO=DEP"  #Pas de département spécifique, affichage global
            
        #Récupération du code de la mesure selectionnée pour l'API : 
        mesure_code = mesure_mapping[mesure]

        #Aucune restriction sur unit_mult ou decimals pour l'API : 
        unit_mult = ""
        decimals = "" 

        #Variable qui liste les mesures qui nécessitent le filtre "Origine du Touriste" (car données disponibles) :
        mesures_avec_filtre_origine = [
        "Nombre d'arrivées", 
        "Nombre de jours du séjour", 
        "Nombre de nuitées"
        ]

        #Boucle qui affiche le filtre "Origine du Touriste" uniquement si la mesure sélectionnée le permet :
        origine_touriste = None  # Valeur par défaut
        if mesure in mesures_avec_filtre_origine:
            origine_touriste = st.selectbox(
                "Filtrer par origine des touristes :",
                ("Tous", "France", "Étranger", "Total")  # Options disponibles
            )

        #Dictionnaire "Origine du Touriste" pour l'API : 
        origine_touriste_mapping = {
            "France": "250",
            "Étranger": "1_X_250",
            "Total": "_T",
            "Tous": None  # Pas de filtre pour "Tous"
        }

        #Récupération du code correspondant à "Origine du Touriste" pour l'API :
        origine_code = origine_touriste_mapping.get(origine_touriste)

        #---------------------------------------------- CONSTRUCTION URL API ----------------------------------------------#

        #Modalités API : 
        API_URL = (
            f"https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000"
            f"&TIME_PERIOD={time_period}"
            f"&FREQ={frequence}"
            f"&TOUR_MEASURE={mesure_code}"
            f"&{geo}"  # Paramètre GEO construit correctement
        )

        #Ajout du filtre "Origine du Touriste" dans l'URL si applicable :
        if origine_code:  #Ajouter seulement si un filtre spécifique est sélectionné (pas obligatoire)
            API_URL += f"&TOUR_RESID={origine_code}"

        #Si le département est "France", je choisis "Total" pour les mesures qu'on ne souhaite pas observer (Type de géographie territoriale, Classement, Type d'hotel) :
        if departement == "France":
            geo_terr_code = "_T"  #Pas de filtre spécifique pour la géographie
            classement_code = "_T"  #Pas de filtre spécifique pour le classement
            type_hotel_code = "_T" #Pas de filtre spécifique pour le type d'hotel
            API_URL += f"&UNIT_LOC_RANKING={classement_code}"  #Ajouter le paramètre classement à l'URL
            API_URL += f"&TERRTYPO={geo_terr_code}"  #Ajouter le paramètre géographie territoriale à l'URL
            API_URL += f"&HOTEL_STA={type_hotel_code}"  #Ajouter le paramètre type hotel à l'URL


        #Ajout conditionnel : seulement si unit_mult ou decimals sont requis : 
        if unit_mult:
            API_URL += f"&UNIT_MULT={unit_mult}"
        if decimals:
            API_URL += f"&DECIMALS={decimals}"

    #Ma colonne 2 :
    with col2:

        #Apparence du bouton "Afficher les données" :
        st.markdown("""
        <style>
        .stButton {
            background-color: transparent;  /* Fond transparent pour le conteneur du bouton */
            border: none;  /* Enlever la bordure du conteneur */
            padding: 0;  /* Enlever le padding du conteneur */
            margin-top: 20px;
            margin-left: 290px;

        }
        .stButton > button {
            background-color: #FBFCFA;  /* Couleur de fond du bouton */
            width: 500px;  /* Largeur du bouton */
            height: 50px;  /* Hauteur du bouton */
            border: 0px solid black;  /* Contour noir fin */
            border-radius: 100px;  /* Bords arrondis */
            padding: 0;  /* Enlever tout padding du bouton */
            font-size: 200px;
        }
        /* Empêche le changement de couleur au survol */
        .stButton > button:hover {
            background-color: #FBFCFA;  /* Garde la même couleur de fond au survol */
        }
        </style>            
                        
        """, unsafe_allow_html=True)

        #Affichage des données :
        if st.button("Afficher les données"):
                
            try:
                #Dictionnaire pour traduire les valeurs de TOUR_RESID
                tour_resid_mapping = {
                    "_T": "Total",
                    "1_X_250": "Etranger",
                    "142": "Asie",
                    "150": "Europe",
                    "156": "Chine",
                    "19": "Amériques",
                    "2": "Afrique",
                    "250": "France",
                    "276": "Allemagne",
                    "380": "Italie",
                    "392": "Japon",
                    "5_13": "Amérique centrale et du sud",
                    "528": "Pays-Bas",
                    "56": "Belgique",
                    "643": "Russie",
                    "724": "Espagne",
                    "756": "Suisse",
                    "826": "Royaume-Uni",
                    "840": "Etats-Unis d'Amérique",
                    "TOUR_PMO": "Proche et Moyen Orient",
                }

                #Effectuer la requête HTTP
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})
                if response.status_code == 200:
                    data = response.json()

                    #Vérification des clés disponibles
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré
                        rows = []
                        for obs in observations:
                            row = {
                                **obs["dimensions"],  #Ajoute toutes les dimensions comme colonnes
                                **obs["attributes"],  #Ajoute tous les attributs comme colonnes
                            }
                            #Traduire la valeur de TOUR_RESID si présente
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = tour_resid_mapping.get(row["TOUR_RESID"], row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    if "value" in measure_data:
                                        row[measure_name] = measure_data["value"]
                                    else:
                                        row[measure_name] = None  #Valeur par défaut si "value" est absent
                            rows.append(row)

                        #Création d'un DataFrame pandas :
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes :
                        rename_columns = {
                        "TOUR_RESID": "Origine du Touriste",
                        "PLACE_OCCUPANCY_RATE": "Taux d'occupation des places (%)",
                        "OBS_VALUE_NIVEAU": "Valeur",
                        "ACTIVITY": "Activité économique",
                        "TIME_PERIOD" : "Période",
                        "TOUR_MEASURE" : "Mesure du tourisme",
                        "GEO" : "Département",
                        "FREQ" : "Fréquence",
                        "TERRTYPO" : "Géographie territoriale",
                        "UNIT_LOC_RANKING" : "Classement",
                        }

                        #Appliquer le renommage des colonnes :
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes :
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Dictionnaires pour remplacer les valeurs des colonnes :
                        frequence_mapping = {
                            "M": "Mensuel",
                            "A": "Annuel"
                        }

                        mesure_mapping = {
                            "ARR": "Nombre d’arrivées",
                            "DAYS_STAY": "Nombre de jours du séjour",
                            "NON_RESIDENT_NIGHTSPENT_RATIO": "Part des nuitées provenant de touristes étrangers (%)",
                            "NUI": "Nombre de nuitées",
                            "PLACE_AVAIL": "Nombre de places offertes",
                            "PLACE_OCCUPANCY_RATE": "Taux d’occupation des places (%)",
                            "PLACE_USED": "Nombre de places occupées",
                            "UNIT_LOC": "Nombre d’établissements"
                        }

                        activite_mapping = {
                            "I55": "Hébergement",
                            "I551": "Hôtels et hébergement similaire",
                            "I552": "Hébergement touristique et autre hébergement de courte durée",
                            "I552A_I552C": "Villages vacances et maisons familiales et Auberges de jeunesse et centres sportifs",
                            "I552B": "Résidences de tourisme – Résidences hôtelières",
                            "I553": "Terrains de camping et parcs pour caravanes ou véhicules de loisirs"
                        }

                        #Dictionnaire de traduction pour Géographie territoriale (TERRTYPO) :
                        territory_mapping = {
                        "_T": "Total",
                        "1": "Île-de-France",
                        "2": "Littoral",
                        "3": "Massifs de ski ou massifs de montagne",
                        "4": "Urbain de province",
                        "5": "Autres espaces",
                        "N_CST": "Non littoral"
                        }

                        #Dictionnaire de traduction pour le classement (UNIT_LOC_RANKING) :
                        ranking_mapping = {
                            "_T": "Total",
                            "1T2": "1 et 2 étoiles",
                            "3": "3 étoiles",
                            "4T5": "4 et 5 étoiles",
                            "C": "Classé",
                            "NC": "Non classé"
                        }


                        #Application des remplacements dans les colonnes spécifiques :
                        df["Fréquence"] = df["Fréquence"].replace(frequence_mapping)
                        df["Mesure du tourisme"] = df["Mesure du tourisme"].replace(mesure_mapping)
                        df["Activité économique"] = df["Activité économique"].replace(activite_mapping)
                        df["Classement"] = df["Classement"].replace(ranking_mapping)
                        df["Géographie territoriale"] = df["Géographie territoriale"].replace(territory_mapping)

                        #Suppression des colonnes désignées : 
                        df = df.drop(columns=["Géographie territoriale", "Classement"])

                        #Remplacer le nom des données de la colonne "Département" : 
                        departementss_mapping = {
                        "http://id.insee.fr/geo/departement/84680e6f-2e99-44c9-a9ba-2e96a2ae48b7": "01 - Ain",
                        "http://id.insee.fr/geo/departement/2cac54dd-bfc6-42f2-a14e-9848aca615f8": "02 - Allier",
                        "http://id.insee.fr/geo/departement/8b195d1f-8676-4c06-873c-ee5b6d66a23f": "03 - Aisne",
                        "http://id.insee.fr/geo/departement/179b6382-6cbe-4dce-84c6-babab2ab4072": "04 - Alpes-de-Haute-Provence",
                        "http://id.insee.fr/geo/departement/4b0642d5-8596-4c7c-8d44-9d8c011a295d": "05 - Hautes-Alpes",
                        "http://id.insee.fr/geo/departement/f18b4c44-0711-4562-975f-3031491da615": "06 - Alpes-Maritimes",
                        "http://id.insee.fr/geo/departement/638877e3-b623-4f0c-9edc-0e39e93a944f": "07 - Ardèche",
                        "http://id.insee.fr/geo/departement/db31b809-e602-44f6-a7c5-05907af2bd36": "08 - Ardennes",
                        "http://id.insee.fr/geo/departement/ed312031-2409-431a-b1d0-7f2c3c317395": "09 - Ariège",
                        "http://id.insee.fr/geo/departement/a8e76039-fbda-4ad3-b71c-36142ac7d84f": "10 - Aube",
                        "http://id.insee.fr/geo/departement/87930345-b296-42d8-bd65-8bcfec80b3fa": "11 - Aude",
                        "http://id.insee.fr/geo/departement/1624ef06-3f52-4346-a05b-a4f9d430fd92": "12 - Aveyron",
                        "http://id.insee.fr/geo/departement/076b614a-0df0-4058-8cae-b768480a673f": "13 - Bouches-du-Rhône",
                        "http://id.insee.fr/geo/departement/b01dce92-b91f-4648-80e7-536bd1823c2c": "14 - Calvados",
                        "http://id.insee.fr/geo/departement/aa5572b4-ba15-41d8-a0de-7dd90d7ec39b": "15 - Cantal",
                        "http://id.insee.fr/geo/departement/c1632a2f-4bc8-4397-85f8-0c6ab21cb64b": "16 - Charente",
                        "http://id.insee.fr/geo/departement/7a8b72df-7547-41d9-9477-a8eb01c10804": "17 - Charente-Maritime",
                        "http://id.insee.fr/geo/departement/7c2fd9ef-83e9-4fe0-bcf2-1b062042ac7a": "18 - Cher",
                        "http://id.insee.fr/geo/departement/d0e664ba-7dd4-4249-b005-4704fd8d8104": "19 - Corrèze",
                        "http://id.insee.fr/geo/departement/5a1a6fc3-f1bb-4d70-a0d5-3673d621f1ce": "21 - Côte-d'Or",
                        "http://id.insee.fr/geo/departement/f07f6a49-9dce-4f2d-a99e-5d61eedf2827": "22 - Côtes-d'Armor",
                        "http://id.insee.fr/geo/departement/353873a3-8a44-4e7a-860a-739e511f3ee7": "23 - Creuse",
                        "http://id.insee.fr/geo/departement/e27cdbdb-cc4f-467f-9f8c-d60b799da7e5": "24 - Dordogne",
                        "http://id.insee.fr/geo/departement/02a64b31-3d10-4784-84ec-2b75d725d602": "25 - Doubs",
                        "http://id.insee.fr/geo/departement/f4e636cd-22c9-4b62-817d-b384965bcf1b": "26 - Drôme",
                        "http://id.insee.fr/geo/departement/3038a0ec-c80a-4928-afc3-62a4ee9a6c5d": "27 - Eure",
                        "http://id.insee.fr/geo/departement/93aca780-1cb8-45f6-9fd7-3f5c3dfe8dbc": "28 - Eure-et-Loir",
                        "http://id.insee.fr/geo/departement/c9a64ff2-3e80-44b3-8224-a322cb838f30": "29 - Finistère",
                        "http://id.insee.fr/geo/departement/b6168b3e-9c83-4c64-9595-c1c1926b522f": "30 - Gard",
                        "http://id.insee.fr/geo/departement/c77569fe-6c4a-42c7-88af-d7145b3aa48f": "31 - Haute-Garonne",
                        "http://id.insee.fr/geo/departement/7357e721-4730-4635-9fe8-4899b0261e5b": "32 - Gers",
                        "http://id.insee.fr/geo/departement/bee9c7ed-221a-46be-9e42-8b815ce285c4": "33 - Gironde",
                        "http://id.insee.fr/geo/departement/a82518c0-bced-4c05-86a3-8d61efcaa232": "34 - Hérault",
                        "http://id.insee.fr/geo/departement/0ccd93c6-4740-4a16-9487-8e82be46a1c7": "35 - Ille-et-Vilaine",
                        "http://id.insee.fr/geo/departement/1881a325-4331-41ba-b807-6ac5deb9dced": "36 - Indre",
                        "http://id.insee.fr/geo/departement/6f46003b-330d-4996-b393-be225f468927": "37 - Indre-et-Loire",
                        "http://id.insee.fr/geo/departement/3a4bb8dc-71a7-4473-8a59-d138d8b1ef50": "38 - Isère",
                        "http://id.insee.fr/geo/departement/be208a7a-533a-403e-9373-db803fc6728b": "39 - Jura",
                        "http://id.insee.fr/geo/departement/375673af-f735-4304-8655-01964a7be12a": "40 - Landes",
                        "http://id.insee.fr/geo/departement/183f5512-c89b-4479-979e-a944870addb5": "41 - Loir-et-Cher",
                        "http://id.insee.fr/geo/departement/dbc42c2f-cc52-46a1-84c5-5ab59c44ec03": "42 - Loire",
                        "http://id.insee.fr/geo/departement/8c3901ab-9f83-411c-9679-ba22b220f339": "43 - Haute-Loire",
                        "http://id.insee.fr/geo/departement/4761bb5b-2684-47af-809d-5459d8539302": "44 - Loire-Atlantique",
                        "http://id.insee.fr/geo/departement/b5ead09a-5263-4635-94ee-aa7e1ccbd41e": "45 - Loiret",
                        "http://id.insee.fr/geo/departement/dbb175d9-0997-44bc-9d3c-a6f17e61f141": "46 - Lot",
                        "http://id.insee.fr/geo/departement/7fe0dec5-86cb-4437-bed7-b729633abec3": "47 - Lot-et-Garonne",
                        "http://id.insee.fr/geo/departement/ae1df568-6374-49c3-b464-deaf06c460b3": "48 - Lozère",
                        "http://id.insee.fr/geo/departement/e7f49648-56ed-41ab-a70b-a612422799b7": "49 - Maine-et-Loire",
                        "http://id.insee.fr/geo/departement/4c8cb5a2-6cda-4ab6-b180-c496e6d3d3dd": "50 - Manche",
                        "http://id.insee.fr/geo/departement/5bd27c2f-eb0c-4ed5-9be1-5fa3dfd63e6a": "51 - Marne",
                        "http://id.insee.fr/geo/departement/cbd705a7-0d80-4bde-a073-d3e64b479bae": "52 - Haute-Marne",
                        "http://id.insee.fr/geo/departement/c19482f0-6dd0-4cde-939f-0bc48553c157": "53 - Mayenne",
                        "http://id.insee.fr/geo/departement/761f468e-c041-4626-9b54-524d48de532b": "54 - Meurthe-et-Moselle",
                        "http://id.insee.fr/geo/departement/a31c20f1-29f2-4a58-970a-9b91ae8aace2": "55 - Meuse",
                        "http://id.insee.fr/geo/departement/2b16a315-574f-4452-9c55-7f7ca012d7d7": "56 - Morbihan",
                        "http://id.insee.fr/geo/departement/829f6473-e54d-496f-9c7d-bd34acdf212c": "57 - Moselle",
                        "http://id.insee.fr/geo/departement/3feb9f7f-c208-4bbf-8f5b-46c61dbcf217": "58 - Nièvre",
                        "http://id.insee.fr/geo/departement/1cabcdea-d4dc-4df1-96c2-ed1db0fa594c": "59 - Nord",
                        "http://id.insee.fr/geo/departement/488d603e-1ad3-4135-97df-ea01535d63d2": "60 - Oise",
                        "http://id.insee.fr/geo/departement/b2d181d4-f75a-4fb1-8e27-dc22cb2c3468": "61 - Orne",
                        "http://id.insee.fr/geo/departement/bf898ead-5a21-4964-aab6-8c51ffd5d89e": "62 - Pas-de-Calais",
                        "http://id.insee.fr/geo/departement/a5aedd31-9278-4505-850d-641997047b42": "63 - Puy-de-Dôme",
                        "http://id.insee.fr/geo/departement/4723b562-b592-42c7-b624-34830fc19296": "64 - Pyrénées-Atlantiques",
                        "http://id.insee.fr/geo/departement/209672ec-0451-419e-adc0-619cadc2f298": "65 - Hautes-Pyrénées",
                        "http://id.insee.fr/geo/departement/85f92734-0bae-4812-b859-9b1d0422aeac": "66 - Pyrénées-Orientales",
                        "http://id.insee.fr/geo/departement/e62b35df-f168-4dfa-b60f-ef6cdb3279a0": "67 - Bas-Rhin",
                        "http://id.insee.fr/geo/departement/f431fd7c-5ec4-43d7-949d-f601ea03397a": "68 - Haut-Rhin",
                        "http://id.insee.fr/geo/departement/8782c0ee-dc75-4fad-aac1-7470109fb0fa": "69 - Rhône",
                        "http://id.insee.fr/geo/departement/28ef2156-9a14-4d9d-a34b-5a4547dcd770": "70 - Haute-Saône",
                        "http://id.insee.fr/geo/departement/0285b2e7-0593-4854-9a47-120d5768a79d": "71 - Saône-et-Loire",
                        "http://id.insee.fr/geo/departement/17b2bca9-bb15-457b-834b-ceab9041240c": "72 - Sarthe",
                        "http://id.insee.fr/geo/departement/50590a56-da61-4963-9c86-432ed63dc083": "73 - Savoie",
                        "http://id.insee.fr/geo/departement/8dfbed51-33ee-4f64-9a1b-476077a450b4": "74 - Haute-Savoie",
                        "http://id.insee.fr/geo/departement/973f58f8-e45f-468d-b91f-03d28bcd08ee": "75 - Paris",
                        "http://id.insee.fr/geo/departement/58a92569-96cf-4a17-b1cc-1a4788bda23f": "76 - Seine-Maritime",
                        "http://id.insee.fr/geo/departement/d4da996f-4159-43df-b2ec-ee107c9a1010": "77 - Seine-et-Marne",
                        "http://id.insee.fr/geo/departement/693c468c-26e6-4fc4-98c1-bba143f7b8d3": "78 - Yvelines",
                        "http://id.insee.fr/geo/departement/260e696c-f34e-429c-82c5-3c9a367d4f7f": "79 - Deux-Sèvres",
                        "http://id.insee.fr/geo/departement/c2c4a2e8-8d4c-4dd8-be3c-a05f1c914b6c": "80 - Somme",
                        "http://id.insee.fr/geo/departement/f30d4384-d4e7-4f39-9621-90d1b50e72f7": "81 - Tarn",
                        "http://id.insee.fr/geo/departement/ae484d01-10d7-49cc-8a72-2c9159b49d62": "82 - Tarn-et-Garonne",
                        "http://id.insee.fr/geo/departement/3c6b7d54-939d-43ad-b91a-2628e048cd75": "83 - Var",
                        "http://id.insee.fr/geo/departement/b7667de8-a912-436c-9ab5-5641f2a9c51d": "84 - Vaucluse",
                        "http://id.insee.fr/geo/departement/0a4c2b68-2dee-4a1f-8498-5a295ad79631": "85 - Vendée",
                        "http://id.insee.fr/geo/departement/387f5118-fdb2-4607-afc6-1a9a5160b56d": "86 - Vienne",
                        "http://id.insee.fr/geo/departement/df1f6ac1-b480-43ac-bc88-b41427b4081c": "87 - Haute-Vienne",
                        "http://id.insee.fr/geo/departement/381511e9-8343-4a5c-9723-5b86da35fb9f": "88 - Vosges",
                        "http://id.insee.fr/geo/departement/f2366472-58ea-440b-87a8-24cb44676af1": "89 - Yonne",
                        "http://id.insee.fr/geo/departement/3df7b77b-cbfd-4152-b8e9-1c0f4f2d34a4": "90 - Territoire de Belfort",
                        "http://id.insee.fr/geo/departement/4fa83910-71e4-412f-83dc-d143647e36d4": "91 - Essonne",
                        "http://id.insee.fr/geo/departement/653b03ce-3103-4efb-ad89-3f961d986be6": "92 - Hauts-de-Seine",
                        "http://id.insee.fr/geo/departement/42e5b3f2-6d71-4b7a-84d8-05275eaeb0ce": "93 - Seine-Saint-Denis",
                        "http://id.insee.fr/geo/departement/6fe1d0ad-65ba-480d-9cc8-1eb76f9f178d": "94 - Val-de-Marne",
                        "http://id.insee.fr/geo/departement/d32e14f8-e8b7-4dbd-a6af-d1ac33f4e51e": "95 - Val-d'Oise",
                        "http://id.insee.fr/geo/departement/d423d69b-3557-41f6-9469-9ed0f3db412a": "972 - Martinique",
                        "http://id.insee.fr/geo/departement/bddb7eb1-e8db-4b01-818f-967057b8bbea": "971 - Guadeloupe",
                        "http://id.insee.fr/geo/departement/a540250f-42d9-496a-9078-cabe94025e85": "973 - Guyane",
                        "http://id.insee.fr/geo/departement/9ead25bc-0ba7-49d8-a997-da17f87074db": "974 - La Réunion",
                        "http://id.insee.fr/geo/departement/7f7fe4af-ae1c-4641-80ef-5c8199aea45c": "976 - Mayotte",
                        "http://id.insee.fr/geo/departement/9de761ab-a07a-4ba9-934d-6f753129b924": "2A - Corse du sud",
                        "http://id.insee.fr/geo/departement/cff23136-dbda-4870-905c-58942c3bc9be": "2B - Haute-Corse",
                        "http://id.insee.fr/geo/france/FM": "France Métropolitaine",
                        "http://id.insee.fr/geo/france/F": "France",
                        }

                        df["Département"] = df["Département"].replace(departementss_mapping)

                        #Afficher Dataframe : 
                        st.dataframe(df, width=1100)

                        st.markdown("""
                        <style>
                        .st.dataframe {
                            margin-: 80px;
                        }
                        </style>            
                                        
                        """, unsafe_allow_html=True)

                    else:
                        st.write("Les données attendues ne sont pas disponibles dans la réponse.")
                else:
                    st.write(f"Erreur : {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.write("Erreur lors de l'appel à l'API :", e)
        