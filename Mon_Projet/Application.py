import streamlit as st
from streamlit_option_menu import option_menu

#Import des fichiers des différentes pages du menu :
from Les_pages.Présentation import render_presentation
from Les_pages.Tendances import render_tendances
from Les_pages.Comparaison import render_comparaison
from Les_pages.Visualisation import render_visualisation
from Les_pages.Données import render_donnees

#Configuration de la page pour maximiser l'espace :
st.set_page_config(layout="wide")

#Cacher les éléments du haut (streamlit) :
st.markdown("""
    <style>
        header {visibility: hidden;}
        .streamlit-footer {display: none;}
    </style>
""", unsafe_allow_html=True)

#Ajout du titre :
st.markdown("""
    <style>
        .custom-title {
            position: absolute;
            top: -70px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 45px;
            color: #333;
            letter-spacing: 2px;
            text-transform: uppercase;
            z-index: 1000;
            font-family: 'Didot';
            font-weight: 300;              
        }
    </style>
    <div class="custom-title">
        FRÉQUENTATIONS TOURISTIQUES
    </div>
""", unsafe_allow_html=True)

#Création du menu horizontal
selected = option_menu(
    menu_title=None,
    options=["PRÉSENTATION", "VISUALISATION DU TOURISME", "COMPARAISON INTER-RÉGIONS", "TENDANCES", "DONNÉES"],
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important", #Pas de padding autour du conteneur (padding = espace interne)
            "background-color": "#eeeee4", #Couleur menu
            "height": "90px", #Hauteur du menu
            "max-width": "100vw", #Utiliser la largeur de l'écran
            "white-space": "nowrap", #Ne pas autoriser les sauts de ligne
            "margin-top": "3px",  #Hauteur position (espace par rapport au haut)
            "border-radius": "100px", #Arrondir les bords
            "flex-wrap": "nowrap",  #Empêcher les éléments de se casser sur plusieurs lignes
            "margin": "0",  #Pas de marge autour du conteneur
        },

        "nav-link": {
            "font-size": "18px", #Ajuster taille texte
            "color": "black", #Couleur texte
            "text-align": "center", #Centrer
            "padding": "30px 30px",  #Centrer l'écriture au milieu de chaque bouton du menu
            "--hover-color": "#eeeee4",  #Couleur de survol
            "border-radius": "100px",  #Arrondir les bords
        },

        "nav-link-selected": {
            "background-color": "#fafafa", 
            "color": "black",
            "border-radius": "100px",
        },

        "icon": {
            "display": "none"  # Enlever les icônes des menus
        },
    },
)


#Police d'écriture
st.markdown("""
    <style>
        p {
            font-family: 'Roboto', sans-serif;
            font-weight: 300;
            font-size: 18px;  
            color: #333;
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


#Navigation entre les pages :
if selected == "PRÉSENTATION":
    render_presentation()
elif selected == "TENDANCES":
    render_tendances()
elif selected == "COMPARAISON INTER-RÉGIONS":
    render_comparaison()
elif selected == "VISUALISATION DU TOURISME":
    render_visualisation()
elif selected == "DONNÉES":
    render_donnees()


#Barre cookies :
import streamlit as st
import streamlit.components.v1 as components

def afficher_barre_cookies():
    #Vérifie si l'utilisateur a déjà accepté ou refusé les cookies :
    if st.session_state.get("cookies_accepted") is None:
        #Apparence de la barre cookies :
        cookie_bar_html = """
        <style>
            .cookie-banner {
                position: fixed;
                top: 0; 
                left: 0;
                width: 100%;
                background-color: #ffffff;
                color: #000000;
                text-align: center;
                padding: 15px;
                font-family: 'Roboto', sans-serif;
                font-weight: 300;
                font-size: 18px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
            }
            .cookie-banner button {
                background-color: #F7BD5F;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 0 10px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Roboto', sans-serif;
                font-weight: 300;
                font-size: 14px;
            }
            .cookie-banner button:hover {
                background-color: #d90429;
            }
            .cookie-banner a {
                color: #007bff;
                text-decoration: none;
            }
            .cookie-banner a:hover {
                text-decoration: underline;
            }
        </style>

        <div class="cookie-banner" id="cookie-banner">
            <span>Nous utilisons des cookies pour améliorer votre expérience. Consultez notre <a href="#">politique de confidentialité</a>.</span>
            <button onclick="acceptCookies()">Accepter</button>
            <button onclick="refuseCookies()">Refuser</button>
        </div>
        <script>
            function acceptCookies() {
                const cookieBanner = document.getElementById('cookie-banner');
                cookieBanner.style.display = 'none';
                Streamlit.setComponentValue("accept");
            }
            function refuseCookies() {
                const cookieBanner = document.getElementById('cookie-banner');
                cookieBanner.style.display = 'none';
                Streamlit.setComponentValue("refuse");
            }
        </script>
        """

        action = components.html(cookie_bar_html, height=100)

        #Enregistre l'état dans la session Streamlit :
        if action == "accept":
            st.session_state["cookies_accepted"] = True
        elif action == "refuse":
            st.session_state["cookies_accepted"] = False

def main():
    afficher_barre_cookies()

if selected == "PRÉSENTATION":
    main()