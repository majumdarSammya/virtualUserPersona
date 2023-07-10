import pandas as pd
import streamlit as st
from streamlit_chat import message
from helperFunctions import business, generate_response, read_dataset,  tech, get_text, customUser

# openai.api_type = st.secrets['API_TYPE']
# openai.api_base = st.secrets['API_BASE']
# openai.api_version = st.secrets['API_VERSION']
# openai.api_key = st.secrets['API_KEY']


def main():
    demo_folder = "HR/data"
    data_folder = "HR/HRdata"

    metatag_system_prompt = """ 
    
        You are Meta Tag Pro, a data specialist. You are required to perform the following tasks:

        - From a given dataset, you need to examine, understand, analyze the data
        - Describe the key components and structure of the data file 
        - Outline the data types of the values, the relationships between the data, and check if any dependencies are present in the data
        - Additionally, identify any potential data inconsistencies or abnormalities that you notice
        - Propose solutions for improvement based on  your findings.
        - Return a SQL query based on user input to return data that matches said input
    
    """

    menu = ["Home", "Business View", "Technical View",
            "SQL Converter"]
    choice = st.sidebar.selectbox("Select your role", menu)
    st.sidebar.markdown("----")

    model = st.sidebar.radio('Pick a model version',
                             ('gpt-3.5-turbo', 'gpt-4'))
    data_string = read_dataset(demo_folder)
    dataStringNew = read_dataset(data_folder)
    init_prompt = generate_response(
        metatag_system_prompt, dataStringNew, model)

    if choice == "Home":
        home()
    elif choice == "Business View":
        business(data_folder, model, metatag_system_prompt, init_prompt)
    elif choice == "Technical View":
        tech(model, metatag_system_prompt, init_prompt)
    elif choice == "SQL Converter":
        customUser(model)


def home():

    st.title("Data Modeller")
    st.markdown("""Data Modeller is a powerful tool that drives data management efficiency, assists with data analysis, providing SQL code by leveraging cutting-edge LLMs. \n
• Easily understand existing datasets with structured, human-readable descriptions and automated metadata management. \n
• Advanced capabilities include generating data product descriptions, creating data dictionaries and suggesting potential use cases and improvements, accelerating technical documentation creation. \n
• Identify PII and sensitive information, providing an extra layer of governance to your data management processes. \n
• For the technical user, the Data Assistant can provide SQL code based on plain english user input in proper code format from the data provided. \n
• The Data Assistant can propose potential improvements in the structure/architecture of the data provided. \n
""")

    st.header("Security and Compliance")
    st.markdown("This Data Modeller works by leveraging Azure OpenAI services and its APIs. For use cases that are sensitive and highly regulated in nature, we have compiled the important security highlights of Azure OpenAI:")
    st.markdown(
        "1. Data used to fine-tune models are stored in Azure Storage and are encrypted at rest. \n 2. User Prompts (including data uploaded from the UI) and its corresponding chat completions are stored in servers for 30 days, then deleted. \n 3. Access to this data are limited to Microsoft employees only in the case of Azure OpenAI service abuse by customer. \n 4. This 30 day data retention and Microsoft employee access can be removed by submitting a form to Microsoft defining the use-case. Once approved nothing will be retained in their servers. \n 5. Chat, completions, prompts are not used to train, test, retrain Azure OpenAI models \n 6. Currently, most of our prompts can produce good results from a well defined data dictionary, so redacting any further information from the data is being considered. \n")
    st.markdown("[Source](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext)")


if __name__ == "__main__":
    main()
