import streamlit as st




def askjura(intext):
    request_text = (
       f"Please conduct an in-depth research on {intext} within the context of Danish law using the Karnov law database and other reliable sources such as ministries, courthouses, and relevant databases. Gather comprehensive information, including associated costs. Provide the law paragraphs and analyze them exactly as they are. Analyze everything with great details, formatted as follows: * BOLD Capitalized titles and headings in a larger font size than the rest of the text * BOLD paragraphs and subtitles in a slightly smaller font size than the capitalized titles and headings. Present the research in a clear and concise manner, highlighting the most important points that refer to the law and relevant laws. Conclude with a Summary. Analyze with great detail all the text and sections, and find the most important points only about the law paragraphs that assosiated with the subject. Then summarize the key points in separate lines, with each key point restricted to 40 characters."

    )
    return request_text


def askpoint(intext):
    request_text = (
      f"Please conduct an in-depth research on {intext} within the context of Danish law using the Karnov law database and other reliable sources such as ministries, court houses, and relevant databases. Gather comprehensive information, including associated costs. Provide the law paragraphs exactly as they are, formatted as follows: * **BOLD** Capitalized titles and headings in larger font size than the rest of the text * **BOLD** paragraphs and subtitles in slightly smaller font size than the capitalized titles and headings Present the research in a clear and concise manner, highlighting the most important points and relevant laws. Conclude with a **Summary** section, where you summarize the key points in separate lines, each restricted to 40 characters. Key requirements: * Use Karnov law database and additional reliable sources * Present law paragraphs exactly as they are * Follow specific formatting guidelines * Provide a clear and concise summary of the research * Each summary point limited to 40 characters Please reply in the exact format specified, ensuring accuracy and precision in your response.** within the context of Danish law using the Karnov law database and other reliable sources such as ministries, court houses, and relevant databases. Gather comprehensive information, including associated costs. Provide the law paragraphs exactly as they are, formatted as follows: * **BOLD** Capitalized titles and headings in larger font size than the rest of the text * **BOLD** paragraphs and subtitles in slightly smaller font size than the capitalized titles and headings Present the research in a clear and concise manner, highlighting the most important points and relevant laws. Conclude with a **Summary** section, where you summarize the key points in separate lines, each restricted to 40 characters. Key requirements: * Use Karnov law database and additional reliable sources * Present law paragraphs exactly as they are * Follow specific formatting guidelines * Provide a clear and concise summary of the research * Each summary point limited to 40 characters Please reply in the exact format specified, ensuring accuracy and precision in your response."
    )
    return request_text

def links(inprompt):
    return f"Provide a comprehensive list of categories or subfields within {inprompt} Main Law in Denmark, as outlined in the Karnov law database and relevant online sources. Organize the categories in a structured manner, explaining how they are arranged within the Danish legal system. Format the response with each category or subfield on a separate line, with a maximum of 40 characters per line, for easy reference and clarity.just display only the law no other comments"


def askbox():
    user_input = st.text_input("Ask a Question", "")
    if user_input:
        return askjura(user_input)
    return ""

