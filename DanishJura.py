import streamlit as st
from PIL import Image
import openai
import Mekanism  # Ensure this module is correctly imported
import re  # Import re module for the findtxt function
import logging
import os
# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to find and extract summary lines from the answer
def findtxt(answer):
    logging.info(f"findtxt called with answer: {answer}")
    
    # Check if answer has text
    if answer:
        # Search for the keywords "**SUMMARY**," "**Summary**," "**summary**," or "**Key Points:**"
        #summary_match = re.search(r'\*\*SAMMENFATNINGSPUNKTER\*\*|\*\*Summary\*\*|\*\*summary\*\*', answer)
        summary_match = re.search(r'\*\*SAMMENFATNINGSPUNKTER\*\*', answer)
        if summary_match:
            # Find the position of the keyword
            start_pos = summary_match.end()
            # Extract the text after the keyword
            after_summary_text = answer[start_pos:].strip()
            
            # Look for "Key Points" after the summary keyword
            key_points_match = re.search(r'\*\*SAMMENFATNINGSPUNKTER?\*\*', after_summary_text)
            if key_points_match:
                start_pos = key_points_match.end()
                after_summary_text = after_summary_text[start_pos:].strip()

            # Extract the lines under the keyword
            summary_lines = []
            for line in after_summary_text.split('\n'):
                line = line.strip()
                if line:
                    summary_lines.append(line)
                elif line == "":  # Stop if an empty line is encountered
                    break
            
            return summary_lines
        else:
            st.write("Jeg kan ikke finde et resumé")
    else:
        st.write("Ingen tekst")
    
    return []

# Function to handle "Answer The Question" button click
def answer_question():
    if 'api_key' not in st.session_state or not st.session_state['api_key']:
        st.session_state['wrong_key'] = True
        return

    openai.api_key = st.session_state['api_key']
    try:
        # Test the API key with a simple request
        openai.Model.list()
    except openai.error.AuthenticationError:
        st.session_state['wrong_key'] = True
        return

    if st.session_state['question']:
        # First Job: Get detailed response from ChatGPT
        askjura_response = Mekanism.askjuradk(st.session_state['question'])
        detailed_answer = get_response(askjura_response)
        st.session_state['answer'] = detailed_answer

        # Extract summary lines automatically after getting the answer
        summary_lines = findtxt(detailed_answer)
        st.session_state['summary_lines'] = summary_lines

        # Second Job: Get summary response from ChatGPT
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

# Set default OpenAI API key if not already set
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
if 'wrong_key' not in st.session_state:
    st.session_state['wrong_key'] = False

# Define the lists of laws
real_estate_laws = [
    "", "Ejendomsejerskab", "Ejendomsoverdragelse", "Tinglysning", "Pantsætningsret",
    "Leje- og boliglovgivning", "Ejendomsbeskatning", "Ejendomsudvikling", "Zoneregler",
    "Bygningsreglement", "Landbrugsejendomslov", "Servitutter og færdselsret", "Ejerlejlighedslov",
    "Andelsboliglov", "Ekspropriationslov", "Miljøregler", "Historisk bevaring",
    "Tvangsauktion og rekvisition", "Arv af ejendom", "Erhvervsejendomslov", "Tvistbilæggelse i ejendom",
    "Ejendomsvurdering", "Lokalplanlægning", "Ejendomsfinansiering", "Ejerforeningslov",
    "Ejendomsinvesteringsforeninger (REITs)", "Offentlig ejendomslov", "Privat ejendomslov", "Ejendomsadministrationslov",
    "Byfornyelseslov", "Huslejeregulering", "Ejendomssalg og erhvervelse", "Ejendomsmæglerlov",
    "Ejendomsforsikringslov", "Ejendomstvister og retssager", "Byggekontrakter", "Ejendomsudviklingsfinansiering",
    "Ejendomsmæglerlov", "Ejendomsvedligeholdelseslov", "Forebyggelse af ejendomssvindel", "Udlejer-lejer tvister",
    "Arkitekturregler", "Byggeret", "Boligkooperativer", "Fælleseje", "Private veje og stier",
    "Offentlig infrastrukturlov", "Installationer til vedvarende energi", "Turist- og hotel ejendomslov",
    "Ejendomslov ved vandfront", "Vildt- og bevaringsområder"
]

