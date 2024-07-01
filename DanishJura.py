import streamlit as st
import openai
import Mekanism
import re
import logging
import os
import requests  # Add requests to check for internet connection
from PIL import Image
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to check for an internet connection
def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

# Function to find and extract summary lines from the answer
def findtxt(answer):
    logging.info(f"findtxt called with answer: {answer}")

    if answer:
        #summary_match = re.search(r'\*\*OPSUMMERING\*\*|\*\*Opsummering\*\*|\*\*opsummering\*\*', answer)
        #summary_match = re.search(r'\*OPSUMMERING\*|\*Opsummering\*|\*opsummering\*', answer)
        summary_match = re.search(r'\*OPSUMMERING\*|\*Opsummering\*|\*opsummering\*|\*FED Nøglepunkter\*', answer)
        summary_match = re.search(r'\*OPSUMMERING\*|\*Opsummering\*|\*opsummering\*|\*FED Nøglepunkter\*|\*FED Opsummering\*', answer)
        #summary_match = re.search(r'\*OPSUMMERING\*|\*Opsummering\*|\*opsummering\*|\*FED Nøglepunkter\*|\*FED Opsummering\*|Opsummering', answer)


        if summary_match:
            start_pos = summary_match.end()
            after_summary_text = answer[start_pos:].strip()

            key_points_match = re.search(r'\*\*Key Points:?\*\*', after_summary_text)
            if key_points_match:
                start_pos = key_points_match.end()
                after_summary_text = after_summary_text[start_pos:].strip()

            summary_lines = []
            for line in after_summary_text.split('\n'):
                line = line.strip()
                if line:
                    summary_lines.append(line)
                elif line == "":
                    break

            return summary_lines
        else:
            st.write("JEG FINDER IKKE RESUMÉ")
    else:
        st.write("INTET TEKST")

    return []

# Function to handle "Svar på spørgsmålet" button click
def answer_question():
    if not check_internet_connection():
        st.error("Ingen internetforbindelse!!! Opret venligst en forbindelse og opdater siden.")
        sys.exit()
        #return

    if 'api_key' not in st.session_state or not st.session_state['api_key']:
        st.session_state['wrong_key'] = True
        return

    openai.api_key = st.session_state['api_key']
    try:
        openai.Model.list()
    except openai.error.AuthenticationError:
        st.session_state['wrong_key'] = True
        return

    if st.session_state['question']:
        askjura_response = Mekanism.askjuradk(st.session_state['question'])
        detailed_answer = get_response(askjura_response)
        st.session_state['answer'] = detailed_answer

        summary_lines = findtxt(detailed_answer)
        st.session_state['summary_lines'] = summary_lines

        links_response = Mekanism.linksdk(st.session_state['question'])
        summary_answer = get_response(links_response)
        st.session_state['summary_points'] = summary_answer.split('\n')

# Function to clear the input box
def clear_input():
    st.session_state['question'] = ''
    st.session_state['answer'] = ''
    st.session_state['summary_points'] = []
    st.session_state['selected_summary'] = ''
    st.session_state['real_estate_law_selected'] = real_estate_laws[0]
    st.session_state['finance_law_selected'] = finance_laws[0]
    st.session_state['business_law_selected'] = business_laws[0]
    st.session_state['summary_lines'] = []
    st.session_state['wrong_key'] = False

# Function to set OpenAI API key
def set_api_key():
    openai.api_key = st.session_state['api_key']

# Function to get response from OpenAI
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jeg er en dansk advokat med over 35 års erfaring, der specialiserer sig i dansk finanslovgivning, erhvervsret, ejendomsret og bankret."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message['content'].strip()

# Function to handle summary link click
def handle_summary_click(point):
    st.session_state['selected_summary'] = point.split('. ', 1)[-1]  # Extract text after the first period and space
    st.session_state['question'] = st.session_state['selected_summary']
    st.experimental_rerun()

# Check internet connection on app start
if not check_internet_connection():
    st.error("Ingen internetforbindelse!!! Opret venligst en forbindelse og opdater siden.")
    st.stop()

# Set default OpenAI API key if not already set
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
if 'wrong_key' not in st.session_state:
    st.session_state['wrong_key'] = False

