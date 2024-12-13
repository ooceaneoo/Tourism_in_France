import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px


def render_tendances():
    #Liste des indicateurs à comparer :
    indicators = [
        "Nombre d'arrivées", 
        "Nombre de jours du séjour", 
        "Part des nuitées provenant de touristes étrangers (%)", 
        "Nombre de nuitées", 
        "Taux d'occupation des places (%)"
    ]
    
    #Disposition des colonnes : cadre à gauche, contenu à droite :
    col2, col1 = st.columns([3, 1])  #Largeur relative : col1 est plus petite que col2

    #Cadre contenant les options sous forme de radio boutons :
    with col1:
        selected_option = st.radio(
            "Choisissez un indicateur :",  # Texte de l'étiquette
            indicators,                   # Liste des indicateurs
            index=0,                      # Option sélectionnée par défaut
            key="indicators_radio"        # Clé unique pour ce widget
        )
        
    #Styles personnalisés :
    st.markdown("""
        <style>
        [data-testid="stRadio"] > label {
            display: block;                /* Afficher chaque option sur une ligne */
            font-size: 16px;               /* Taille de la police */
            margin-bottom: 10px;           /* Espacement entre les options */
        }
        </style>
    """, unsafe_allow_html=True)


    #Contenu affiché en fonction du bouton sélectionné :
    with col2:

        if selected_option:

            if selected_option == "Nombre d'arrivées":   

                                #-------------------------- API POUR GRAPHIQUE 1 --------------------------#             
                API_URL = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000&FREQ=A&TOUR_MEASURE=ARR&GEO=FRANCE&TOUR_RESID=_T&UNIT_LOC_RANKING=_T&TERRTYPO=_T&HOTEL_STA=_T"
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré :
                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            #Traduire la valeur de TOUR_RESID si présente :
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne :
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                        #Création d'un DataFrame pandas :
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes :
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles :
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Mapping des départements :
                        departementss_mapping = {
                        "http://id.insee.fr/geo/france/FM": "France Métropolitaine",
                        "http://id.insee.fr/geo/france/F": "France",
                        }

                        #Appliquer le mapping des départements :
                        df["Département"] = df["Département"].map(departementss_mapping)
                        

                        #Liste des colonnes à supprimer :
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes :
                        df.drop(columns=colonnes_a_supprimer, inplace=True)
                                                
                        #Filtrer pour ne garder que les données du département "France" :
                        df_france = df[df['Département'] == 'France']

                        #Trier les données par la colonne 'Période' (Année) dans l'ordre croissant :
                        df_france = df_france.sort_values(by='Période', ascending=True)

                        # Création du graphique linéaire :
                        fig = px.line(df_france, 
                                    x='Période', 
                                    y='Valeur',
                                    labels={'Période': '', 'Valeur': ''},
                                    title="ÉVOLUTION DU NOMBRE D'ARRIVÉES DANS LES HÉBERGEMENTS ET HOTELS EN FRANCE")

                        #Personnalisation de l'apparence du graphique : 
                        fig.update_layout(title={
                            'text': "ÉVOLUTION DU NOMBRE D'ARRIVÉES DANS LES HÉBERGEMENTS ET HOTELS EN FRANCE",  #Titre du graphique
                            'x': 0.5,  # Centrer le titre
                            'xanchor': 'center',  # Ancrer le titre au centre
                            'yanchor': 'top',  # Ancrer le titre en haut
                            'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  #Style du titre
                        })

                        #Personnalisation de la ligne du graphique :
                        fig.update_traces(line=dict(color='black', width=3))  #Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille :
                        fig.update_layout(
                            plot_bgcolor="#FBFCFA",  # Couleur de fond du graphique
                            paper_bgcolor="#FBFCFA",  # Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit :
                        st.plotly_chart(fig)
                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")
            
                #-------------------------- API POUR GRAPHIQUE 2 --------------------------#
                API_URL2 = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000&FREQ=A&TOUR_MEASURE=ARR&GEO=DEP&TOUR_RESID=_T"
                response = requests.get(API_URL2, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                        #Création d'un DataFrame pandas :
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes :
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles :
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Dictionnaire départements : 
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

                        #Appliquer le mapping des départements :
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Liste des colonnes à supprimer :
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes :
                        df.drop(columns=colonnes_a_supprimer, inplace=True)

                        #Liste unique des départements :
                        departements_uniques = df["Département"].dropna().unique()

                        #Ajout de la selectbox pour choisir un département :
                        departement_selectionne = st.selectbox(
                            "Sélectionnez un département :",
                            options=list(departements_uniques),
                            index=0  # Par défaut, afficher "Tous"
                        )

                        #Filtrer les données en fonction de la sélection et trier par période :
                        df_filtre = df[df["Département"] == departement_selectionne].sort_values("Période").reset_index(drop=True)

                        #Générer le graphique :
                        fig = px.line(
                                df_filtre,
                                x="Période",
                                y="Valeur",
                                labels={"Période": "Année", "Valeur": ""},
                                title=f"Évolution du nombre d'arrivées - {departement_selectionne}"
                        )

                        #Connecter les points manquants (en remplissant les trous) :
                        fig.update_traces(connectgaps=True)

                        #Personnalisation du graphique :
                        fig.update_layout(title={
                                'text': "ÉVOLUTION DU NOMBRE D'ARRIVÉES",  #Titre du graphique
                                'x': 0.5,  #Centrer le titre
                                'xanchor': 'center',  #Ancrer le titre au centre
                                'yanchor': 'top',  #Ancrer le titre en haut
                                'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  #Style du titre
                        })

                        #Personnalisation de la ligne du graphique :
                        fig.update_traces(line=dict(color='black', width=3))  #Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille
                        fig.update_layout(
                                plot_bgcolor="#FBFCFA",  #Couleur de fond du graphique
                                paper_bgcolor="#FBFCFA",  #Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit
                        st.plotly_chart(fig)

                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")
            
            
            if selected_option == "Nombre de jours du séjour":

                #-------------------------- API POUR GRAPHIQUE 1 --------------------------#
                API_URL = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=200&TOUR_MEASURE=DAYS_STAY&UNIT_LOC_RANKING=_T&TERRTYPO=_T&HOTEL_STA=_T&ACTIVITY=I551&FREQ=A&TOUR_RESID=_T&TIME_PERIOD=2023&GEO=DEP"
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré :
                        rows = [
                            {
                            "Département": obs["dimensions"].get("GEO", ""),
                            "Valeur": obs["measures"]["OBS_VALUE_NIVEAU"]["value"]
                            }
                        for obs in data["observations"]
                        if "measures" in obs and "OBS_VALUE_NIVEAU" in obs["measures"]
                        ]
                        
                        #Création d'un DataFrame pandas :
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes :
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Mapping des départements :
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

                        #Appliquer le mapping des départements :
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Filtrer les colonnes nécessaires :
                        df = df[["Département", "Valeur"]]

                        #Création du graphique interactif avec Plotly :
                        fig = px.bar(
                            df,
                            x="Département",
                            y="Valeur",
                            title="NOMBRE DE JOURS DE SÉJOUR PAR DÉPARTEMENT",
                            labels={"Valeur": "Nombre de jours", "Département": "Département"},
                            color="Département",
                            color_continuous_scale="Viridis"
                        )

                        #Titre du graphique :
                        fig.update_layout(title={
                            'text': "NOMBRE MOYEN DE JOURS DE SÉJOUR PAR DÉPARTEMENT",  # Titre du graphique
                            'x': 0.5,  # Centrer le titre
                            'xanchor': 'center',  # Ancrer le titre au centre
                            'yanchor': 'top',  # Ancrer le titre en haut
                            'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  # Style du titre
                        })

                        max_valeur = df["Valeur"].max()


                        #Créer une carte pour afficher la moyenne :
                        st.markdown(
                            f"""
                            <div style="
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                flex-direction: column;
                                background-color: #FBFCFA;
                                padding: 30px;
                                width: 500px;
                                margin-left: 20px;
                                transition: transform 0.2s;
                            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1.0)'">
                                <h3 style="color: black; margin: 0; font-size: 18px; font-family: 'Arial', sans-serif;">Séjour le + long (en moyenne)</h3>
                                <p style="font-size: 36px; color: black; margin: 10px 0;">
                                    {max_valeur:.2f}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        #Afficher le graphique dans Streamlit :
                        st.plotly_chart(fig)

                        #Calculer la valeur maximale par département :
                        df_max_par_dept = df.groupby('Département')['Valeur'].max().reset_index()

                        #Trier par valeur décroissante :
                        df_sorted = df_max_par_dept.sort_values(by='Valeur', ascending=False)

                        #Sélectionner les 3 premiers départements :
                        top_3_departments = df_sorted.head(3)

                        #Afficher les résultats (exemple avec un graphique à barres) :
                        fig = px.bar(top_3_departments, x='Département', y='Valeur', title="TOP 3 DES DÉPARTEMENTS AVEC LE SÉJOUR MOYEN LE + LONG")
                        st.plotly_chart(fig)
                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")

                

            if selected_option == "Part des nuitées provenant de touristes étrangers (%)":

                #-------------------------- API POUR GRAPHIQUE 1 --------------------------#
                API_URL = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000&FREQ=A&TOUR_MEASURE=NON_RESIDENT_NIGHTSPENT_RATIO&GEO=FRANCE&UNIT_LOC_RANKING=_T&TERRTYPO=_T&HOTEL_STA=_T"
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré
                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            #Traduire la valeur de TOUR_RESID si présente
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                        #Création d'un DataFrame pandas
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Mapping des départements
                        departementss_mapping = {
                        "http://id.insee.fr/geo/france/FM": "France Métropolitaine",
                        "http://id.insee.fr/geo/france/F": "France",
                        }

                        #Appliquer le mapping des départements
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Liste des colonnes à supprimer
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes
                        df.drop(columns=colonnes_a_supprimer, inplace=True)


                        #Filtrer pour ne garder que les données du département "France"
                        df_france = df[df['Département'] == 'France']

                        #Trier les données par la colonne 'Période' (Année) dans l'ordre croissant
                        df_france = df_france.sort_values(by='Période', ascending=True)

                        #Création du graphique linéaire
                        fig = px.line(df_france, 
                                    x='Période', 
                                    y='Valeur',
                                    labels={'Période': '', 'Valeur': ''},
                                    title="ÉVOLUTION DE LA PART DES NUITÉES PROVENANT DE TOURISTES ÉTRANGERSEN FRANCE (%)")
                        
                        #Connecter les points manquants (en remplissant les trous)
                        fig.update_traces(connectgaps=True)


                        #Personnalisation de l'apparence du graphique :
                        fig.update_layout(title={
                            'text': "ÉVOLUTION DE LA PART DES NUITÉES PROVENANT DE TOURISTES ÉTRANGERS EN FRANCE (%)",  # Titre du graphique
                            'x': 0.5,  # Centrer le titre
                            'xanchor': 'center',  # Ancrer le titre au centre
                            'yanchor': 'top',  # Ancrer le titre en haut
                            'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  # Style du titre
                        })

                        #Personnalisation de la ligne du graphique :
                        fig.update_traces(line=dict(color='black', width=3))  # Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille :
                        fig.update_layout(
                            plot_bgcolor="#FBFCFA",  # Couleur de fond du graphique
                            paper_bgcolor="#FBFCFA",  # Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit :
                        st.plotly_chart(fig)

                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")
                
                #-------------------------- API POUR GRAPHIQUE 2 --------------------------#
                API_URL2 = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000&FREQ=A&TOUR_MEASURE=NON_RESIDENT_NIGHTSPENT_RATIO&GEO=DEP&UNIT_LOC_RANKING=_T&TERRTYPO=_T&HOTEL_STA=_T"
                response = requests.get(API_URL2, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré
                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            #Traduire la valeur de TOUR_RESID si présente
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                        #Création d'un DataFrame pandas
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Dictionnaire départements : 
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

                        #Appliquer le mapping des départements
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Liste des colonnes à supprimer
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes
                        df.drop(columns=colonnes_a_supprimer, inplace=True)

                        #Liste unique des départements
                        departements_uniques = df["Département"].dropna().unique()

                        #Calcul de la part des nuitées provenant de touristes étrangers pour chaque département
                        df['Valeur'] = df['Valeur'].astype(float)

                        #Calcul de la part moyenne par département 
                        df_moyenne_par_departement = df.groupby("Département")["Valeur"].mean().reset_index()

                        #Trier les départements par la part moyenne de nuitées étrangères (en ordre décroissant)
                        df_moyenne_par_departement = df_moyenne_par_departement.sort_values(by="Valeur", ascending=False)

                        #Sélectionner les départements les plus élevés pour un graphique
                        top_departements = df_moyenne_par_departement.head(10)  # Afficher les 10 premiers départements

                        #Création d'un graphique :
                        fig = px.bar(
                            top_departements,
                            x="Département",
                            y="Valeur",
                            labels={"Département": "Nom du Département", "Valeur": "Part des Nuitées Étrangères (%)"},
                            title="Les 10 départements avec la plus grande part de nuitées provenant de touristes étrangers"
                        )

                        #Personnalisation du graphique
                        fig.update_layout(
                            title={'text': "Top 10 des départements avec la plus grande part de touristes étrangers", 'x': 0.5, 'xanchor': 'center'},
                            plot_bgcolor="#FBFCFA", 
                            paper_bgcolor="#FBFCFA"
                        )

                        #Affichage du graphique
                        st.plotly_chart(fig)

                        #Ajout de la selectbox pour choisir un département
                        departement_selectionne = st.selectbox(
                            "Sélectionnez un département :",
                            options=list(departements_uniques),
                            index=0  # Par défaut, afficher "Tous"
                        )

                        #Filtrer les données en fonction de la sélection et trier par période
                        df_filtre = df[df["Département"] == departement_selectionne].sort_values("Période").reset_index(drop=True)

                        #Générer le graphique
                        fig = px.line(
                                df_filtre,
                                x="Période",
                                y="Valeur",
                                labels={"Période": "Année", "Valeur": ""},
                                title=f"Évolution du nombre d'arrivées - {departement_selectionne}"
                        )

                        #Connecter les points manquants (en remplissant les trous)
                        fig.update_traces(connectgaps=True)

                        #Titre du graphique
                        fig.update_layout(title={
                                'text': "ÉVOLUTION DE LA PART DE TOURISTES ÉTRANGERS (%)",  # Titre du graphique
                                'x': 0.5,  # Centrer le titre
                                'xanchor': 'center',  # Ancrer le titre au centre
                                'yanchor': 'top',  # Ancrer le titre en haut
                                'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  # Style du titre
                        })

                        #Personnalisation de la ligne du graphique
                        fig.update_traces(line=dict(color='black', width=3))  # Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille
                        fig.update_layout(
                                plot_bgcolor="#FBFCFA",  # Couleur de fond du graphique
                                paper_bgcolor="#FBFCFA",  # Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit
                        st.plotly_chart(fig)

                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")





            if selected_option == "Nombre de nuitées":
                
                #-------------------------- API POUR GRAPHIQUE 1 --------------------------#
                API_URL = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=200&FREQ=A&ACTIVITY=I551&TOUR_RESID=_T&HOTEL_STA=_T&TERRTYPO=_T&TOUR_MEASURE=NUI&UNIT_LOC_RANKING=_T&GEO=FRANCE"
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré
                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            #Traduire la valeur de TOUR_RESID si présente
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                        #Création d'un DataFrame pandas
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Mapping des départements
                        departementss_mapping = {
                        "http://id.insee.fr/geo/france/FM": "France Métropolitaine",
                        "http://id.insee.fr/geo/france/F": "France",
                        }

                        #Appliquer le mapping des départements
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Liste des colonnes à supprimer
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes
                        df.drop(columns=colonnes_a_supprimer, inplace=True)


                        #Filtrer pour ne garder que les données du département "France"
                        df_france = df[df['Département'] == 'France']

                        #Trier les données par la colonne 'Période' (Année) dans l'ordre croissant
                        df_france = df_france.sort_values(by='Période', ascending=True)

                        #Création du graphique linéaire
                        fig = px.line(df_france, 
                                    x='Période', 
                                    y='Valeur',
                                    labels={'Période': '', 'Valeur': ''},
                                    title="ÉVOLUTION DU NOMBRE DE NUITÉES EN FRANCE")

                        #Personnalisation de l'apparence

                        #Titre du graphique
                        fig.update_layout(title={
                            'text': "ÉVOLUTION DU NOMBRE DE NUITÉES EN FRANCE",  # Titre du graphique
                            'x': 0.5,  # Centrer le titre
                            'xanchor': 'center',  # Ancrer le titre au centre
                            'yanchor': 'top',  # Ancrer le titre en haut
                            'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  # Style du titre
                        })

                        #Personnalisation de la ligne du graphique
                        fig.update_traces(line=dict(color='black', width=3))  # Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille
                        fig.update_layout(
                            plot_bgcolor="#FBFCFA",  # Couleur de fond du graphique
                            paper_bgcolor="#FBFCFA",  # Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit
                        st.plotly_chart(fig)

                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")
     
            if selected_option == "Taux d'occupation des places (%)":

                #-------------------------- API POUR GRAPHIQUE 1 --------------------------#
                API_URL = "https://api.insee.fr/melodi/data/DS_TOUR_FREQ?maxResult=100000&TOUR_MEASURE=PLACE_OCCUPANCY_RATE&GEO=FRANCE&UNIT_LOC_RANKING=_T&TERRTYPO=_T&HOTEL_STA=_T"
                response = requests.get(API_URL, headers={"Authorization": "Bearer VOTRE_CLE_API"})

                if response.status_code == 200:
                    data = response.json()
                    if "observations" in data:
                        observations = data["observations"]

                        #Transformation des observations en tableau structuré
                        rows = []
                        for obs in observations:
                            row = {**obs["dimensions"], **obs["attributes"]}

                            #Traduire la valeur de TOUR_RESID si présente
                            if "TOUR_RESID" in row:
                                row["TOUR_RESID"] = row.get("TOUR_RESID", row["TOUR_RESID"])

                            #Ajouter chaque mesure comme colonne
                            if "measures" in obs:
                                for measure_name, measure_data in obs["measures"].items():
                                    row[measure_name] = measure_data.get("value", None)
                            rows.append(row)

                         #Création d'un DataFrame pandas
                        df = pd.DataFrame(rows)

                        #Renommer les colonnes
                        rename_columns = {
                            "OBS_VALUE_NIVEAU": "Valeur",
                            "TIME_PERIOD": "Période",
                            "GEO": "Département",
                        }
                        df = df.rename(columns=rename_columns)

                        #Supprimer les colonnes inutiles
                        df = df.drop(columns=["DECIMALS", "UNIT_MULT", "CONF_STATUS", "OBS_STATUS", "OBS_STATUS_FR", "HOTEL_STA"])

                        #Mapping des départements
                        departementss_mapping = {
                            "http://id.insee.fr/geo/france/FM": "France Métropolitaine",
                            "http://id.insee.fr/geo/france/F": "France",
                        }

                        #Appliquer le mapping des départements
                        df["Département"] = df["Département"].map(departementss_mapping)

                        #Liste des colonnes à supprimer
                        colonnes_a_supprimer = ["TOUR_MEASURE", "TERRTYPO", "ACTIVITY", "TOUR_RESID", "UNIT_LOC_RANKING", "FREQ"]

                        #Suppression des colonnes
                        df.drop(columns=colonnes_a_supprimer, inplace=True)

                        #Filtrer pour ne garder que les données du département "France"
                        df_france = df[df['Département'] == 'France']

                        #Convertir la colonne 'Période' en datetime et extraire l'année et le mois
                        df_france['Période'] = pd.to_datetime(df_france['Période'], format='%Y-%m', errors='coerce')
                        df_france['Année'] = df_france['Période'].dt.year
                        df_france['Mois'] = df_france['Période'].dt.month

                        #Filtrer pour ne garder que les données du mois de janvier (Mois = 1)
                        df_france_janvier = df_france[df_france['Mois'] == 1]

                        #Trier les données par la colonne 'Période' (Année) dans l'ordre croissant
                        df_france_janvier = df_france_janvier.sort_values(by='Année', ascending=True)

                        #Création du graphique linéaire
                        fig = px.line(df_france_janvier, 
                                    x='Année', 
                                    y='Valeur',
                                    labels={'Période': '', 'Valeur': '', 'Année': ''},
                                    title="ÉVOLUTION DU TAUX D'OCCUPATION DES PLACES EN FRANCE")
                        
                        #Connecter les points manquants (en remplissant les trous)
                        fig.update_traces(connectgaps=True)

                        #Personnalisation de l'apparence

                        #Titre du graphique
                        fig.update_layout(title={
                            'text': "ÉVOLUTION DU TAUX D'OCCUPATION DES PLACES EN FRANCE",  # Titre du graphique
                            'x': 0.5,  # Centrer le titre
                            'xanchor': 'center',  # Ancrer le titre au centre
                            'yanchor': 'top',  # Ancrer le titre en haut
                            'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}  # Style du titre
                        })

                        #Personnalisation de la ligne du graphique
                        fig.update_traces(line=dict(color='black', width=3))  # Couleur et largeur de la ligne

                        #Personnalisation des couleurs de la grille
                        fig.update_layout(
                            plot_bgcolor="#FBFCFA",  # Couleur de fond du graphique
                            paper_bgcolor="#FBFCFA",  # Couleur de fond du graphique dans Streamlit
                        )

                        #Affichage du graphique sur Streamlit
                        st.plotly_chart(fig)

                        #Calculer la moyenne des valeurs pour chaque mois sur toutes les années
                        df_moyenne_mensuelle = df_france.groupby('Mois')['Valeur'].mean().reset_index()
                        # Nom des mois en français
                        mois_francais = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
                        df_moyenne_mensuelle['Mois_nom'] = df_moyenne_mensuelle['Mois'].apply(lambda x: mois_francais[x-1])

                        #Création du graphique pour les moyennes mensuelles
                        fig_moyenne_mensuelle = px.bar(df_moyenne_mensuelle,
                                                    x='Mois_nom',
                                                    y='Valeur',
                                                    labels={'Mois_nom': 'Mois', 'Valeur': 'Taux d\'Occupation Moyen (%)'},
                                                    title="Moyenne du taux d'occupation des places par mois en France")
                        fig_moyenne_mensuelle.update_layout(
                            xaxis=dict(tickmode='array', tickvals=mois_francais),
                            plot_bgcolor="#FBFCFA",
                            paper_bgcolor="#FBFCFA",
                            title={
                                'text': "Moyenne du Taux d'Occupation des Places par Mois",
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': {'size': 18, 'family': 'Roboto, sans-serif', 'color': 'black'}
                            }
                        )
                        st.plotly_chart(fig_moyenne_mensuelle)
                    else:
                        st.error("Aucune donnée disponible.")
                else:
                    st.error(f"Erreur de récupération des données : {response.status_code}")
        else:

            st.markdown("""
            <style> 
            .slider-container {
                position: relative;
                width: 100%;
                max-width: 1080px;
                margin: auto;
                margin-top: -15px;
            }
            .slider-content {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 18px;
                min-height: 380px;
                border: 1px solid black; /* Contour noir fin */
            }
            </style>
        """, unsafe_allow_html=True)
            
            st.markdown(
            f"""
            <div class='slider-container'>
                <div class='slider-content'>{"Bienvenue dans cette section."}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
            
        

            