finance_laws = [
    "", "Banklovgivning", "Værdipapirret", "Investeringslovgivning", "Finansiel regulering", "Forsikringslovgivning", "Pensionslovgivning",
    "Erhvervsfinansieringslov", "Kapitalmarkedslovgivning", "Hvidvaskningslovgivning", "Finansiel kriminalitetslovgivning", "Betalingstjenester",
    "Kreditlovgivning", "Forbrugerfinansiering", "Finanstilsyn", "Lov om finansielle instrumenter", "Lov om finansielle kontrakter",
    "Offentlig finanslov", "Skattelovgivning", "Fusions- og opkøbslovgivning", "Finansielle tjenester", "Afledte finansielle instrumenter", "Regnskabslov",
    "Revisionslovgivning", "Konkurslovgivning", "Insolvenslovgivning", "Finansiel rapportering", "Risikostyringslovgivning", "Compliance-lovgivning",
    "Hedgefondslovgivning", "Private equity lovgivning", "Kapitalforvaltningslov", "Fondsforvaltningslovgivning", "Crowdfunding lovgivning", "Fintech-lovgivning",
    "Mikrofinansieringslovgivning", "Ejendomsfinansieringslovgivning", "International finanslovgivning", "Elektroniske penge lovgivning", "Finansiel teknologilovgivning",
    "Finansiel stabilitetslovgivning", "Tværnational finanslovgivning", "Finansmarkedslovgivning", "Markedsmisbrugslovgivning", "Finansiel gennemsigtighed",
    "Formueforvaltning", "Struktureret finanslovgivning", "Securitization lovgivning", "Risikokapital lovgivning", "Statens gældslovgivning",
    "International banklovgivning", "Valutalovgivning", "Corporate governance-lovgivning", "Finansiel rådgivningslovgivning",
    "Lov om kreditvurderingsbureauer", "Forbrugerbeskyttelse i finansielle tjenester", "Økonomiske sanktioner", "Handelsfinansiering",
    "Projektfinansieringslovgivning", "Grøn finanslovgivning", "Bæredygtig finanslovgivning", "Basel III overholdelse", "Solvens II regulering",
    "Finansiel ombudsmand", "Digital banklovgivning", "Open banking lovgivning", "Kryptovaluta lovgivning", "Blockchain finanslovgivning",
    "Robo-rådgivningslovgivning", "Finansiel inklusionslovgivning", "Lov om kreditforeninger", "Regulering af centralbanker", "Monetær politiklovgivning",
    "Udenlandske direkte investeringer", "Økonomisk udviklingslovgivning", "Leasingfinansieringslovgivning", "Factoring-lovgivning", "Handelskreditforsikring",
    "Finansiel ingeniørkunst", "Offentlig-private partnerskaber", "Eksportkreditlovgivning", "Pengemarkedsfondslovgivning",
    "Ejendomsinvesteringslovgivning", "Private banking lovgivning", "Finansiel literacy lovgivning", "Shadow banking lovgivning", "Finansiel planlægning",
    "Forbedring af afkast", "Pensionsopsparingslovgivning", "Aktuariel lovgivning", "Genforsikringslovgivning"
]

