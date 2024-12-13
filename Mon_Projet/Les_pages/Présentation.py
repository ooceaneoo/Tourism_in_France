import streamlit as st

#Fonction de la page "Présentation" de mon menu : 
def render_presentation():
    #Style CSS pour mon slider/cadre:
    st.markdown("""
        <style> 
        .slider-container {
            position: relative;
            width: 100%;
            max-width: 700px;
            margin: auto;
            margin-top: -750px;
            margin-left: 700px;
        }
        .slider-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            min-height: 700px;
            border: 1px solid black; /* Contour noir fin */
        }
        </style>
    """, unsafe_allow_html=True)

    #Insérer une image (url, taille, position):
    st.markdown("""
        <div style='margin-top: -20px;'>
            <img src="https://image.noelshack.com/fichiers/2024/47/5/1732245392-design-sans-titre-3.png" 
                width="600" alt="Image de présentation">
        </div>
    """, unsafe_allow_html=True)

    # Création de mon slider
    slides = [
    #Slide 1 :
    """
    <style>
        li {
            font-family: 'Roboto', sans-serif;
            font-weight: 300;
        }
    </style>
    <br>
    <h4 style="color: black; text-align: center;">BIENVENUE SUR NOTRE DASHBOARD</h4>
    <br>
    <p style="text-align: center;">Ce tableau de bord interactif est conçu pour explorer les tendances de fréquentation touristique en France à travers plusieurs types de mesures.</p>
    <p style="text-align: center;">Ces données vous permettront de comprendre les flux touristiques et d'identifier les tendances de fréquentation.</p>
    <br>
    <h4 style="text-align: center;">Qu'allez-vous découvrir précisément ?</h4>
    <ul style="text-align: left; margin-left: 50px;"> 
        <li>Le volume de nuitées et d’arrivées dans les hébergements touristiques, à différents niveaux géographiques.</li>
        <li>Les durées moyennes de séjour, pour comprendre les préférences des touristes.</li>
        <li>Les périodes de forte et faible activité touristique.</li>
        <li>L'évolution dans le temps de plusieurs indicateurs.</li>
    </ul>
    """,
    #Slide 2 :
    """
    <h3 style="color: black; text-align: center;">PRÉSENTÉ PAR :</h3>
    <h4 style="text-align: center;">Camille & Océane</h4>
    """
]

    #Gestion de l'état du slide actuel : 
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    #Affichage du slide actuel :
    st.markdown(
        f"""
        <div class='slider-container'>
            <div class='slider-content'>{slides[st.session_state.current_slide]}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    #Bouton pour passer au slide suivant :
    if st.button(""):
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)

    #Apparence de mon bouton :
    st.markdown("""
        <style>
            .slider-container {
                text-align: center;
            }

            .slider-content {
                background-color: #FBFCFA;
                padding: 40px;
                border-radius: 10px;
                border: none;
                font-family: 'Roboto', sans-serif; 
                font-size: 18px;  
                color: #333;
                font-weight: 300;
            }

            .stButton > button {
                background-image: url('https://us.123rf.com/450wm/cowpland/cowpland1501/cowpland150100073/35161869-fl%C3%A8che-vers-la-droite-l-ic%C3%B4ne-plat-moderne.jpg'); 
                background-size: contain;
                background-repeat: no-repeat;
                padding: 0;
                border: none;
                width: 100px;
                height: 100px;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease;

                position: absolute;
                margin-top: -455px;
                margin-left: 1450px;
                transform: translateX(-50%);
                text-align: center;
            }

            .stButton > button:hover {
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

    