import streamlit as st
from PIL import Image
import openai
import Mekanism  # Ensure this module is correctly imported
import re  # Import re module for the findtxt function
import logging
import os
from openai.error import AuthenticationError  # Import AuthenticationError

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to find and extract summary lines from the answer
def findtxt(answer):
    logging.info(f"findtxt called with answer: {answer}")
    
    # Check if answer has text
    if answer:
        # Search for the keywords "**SUMMARY**," "**Summary**," "**summary**," or "**Key Points:**"
        summary_match = re.search(r'\*\*SUMMARY\*\*|\*\*Summary\*\*|\*\*summary\*\*', answer)
        if summary_match:
            # Find the position of the keyword
            start_pos = summary_match.end()
            # Extract the text after the keyword
            after_summary_text = answer[start_pos:].strip()
            
            # Look for "Key Points" after the summary keyword
            key_points_match = re.search(r'\*\*Key Points:?\*\*', after_summary_text)
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
            st.write("I DON'T FIND SUMMARY")
    else:
        st.write("NOT TEXT")
    
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
    except AuthenticationError:
        st.session_state['wrong_key'] = True
        return

    if st.session_state['question']:
        # First Job: Get detailed response from ChatGPT
        askjura_response = Mekanism.askjura(st.session_state['question'])
        detailed_answer = get_response(askjura_response)
        st.session_state['answer'] = detailed_answer

        # Extract summary lines automatically after getting the answer
        summary_lines = findtxt(detailed_answer)
        st.session_state['summary_lines'] = summary_lines

        # Second Job: Get summary response from ChatGPT
        links_response = Mekanism.links(st.session_state['question'])
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
    "Property Ownership", "Property Transfer", "Land Registration (Tinglysning)", "Mortgage Law",
    "Leasing and Tenancy Law", "Property Taxation", "Property Development", "Zoning Regulations",
    "Building Regulations", "Agricultural Property Law", "Easements and Rights of Way", "Condominium Law",
    "Cooperative Housing Law", "Expropriation Law", "Environmental Regulations", "Historical Preservation",
    "Foreclosure and Repossession", "Inheritance of Property", "Commercial Property Law", "Dispute Resolution in Property",
    "Property Valuation", "Land Use Planning", "Property Financing", "Homeowner Association Law",
    "Real Estate Investment Trusts (REITs)", "Public Property Law", "Private Property Law", "Property Management Law",
    "Urban Renewal Law", "Rent Control and Regulation", "Property Sales and Acquisition", "Real Estate Brokerage Law",
    "Property Insurance Law", "Property Disputes and Litigation", "Construction Contracts", "Property Development Finance",
    "Real Estate Agency Law", "Property Maintenance Law", "Property Fraud Prevention", "Landlord-Tenant Disputes",
    "Architectural Regulations", "Construction Law", "Housing Cooperatives", "Joint Ownership", "Private Roads and Pathways",
    "Public Infrastructure Law", "Renewable Energy Installations", "Tourism and Hospitality Property Law",
    "Waterfront Property Law", "Wildlife and Conservation Areas"
]

finance_laws = [
    "Banking Law", "Securities Law", "Investment Law", "Financial Regulation", "Insurance Law", "Pension Law",
    "Corporate Finance Law", "Capital Markets Law", "Anti-Money Laundering Law", "Financial Crime Law", "Payment Services Law",
    "Credit Law", "Consumer Finance Law", "Financial Supervision", "Financial Instruments Law", "Financial Contracts Law",
    "Public Finance Law", "Tax Law", "Mergers and Acquisitions", "Financial Services Law", "Derivatives Law", "Accounting Law",
    "Auditing Law", "Bankruptcy Law", "Insolvency Law", "Financial Reporting", "Risk Management Law", "Compliance Law",
    "Hedge Fund Law", "Private Equity Law", "Asset Management Law", "Fund Management Law", "Crowdfunding Law", "Fintech Law",
    "Microfinance Law", "Real Estate Finance Law", "International Finance Law", "Electronic Money Law", "Financial Technology Law",
    "Financial Stability Law", "Cross-Border Finance Law", "Financial Markets Law", "Market Abuse Law", "Financial Transparency Law",
    "Wealth Management Law", "Structured Finance Law", "Securitization Law", "Venture Capital Law", "Sovereign Debt Law",
    "International Banking Law", "Foreign Exchange Law", "Corporate Governance Law", "Financial Advisory Law",
    "Credit Rating Agency Law", "Financial Consumer Protection Law", "Economic Sanctions Law", "Trade Finance Law",
    "Project Finance Law", "Green Finance Law", "Sustainable Finance Law", "Basel III Compliance", "Solvency II Regulation",
    "Financial Ombudsman", "Digital Banking Law", "Open Banking Law", "Cryptocurrency Law", "Blockchain Finance Law",
    "Robo-Advisory Law", "Financial Inclusion Law", "Credit Union Law", "Central Bank Regulation", "Monetary Policy Law",
    "Foreign Direct Investment Law", "Economic Development Law", "Leasing Finance Law", "Factoring Law", "Trade Credit Insurance Law",
    "Financial Engineering Law", "Public-Private Partnership Law", "Export Credit Law", "Money Market Funds Law",
    "Real Estate Investment Law", "Private Banking Law", "Financial Literacy Law", "Shadow Banking Law", "Financial Planning Law",
    "Yield Enhancement Law", "Retirement Savings Law", "Actuarial Science Law", "Reinsurance Law"
]