business_laws = [
    "", "Selskabslovgivning", "Kommercielle kontrakter", "Corporate governance", "Fusions- og opkøbslovgivning", "Intellektuel ejendomslovgivning",
    "Ansættelsesret", "Konkurrencelovgivning", "Forbrugerbeskyttelse", "Konkurs- og insolvenslovgivning", "Skattelovgivning",
    "International handelslovgivning", "Miljølovgivning", "Energilovgivning", "Ejendomsret", "Finansiel regulering", "Værdipapirret",
    "Hvidvaskningslovgivning", "Databeskyttelseslovgivning", "E-handelslovgivning", "Offentlige indkøb", "Franchise-lovgivning", "Agenturlovgivning",
    "Distributionslovgivning", "Partnerskabslovgivning", "Joint ventures", "Kommerciel tvistbilæggelse", "Voldgiftslovgivning", "Mæglingslovgivning",
    "Corporate finance lovgivning", "Private equity lovgivning", "Risikokapital lovgivning", "Investeringsfonds lovgivning", "Forsikringslovgivning", "Pensionslovgivning",
    "Søret", "Luftfartslovgivning", "Transportlovgivning", "Medie- og underholdningslovgivning", "Telekommunikationslovgivning", "Sundhedslovgivning",
    "Lægemiddellovgivning", "Teknologilovgivning", "Byggeret", "Landbrugslovgivning", "Minedriftslovgivning", "Sportslovgivning", "Spillelovgivning",
    "Hospitality lovgivning", "Turismelovgivning", "Offentlig ret", "Reguleringsoverholdelse", "Virksomhedsrestrukturering", "Virksomheders sociale ansvar",
    "Antikorruptionslovgivning", "Eksportkontroller", "Toldlovgivning", "Handelsoverholdelse", "Virksomhedskriminalitet", "Hvidkravekriminalitet",
    "Ansættelsesfordele", "Arbejdsforhold", "Sundhed og sikkerhed", "Reklamelovgivning", "Markedsføringslovgivning", "Forbrugerrettigheder",
    "Produktansvarslovgivning", "Forsyningskæde lovgivning", "Outsourcing lovgivning", "IT-lovgivning", "Cybersikkerhedslovgivning", "Telekommunikationsregulering",
    "Internetlovgivning", "Cloud computing lovgivning", "Blockchain-lovgivning", "Kryptovaluta lovgivning", "Crowdfunding lovgivning", "Økonomiske sanktioner",
    "Udenlandske investeringer", "Statens formuefonde", "Erhvervsleasing", "Ejendomsleasing", "Ejendomsinvesteringslovgivning", "Vedvarende energilovgivning",
    "Klimalovgivning", "Affaldshåndtering", "Vandlovgivning", "Offentlig sundhed", "Bioteknologilovgivning", "Life sciences lovgivning",
    "Medicinsk udstyr", "Uddannelseslovgivning", "Nonprofit lovgivning", "Velgørende organisationer", "Sociale virksomheder", "Familievirksomheder",
    "Entreprenørskab", "Opstartslovgivning", "Innovationslovgivning", "Forskning og udvikling", "Tilskud og subsidier",
    "Offentlig-private partnerskaber", "Infrastrukturlovgivning"
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
            <h2 style='margin: 0;'>Danish Jura - Legal Expert AI</h2>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Sådan bruger du denne app"):
        Mekanism.loadhelp("Help.pdf")

# Add the input box for API key under the title
st.text_input("Indtast AI nøgle", value=st.session_state['api_key'], key='api_key')
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

# Function to get response from OpenAI
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "I am a Danish lawyer with over 35 years of experience specializing in Danish finance law, business law, real estate law, and banking law. rrr."},
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

# Function to update the question input box from list box selection
def update_question_from_real_estate():
    st.session_state['question'] = st.session_state['real_estate_law_selected']

def update_question_from_finance():
    st.session_state['question'] = st.session_state['finance_law_selected']

def update_question_from_business():
    st.session_state['question'] = st.session_state['business_law_selected']

# Input box for entering the question
def update_question():
    st.session_state['question'] = st.session_state['question_input']

question = st.text_input("Indtast dit spørgsmål", value=st.session_state['question'], key="question_input", on_change=update_question)

# Set the sidebar title based on the input box value
sidebar_title = st.session_state['question'] if 'question' in st.session_state and st.session_state['question'] else "Juridisk ekspert"
st.sidebar.title(sidebar_title)
st.sidebar.write("Vigtige links vil vises her")

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
    st.button("Besvar spørgsmålet", key="answer_button", help="Klik for at få svaret", on_click=answer_question)
with col4:
    st.button("Ryd forespørgsel", key="clear_button", help="Klik for at rydde forespørgslen", on_click=clear_input)

# Display the answer if available and add summary points as clickable links
if st.session_state['answer']:
    st.write("Du spurgte: ", st.session_state['question'])
    st.write("Svar: ", st.session_state['answer'])
    
    # Extract summary lines and display them as clickable buttons
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
