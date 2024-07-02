import streamlit as st

def askjura(intext):
    request_text = (
       f"Please conduct an in-depth research on {intext} within the context of Danish law using the Karnov law database and other reliable sources such as ministries, courthouses, and relevant databases. Gather comprehensive information, including associated costs. Provide the law paragraphs and analyze them exactly as they are. Analyze everything with great details, formatted as follows: * BOLD Capitalized titles and headings in a larger font size than the rest of the text * BOLD paragraphs and subtitles in a slightly smaller font size than the capitalized titles and headings. Present the research in a clear and concise manner, highlighting the most important points that refer to the law and relevant laws. Conclude with a Summary. Analyze with great detail all the text and sections, and find the most important points only about the law paragraphs that assosiated with the subject. Then summarize the key points in separate lines, with each key point restricted to 40 characters."

    )
    return request_text


def askpoint(intext):
    request_text = (
      f"Gennemfør en dybdegående undersøgelse af {intext} inden for rammerne af dansk lovgivning. Anvend Karnov lovdatabase og andre pålidelige kilder som ministerier, domstole og relevante databaser. Indsaml omfattende information, herunder forbundne omkostninger. Giv lovparagrafferne og analyser dem præcis som de er. Analyser alt med stor detaljerigdom, formateret som følger: BOLD KAPITALISEREDE TITLER OG OVERSKRIFTER I EN STØRRE SKRIFTSTØRRELSE END RESTEN AF TEKSTEN BOLD afsnit og undertitler i en lidt mindre skriftstørrelse end de kapitaliserede titler og overskrifter. Præsenter forskningen på en klar og præcis måde, fremhæv de vigtigste punkter, der henviser til loven og relevante love. Afslut med et resumé. Analyser med stor detaljerigdom alle tekster og afsnit, og find de vigtigste punkter kun om lovparagrafferne, der er forbundet med emnet. Sammenfat derefter nøglepunkterne i separate linjer, under en tekst 'Sammenfatningspunkter' uden karakter '*' hver Sammemfatningspunkt i separate linje med hvert nøglepunkt begrænset til 40 tegn."
    )
    return request_text

def links(inprompt):
    return f"Provide a comprehensive list of categories or subfields within {inprompt} Main Law in Denmark, as outlined in the Karnov law database and relevant online sources. Organize the categories in a structured manner, explaining how they are arranged within the Danish legal system. Format the response with each category or subfield on a separate line, with a maximum of 40 characters per line, for easy reference and clarity.just display only the law no other comments"


def askbox():
    user_input = st.text_input("Ask a Question", "")
    if user_input:
        return askjura(user_input)
    return ""

def askjuradk(intext):
    request_text = (
      f"ennemfør en dybdegående undersøgelse af {intext} inden for rammerne af dansk lovgivning. Anvend Karnov lovdatabase og andre pålidelige kilder som ministerier, domstole og relevante databaser. Indsaml omfattende information, herunder forbundne omkostninger. Giv lovparagrafferne og analyser dem præcis som de er. Analyser alt med stor detaljerigdom, formateret som følger: BOLD KAPITALISEREDE TITLER OG OVERSKRIFTER I EN STØRRE SKRIFTSTØRRELSE END RESTEN AF TEKSTEN BOLD afsnit og undertitler i en lidt mindre skriftstørrelse end de kapitaliserede titler og overskrifter. Præsenter forskningen på en klar og præcis måde, fremhæv de vigtigste punkter, der henviser til loven og relevante love. Afslut med et resumé. Analyser med stor detaljerigdom alle tekster og afsnit, og find de vigtigste punkter kun om lovparagrafferne, der er forbundet med emnet. Sammenfat derefter nøglepunkterne i separate linjer, Alle separate linjer skal være lige under hinanden uden tomme linjer imellem, under en tekst 'Sammenfatningspunkter' uden karakter '*' hver Sammemfatningspunkt i separate linje med hvert nøglepunkt begrænset til 40 tegn og tilslute '.''."

    )
    return request_text


def linksdk(inprompt):
    return f"Lever en omfattende liste over kategorier eller underområder inden for {inprompt} hovedlov i Danmark, som skitseret i Karnov lovdatabase og relevante onlinekilder. Organiser kategorierne på en struktureret måde, og forklar, hvordan de er arrangeret inden for det danske retssystem. Formatér svaret med hver kategori eller underområde på en separat linje, med maksimalt 40 tegn pr. linje, for nem reference og klarhed. Vis kun loven uden andre kommentarer"

def askbox():
    user_input = st.text_input("Ask a Question", "")
    if user_input:
        return askjura(user_input)
    return ""

#-----------------------------------------------------------------------
def loadhelp(tpath):
    # Read the file content
    try:
        with open(tpath, 'rb') as file:
            file_content = file.read()
            
        # Provide a download button
        st.download_button(
            label="Download File",
            data=file_content,
            file_name=tpath.split('/')[-1],  # Extract file name from path
            mime="application/octet-stream"
        )
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