business_laws = [
    "Company Law", "Commercial Contracts", "Corporate Governance", "Mergers and Acquisitions", "Intellectual Property Law",
    "Employment Law", "Competition Law", "Consumer Protection Law", "Bankruptcy and Insolvency Law", "Tax Law",
    "International Trade Law", "Environmental Law", "Energy Law", "Real Estate Law", "Financial Regulation", "Securities Law",
    "Anti-Money Laundering Law", "Data Protection Law", "E-commerce Law", "Public Procurement Law", "Franchise Law", "Agency Law",
    "Distribution Law", "Partnership Law", "Joint Ventures", "Commercial Dispute Resolution", "Arbitration Law", "Mediation Law",
    "Corporate Finance Law", "Private Equity Law", "Venture Capital Law", "Investment Funds Law", "Insurance Law", "Pension Law",
    "Shipping Law", "Aviation Law", "Transportation Law", "Media and Entertainment Law", "Telecommunications Law", "Healthcare Law",
    "Pharmaceutical Law", "Technology Law", "Construction Law", "Agriculture Law", "Mining Law", "Sports Law", "Gaming Law",
    "Hospitality Law", "Tourism Law", "Public Law", "Regulatory Compliance", "Corporate Restructuring", "Corporate Social Responsibility",
    "Anti-Corruption Law", "Export Controls", "Customs Law", "Trade Compliance", "Corporate Criminal Law", "White-Collar Crime",
    "Employee Benefits Law", "Labor Relations Law", "Health and Safety Law", "Advertising Law", "Marketing Law", "Consumer Rights Law",
    "Product Liability Law", "Supply Chain Law", "Outsourcing Law", "IT Law", "Cybersecurity Law", "Telecom Regulation", "Internet Law",
    "Cloud Computing Law", "Blockchain Law", "Cryptocurrency Law", "Crowdfunding Law", "Economic Sanctions Law", "Foreign Investment Law",
    "Sovereign Wealth Funds Law", "Commercial Leasing Law", "Property Leasing Law", "Real Estate Investment Law", "Renewable Energy Law",
    "Climate Change Law", "Waste Management Law", "Water Law", "Public Health Law", "Biotechnology Law", "Life Sciences Law",
    "Medical Devices Law", "Education Law", "Nonprofit Law", "Charitable Organizations Law", "Social Enterprises Law", "Family Business Law",
    "Entrepreneurship Law", "Startup Law", "Innovation Law", "Research and Development Law", "Grants and Subsidies Law",
    "Public-Private Partnership Law", "Infrastructure Law"
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

# Add the input box for API key under the title
st.text_input("Enter AI Key", value=st.session_state['api_key'], key='api_key')
if st.button("Send Key"):
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
    if st.markdown('<button class="wrong-key-button" onclick="window.location.reload()">Wrong Key</button>', unsafe_allow_html=True):
        clear_input()

# Add the logo to the sidebar above the title
with st.sidebar:
    st.image(logo, width=100)

# Function to get response from OpenAI
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
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

question = st.text_input("Enter your Question", value=st.session_state['question'], key="question_input", on_change=update_question)

# Set the sidebar title based on the input box value
sidebar_title = st.session_state['question'] if 'question' in st.session_state and st.session_state['question'] else "Legal Expert"
st.sidebar.title(sidebar_title)
st.sidebar.write("Important links will appear here")

# Display summary points in the sidebar as links
if st.session_state['summary_points']:
    st.sidebar.write("Summary:")
    for i, point in enumerate(st.session_state['summary_points']):
        if st.sidebar.button(point, key=f"summary_point_{i}"):
            handle_summary_click(point)

# Select boxes for laws with default value and callback
real_estate_law = st.selectbox(
    "Real Estate main Law", 
    real_estate_laws, 
    key="real_estate_law_selected",
    on_change=update_question_from_real_estate
)
finance_law = st.selectbox(
    "Finance main Law", 
    finance_laws, 
    key="finance_law_selected",
    on_change=update_question_from_finance
)
business_law = st.selectbox(
    "Business main Law", 
    business_laws, 
    key="business_law_selected",
    on_change=update_question_from_business
)

# Layout for the buttons
col3, col4 = st.columns([1, 1])
with col3:
    st.button("Answer The Question", key="answer_button", help="Click to get the answer", on_click=answer_question)
with col4:
    st.button("Clear Prompt", key="clear_button", help="Click to clear the prompt", on_click=clear_input)

# Display the answer if available and add summary points as clickable links
if st.session_state['answer']:
    st.write("You asked: ", st.session_state['question'])
    st.write("Answer: ", st.session_state['answer'])
    
    # Extract summary lines and display them as clickable buttons
    if st.session_state['summary_lines']:
        st.write("Summary Points:")
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



