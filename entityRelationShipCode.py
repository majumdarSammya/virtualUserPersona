import openai
import streamlit as st
from helperFunctions import generate_response

openai.api_key = st.secrets["API_KEY"]


def mermaid_chart(markdown_code):
    html_code = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <div class="mermaid">{markdown_code}</div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    """
    return html_code


system_prompt = """

            You are a data modeller. You have to create markdown code for Entity Relationship diagram for mermaid.js 
            library using the following information.

"""
markdown_code = generate_response(system_prompt, prompt, model)