# Define the lists of laws
real_estate_laws = [
    "", "Ejerskab af ejendom", "Overdragelse af ejendom", "Jordregistrering (Tinglysning)", "Pantsætningslovgivning",
    "Lejelovgivning", "Ejendomsbeskatning", "Ejendomsudvikling", "Zonereguleringer",
    "Bygningsreguleringer", "Landbrugsejendomslovgivning", "Servitutter og brugsret", "Andelsboliglovgivning",
    "Andelshuslovgivning", "Ekspropriationslovgivning", "Miljøreguleringer", "Historisk bevarelse",
    "Tvangsauktion og tilbagekøb", "Arv af ejendom", "Kommerciel ejendomslovgivning", "Tvistbilæggelse i ejendomssager",
    "Ejendomsvurdering", "Planlægning af jordbrug", "Ejendomsfinansiering", "Husejerforeningslovgivning",
    "Ejendomsinvesteringsforeninger (REITs)", "Offentlig ejendomslovgivning", "Privat ejendomslovgivning", "Ejendomsforvaltningslovgivning",
    "Byfornyelseslovgivning", "Lejekontrol og regulering", "Ejendomssalg og erhvervelse", "Ejendomsmæglingslovgivning",
    "Ejendomsforsikringslovgivning", "Ejendomstvister og retssager", "Byggekontrakter", "Finansiering af ejendomsudvikling",
    "Ejendomsmæglingslovgivning", "Ejendomsvedligeholdelseslovgivning", "Forebyggelse af ejendomssvindel", "Udlejer-lejer-tvister",
    "Arkitektoniske reguleringer", "Byggeret", "Boligkooperativer", "Fælles ejerskab", "Private veje og stier",
    "Offentlig infrastrukturret", "Vedvarende energianlæg", "Turisme- og gæstfrihedsejendomslovgivning",
    "Vandfrontsejendomslovgivning", "Vildt- og naturbeskyttelsesområder"
]

finance_laws = [
    "", "Banklovgivning", "Værdipapirlovgivning", "Investeringslovgivning", "Finansiel regulering", "Forsikringslovgivning", "Pensionslovgivning",
    "Virksomhedsfinansieringslovgivning", "Kapitalmarkedslovgivning", "Lov om bekæmpelse af hvidvaskning af penge", "Finansiel kriminalitetslovgivning", "Betalingstjenestelovgivning",
    "Kreditlovgivning", "Forbrugerfinansieringslovgivning", "Finanstilsyn", "Lov om finansielle instrumenter", "Finansielle kontraktslovgivning",
    "Offentlig finanslovgivning", "Skattelovgivning", "Fusioner og opkøb", "Finansielle tjenestelovgivning", "Derivaterlovgivning", "Regnskabslovgivning",
    "Revisionslovgivning", "Konkurslovgivning", "Insolvenslovgivning", "Finansiel rapportering", "Risikostyringslovgivning", "Overholdelseslovgivning",
    "Hedgefondlovgivning", "Private equity lovgivning", "Formueforvaltningslovgivning", "Fondslovgivning", "Crowdfunding lovgivning", "Fintech lovgivning",
    "Mikrofinanslovgivning", "Ejendomsfinansieringslovgivning", "International finanslovgivning", "Elektroniske pengelovgivning", "Finansiel teknologilovgivning",
    "Finansiel stabilitetslovgivning", "Lov om grænseoverskridende finansiering", "Finansmarkedsregulering", "Lov om markedsmisbrug", "Lov om finansiel gennemsigtighed",
    "Formueforvaltningslovgivning", "Struktureret finansieringslovgivning", "Securitization lovgivning", "Venturekapitallovgivning", "Statsgældslovgivning",
    "International banklovgivning", "Valutalovgivning", "Lovgivning om virksomhedsledelse", "Lov om finansiel rådgivning",
    "Lov om kreditvurderingsbureauer", "Lov om forbrugerbeskyttelse", "Lovgivning om økonomiske sanktioner", "Handelsfinansieringslovgivning",
    "Projektfinansieringslovgivning", "Grøn finanslovgivning", "Bæredygtig finanslovgivning", "Basel III-overholdelse", "Solvens II-regulering",
    "Finansiel ombudsmand", "Digital banklovgivning", "Åben banklovgivning", "Kryptovalutalovgivning", "Blockchain finanslovgivning",
    "Robo-rådgivningslovgivning", "Finansiel inklusionslovgivning", "Lov om kreditforeninger", "Centralbankregulering", "Pengepolitisk lovgivning",
    "Lov om direkte udenlandske investeringer", "Økonomisk udviklingslovgivning", "Leasingfinansieringslovgivning", "Faktureringslovgivning", "Lov om handelskreditforsikring",
    "Finansiel ingeniørkunst", "Offentlig-privat partnerskabslovgivning", "Lov om eksportkreditter", "Pengefondslovgivning",
    "Ejendomsinvesteringslovgivning", "Private banklovgivning", "Lov om finansiel forståelse", "Skyggebanklovgivning", "Finansiel planlægning",
    "Lov om forrentning", "Pensionsopsparingslovgivning", "Aktuariel lovgivning", "Genforsikringslovgivning"
]

