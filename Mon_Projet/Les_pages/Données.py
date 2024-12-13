import streamlit as st

def render_donnees():

        #Style personnalisé :
        st.markdown("""
        <style>
        .content-box {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .content-title {
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .content-body {
            font-size: 16px;
            line-height: 1.6;
            color: #34495e;
        }
        </style>
        """, unsafe_allow_html=True)

        #Introduction générale :
        st.markdown("""
        <div class="content-box">
            <div class="content-title">Mesure du Tourisme</div>
            <div class="content-body">
                La variable <strong>Mesure du Tourisme</strong> regroupe différents indicateurs clés pour évaluer l'importance et les
                tendances du tourisme dans une région. Ces indicateurs permettent d'analyser la fréquentation, les durées de séjour,
                les capacités d'accueil et le taux d'occupation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 1 : Nombre d’arrivées
        st.markdown("""
        <div class="content-box">
            <div class="content-title">1. Nombre d’arrivées</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Indique le nombre total de touristes arrivant dans une région ou un hébergement donné.<br><br>
                <strong>Caractéristiques :</strong><br>
                Permet de suivre l'attractivité d'une destination sur une période donnée.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 2 : Nombre de jours du séjour
        st.markdown("""
        <div class="content-box">
            <div class="content-title">2. Nombre de jours du séjour</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Indique la durée des séjours des touristes dans une région ou un type d’hébergement.<br><br>
                <strong>Caractéristiques :</strong><br>
                Utilisé pour analyser les comportements touristiques, comme les séjours courts pour les affaires ou longs pour les vacances.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 3 : Part des nuitées provenant de touristes étrangers (%)
        st.markdown("""
        <div class="content-box">
            <div class="content-title">3. Part des nuitées provenant de touristes étrangers (%)</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Indique la proportion des nuitées réalisées par des touristes étrangers, exprimée en pourcentage.<br><br>
                <strong>Caractéristiques :</strong><br>
                Permet d'identifier l'attractivité internationale d'une région ou d'une infrastructure touristique.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 4 : Nombre de nuitées
        st.markdown("""
        <div class="content-box">
            <div class="content-title">4. Nombre de nuitées</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Total des nuitées passées par les touristes dans une région ou un hébergement.<br><br>
                <strong>Caractéristiques :</strong><br>
                Utilisé pour évaluer l'occupation réelle et la durée des séjours cumulés.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 5 : Nombre de places offertes
        st.markdown("""
        <div class="content-box">
            <div class="content-title">5. Nombre de places offertes</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Nombre total de places disponibles dans les hébergements touristiques (hôtels, campings, etc.).<br><br>
                <strong>Caractéristiques :</strong><br>
                Permet d'évaluer la capacité maximale d'accueil d'une infrastructure touristique.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 6 : Taux d’occupation des places (%)
        st.markdown("""
        <div class="content-box">
            <div class="content-title">6. Taux d’occupation des places (%)</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Indicateur exprimant le pourcentage des places réellement occupées par rapport au nombre total de places offertes.<br><br>
                <strong>Caractéristiques :</strong><br>
                Utilisé pour évaluer l’efficacité ou la popularité d’un hébergement.
            </div>
        </div>
        """, unsafe_allow_html=True)

        #Sous-catégorie 7 : Nombre de places occupées
        st.markdown("""
        <div class="content-box">
            <div class="content-title">7. Nombre de places occupées</div>
            <div class="content-body">
                <strong>Description :</strong><br>
                Indique le nombre total de places réellement occupées dans les hébergements touristiques.<br><br>
                <strong>Caractéristiques :</strong><br>
                Sert à mesurer la fréquentation réelle d'une infrastructure.
            </div>
        </div>
        """, unsafe_allow_html=True)