business_laws = [
    "", "Selskabslovgivning", "Kommercielle kontrakter", "Virksomhedsledelse", "Fusioner og opkøb", "Intellektuel ejendomsret",
    "Ansættelseslovgivning", "Konkurrencelovgivning", "Forbrugerbeskyttelseslovgivning", "Konkurs- og insolvenslovgivning", "Skattelovgivning",
    "International handelslovgivning", "Miljølovgivning", "Energilovgivning", "Ejendomslovgivning", "Finansiel regulering", "Værdipapirlovgivning",
    "Lov om bekæmpelse af hvidvaskning af penge", "Databeskyttelseslovgivning", "E-handelslovgivning", "Offentlig indkøbslovgivning", "Franchiselovgivning", "Agenturlovgivning",
    "Distributionslovgivning", "Partnerskabslovgivning", "Joint ventures", "Kommerciel tvistbilæggelse", "Voldgiftslovgivning", "Mæglinglovgivning",
    "Virksomhedsfinansieringslovgivning", "Private equity lovgivning", "Venturekapitallovgivning", "Investeringsfondslovgivning", "Forsikringslovgivning", "Pensionslovgivning",
    "Shipping lovgivning", "Luftfartslovgivning", "Transportlovgivning", "Medie- og underholdningslovgivning", "Telekommunikationslovgivning", "Sundhedslovgivning",
    "Farmaceutisk lovgivning", "Teknologilovgivning", "Byggeret", "Landbrugslovgivning", "Minedriftlovgivning", "Sportslovgivning", "Spillelovgivning",
    "Gæstfrihedslovgivning", "Turismelovgivning", "Offentlig ret", "Reguleringsmæssig overholdelse", "Virksomhedsomstrukturering", "Virksomheders sociale ansvar",
    "Antikorruptionslovgivning", "Eksportkontrol", "Toldlovgivning", "Handelsmæssig overholdelse", "Selskabskriminalitet", "Økonomisk kriminalitet",
    "Lovgivning om medarbejderfordele", "Arbejdsrelationer", "Sundheds- og sikkerhedslovgivning", "Reklamelovgivning", "Markedsføringslovgivning", "Forbrugerrettigheder",
    "Produktansvarslovgivning", "Forsyningskædelovgivning", "Outsourcing lovgivning", "IT-lovgivning", "Cybersecurity lovgivning", "Telekommunikationsregulering", "Internetlovgivning",
    "Cloud computing lovgivning", "Blockchain lovgivning", "Kryptovalutalovgivning", "Crowdfunding lovgivning", "Økonomiske sanktioner", "Udenlandske investeringer",
    "Sovereign Wealth Funds lovgivning", "Kommercielle leasinglovgivning", "Ejendomsleasing lovgivning", "Ejendomsinvesteringslovgivning", "Vedvarende energilovgivning",
    "Klimalovgivning", "Affaldshåndteringslovgivning", "Vandlovgivning", "Folkesundhedslovgivning", "Bioteknologilovgivning", "Life Sciences lovgivning",
    "Medicinsk udstyr lovgivning", "Uddannelseslovgivning", "Nonprofit lovgivning", "Velgørenhedsorganisationer", "Sociale virksomheder",
    "Familievirksomhedslovgivning", "Entreprenørskabslovgivning", "Opstartslovgivning", "Innovationslovgivning", "Lovgivning om forskning og udvikling", "Tilskuds- og støtteordninger",
    "Offentlig-privat partnerskabslovgivning", "Infrastrukturlovgivning"
]

# Initialize session state keys
if 'question' not in st.session_state:
    st.session_state['question'] = ''
if 'answer' not in st.session_state:
    st.session_state['answer'] = ''
if 'summary_points' not in st.session_state:
    st.session_state['summary_points'] = []
if 'selected_summary' not in st.session_state:
    st.session_state['selected_summary'] = ''
if 'real_estate_law_selected' not in st.session_state:
    st.session_state['real_estate_law_selected'] = real_estate_laws[0]
if 'finance_law_selected' not in st.session_state:
    st.session_state['finance_law_selected'] = finance_laws[0]
if 'business_law_selected' not in st.session_state:
    st.session_state['business_law_selected'] = business_laws[0]
if 'summary_lines' not in st.session_state:
    st.session_state['summary_lines'] = []
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
if 'wrong_key' not in st.session_state:
    st.session_state['wrong_key'] = False

# Function to update the question input box from list box selection
def update_question_from_real_estate():
    st.session_state['question'] = st.session_state['real_estate_law_selected']

def update_question_from_finance():
    st.session_state['question'] = st.session_state['finance_law_selected']

def update_question_from_business():
    st.session_state['question'] = st.session_state['business_law_selected']

# Load the logo image
logo_path = os.path.join(os.path.dirname(__file__), 'images', 'Screenshot_2024-06-04_232939-removebg-preview.png')
logo = Image.open(logo_path)

# Display the logo and text in the main section with adjusted spacing
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=100)
with col2:
    st.markdown("""
        <div style='display: flex; align-items: center;'>
            <h2 style='margin: 0;'>Dansk Jura - Juridisk Ekspert AI</h2>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Hvordan bruger man denne app"):
        Mekanism.loadhelp("Help.pdf")

# Add the input box for API key under the title
st.text_input("Indtast AI-nøgle", value=st.session_state['api_key'], key='api_key')
if st.button("Send nøgle"):
    set_api_key()

if st.session_state['wrong_key']:
    st.markdown(
        """
        <style>
        .wrong-key-button {
            background-color: lightcoral;
            color: black;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True
    )
    if st.markdown('<button class="wrong-key-button" onclick="window.location.reload()">Forkert nøgle</button>', unsafe_allow_html=True):
        clear_input()

# Add the logo to the sidebar above the title
with st.sidebar:
    st.image(logo, width=100)

# Input box for entering the question
def update_question():
    st.session_state['question'] = st.session_state['question_input']

question = st.text_input("Indtast dit spørgsmål", value=st.session_state['question'], key="question_input", on_change=update_question)

# Set the sidebar title based on the input box value
sidebar_title = st.session_state['question'] if 'question' in st.session_state and st.session_state['question'] else "Juridisk Ekspert"
st.sidebar.title(sidebar_title)
st.sidebar.write("Vigtige links vises her")

# Display summary points in the sidebar as links
if st.session_state['summary_points']:
    st.sidebar.write("Resumé:")
    for i, point in enumerate(st.session_state['summary_points']):
        if st.sidebar.button(point, key=f"summary_point_{i}"):
            handle_summary_click(point)

# Select boxes for laws with default value and callback
real_estate_law = st.selectbox(
    "Ejendomshovedlov", 
    real_estate_laws, 
    key="real_estate_law_selected",
    on_change=update_question_from_real_estate
)
finance_law = st.selectbox(
    "Finanshovedlov", 
    finance_laws, 
    key="finance_law_selected",
    on_change=update_question_from_finance
)
business_law = st.selectbox(
    "Erhvervshovedlov", 
    business_laws, 
    key="business_law_selected",
    on_change=update_question_from_business
)

# Layout for the buttons
col3, col4 = st.columns([1, 1])
with col3:
    st.button("Svar på spørgsmålet", key="answer_button", help="Klik for at få svaret", on_click=answer_question)
with col4:
    st.button("Ryd prompt", key="clear_button", help="Klik for at rydde prompten", on_click=clear_input)

# Display the answer if available and add summary points as clickable links
if st.session_state['answer']:
    st.write("Du spurgte: ", st.session_state['question'])
    st.write("Svar: ", st.session_state['answer'])

    if st.session_state['summary_lines']:
        st.write("Resumé punkter:")
        for i, line in enumerate(st.session_state['summary_lines']):
            if st.button(line, key=f"summary_line_{i}"):
                st.session_state['question'] = line
                st.experimental_rerun()

# Custom styling for the button
st.markdown("""
    <style>
    .stButton > button {
        background-color: black;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
