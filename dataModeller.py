import openai
import pandas as pd
import os
import streamlit as st
from streamlit_chat import message


# openai.api_type = st.secrets['API_TYPE']
# openai.api_base = st.secrets['API_BASE']
# openai.api_version = st.secrets['API_VERSION']
# openai.api_key = st.secrets['API_KEY']

openai.api_key = st.secrets["API_KEY"]


@st.cache_data
def generate_response(system_prompt, user_prompt, model):

    response = openai.ChatCompletion.create(
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
        model=model,
        max_tokens=2048,
        temperature=0.3
        # engine='demo3'
    )

    return response['choices'][0]['message']['content'].strip()


def read_dataset(folder_path):
    dataset_as_string = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            non_null_rows = df.dropna().iloc[:5]
            dataset_as_string[filename] = non_null_rows.to_csv(
                index=False, sep=',')
        elif filename.endswith('.xlsx'):
            excel_data = pd.read_excel
            for sheet_name, sheet_data in excel_data.items():
                sheet_data = sheet_data.dropna().iloc[:5]
                dataset_as_string[sheet_name] = sheet_data.to_csv(
                    index=False, sep=',')

    data_string = ""
    for table_name, table_string in dataset_as_string.items():
        data_string += f"Table: {table_name}" + table_string + "\n"

    return data_string


def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


def main():
    demo_folder = "HR/data"
    data_folder = "HR/HRdata"
    metatag_system_prompt_previous = """Your name is MetaTag Pro. You are a data specialist, you need to perform the following tasks:
- From a given dataset, you need to examine, understand, analyze the data
- If there is an ETL code relating to the given dataset, you need to review and understand the code
- You then need to create a summary description of their data product which can be published on the data product marketplace to help consumers understand the data product. 
- You should suggest potential use cases of the input dataset
- Finally you need to reorgnise the output as README.md format with the first section as Summary, second section as potential use cases, third section as data description. In the third section,  for each attribute, it should be associated with data type and a detailed description structured as a table"""

    metatag_system_prompt = """ 
    
        You are Meta Tag Pro, a data specialist. You are required to perform the following tasks:

        - From a given dataset, you need to examine, understand, analyze the data
        - Describe the key components and structure of the data file 
        - Outline the data types of the values, the relationships between the data, and check if any dependencies are present in the data
        - Additionally, identify any potential data inconsistencies or abnormalities that you notice
        - Propose solutions for improvement based on  your findings.
        - Return a SQL query based on user input to return data that matches said input
    
    """

    menu = ["Home", "Business User", "Technical User",
            "Technical User Two", "Business User Two"]
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
    elif choice == "Business User":
        business(data_folder, model, metatag_system_prompt, init_prompt)
    elif choice == "Technical User":
        tech(model, metatag_system_prompt, init_prompt)
    elif choice == "Technical User Two":
        techUserTwo(model, metatag_system_prompt, init_prompt)
    elif choice == "Business User Two":
        businessUserTwo(demo_folder, model, metatag_system_prompt, generate_response(
            metatag_system_prompt, data_string, model))


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


def business(folder, model, metatag_system_prompt, init_prompt):
    st.title("For Business User")

    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    conversation_history.append({"role": "assistant", "content": init_prompt})

    st.sidebar.markdown("----")
    if st.sidebar.button("Load Dataset") or st.session_state.data_loaded:
        for filename in os.listdir(folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)
                non_null_rows = df.iloc[:5]
                st.markdown(f"### Dataset sample: `{filename}`")
                st.table(non_null_rows)
        st.session_state.data_loaded = True

    st.sidebar.markdown("----")

    questions = {'Summary': 'Give me the summary of the data in one paragraph',
                 'Use_Case': 'Give me the potential use cases of this data',
                 'Data_Description': 'Give me only the data description section',
                 'Sensitive_Info': 'Which attributes contain personal sensitive information?'}

    storeResponsesBizUser = ""
    qCountBizUser = 1
    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            # conversation_history.append({"role": "user", "content": questions[q]})
            prompt = init_prompt + '\n' + questions[q]
            print(prompt)
            output = generate_response(metatag_system_prompt, prompt, model)
            storeResponsesBizUser += f'Q{qCountBizUser}. ' + \
                questions[q] + \
                '\n\n' + output + '\n\n\n\n'
            qCountBizUser += 1
            # conversation_history.append({"role": "assistant", "content": output})
            with st.expander(questions[q]):
                st.write(output)
                # st.button("Export " + q + " to Data Marketplace")
        st.sidebar.download_button(
            "Download Responses", data=storeResponsesBizUser)


# start

def businessUserTwo(folder, model, metatag_system_prompt, init_prompt):
    st.title("For Business User Two")

    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    conversation_history.append({"role": "assistant", "content": init_prompt})

    st.sidebar.markdown("----")
    if st.sidebar.button("Load Dataset") or st.session_state.data_loaded:
        for filename in os.listdir(folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path)
                non_null_rows = df.iloc[:5]
                st.markdown(f"### Dataset sample: `{filename}`")
                st.table(non_null_rows)
        st.session_state.data_loaded = True

    st.sidebar.markdown("----")

    questions = {'Summary': 'Give me the summary of the data in one paragraph',
                 'Use_Case': 'Give me the potential use cases of this data',
                 'Data_Description': 'Give me only the data description section',
                 'Sensitive_Info': 'Which attributes contain personal sensitive information?'}

    storeResponsesBizUserTwo = ""
    qCountBizUserTwo = 1
    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            # conversation_history.append({"role": "user", "content": questions[q]})
            prompt = init_prompt + '\n' + questions[q]
            print(prompt)
            output = generate_response(metatag_system_prompt, prompt, model)
            storeResponsesBizUserTwo += f'Q{qCountBizUserTwo}. ' + \
                questions[q] + \
                '\n\n' + output + '\n\n\n\n'
            qCountBizUserTwo += 1
            # conversation_history.append({"role": "assistant", "content": output})
            with st.expander(questions[q]):
                st.write(output)
                # st.button("Export " + q + " to Data Marketplace")
        st.sidebar.download_button(
            "Download Responses", data=storeResponsesBizUserTwo)
# # end


def techUserTwo(model, metatag_system_prompt, init_prompt):
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    # conversation_history.append({"role": "assistant", "content": init_prompt})
    st.title("For Technical User Two")
    st.sidebar.markdown("----")

    st.sidebar.markdown('----')

    # downloadButton = st.sidebar.download_button("Download Responses")

    # st.sidebar.markdown('----')

    uploaded_files = st.sidebar.file_uploader(
        "Select the source code to interpret", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        code_txt = uploaded_file.getvalue()
        content = str(uploaded_file.name) + " " + str(code_txt)
        conversation_history.append({"role": "user", "content": content})
        st.write("filename:", uploaded_file.name)
        st.code(code_txt.decode("utf-8"), language='python')

    st.sidebar.markdown("----")

    questions = {'Summary': 'give me a brief one paragraph summary of the uploaded data',
                 'SQL table': 'create a SQL table based on the above data in proper code format, breaking it into several tables with primary keys and foreign keys if necessary.',
                 'Data Model': 'Can you show the data model in tabular format if we create several SQL tables based on the above data dictionary with primary key relationships in details'}

    # for the above table -> the input to the 'get SQL code'

    storeResponsesTechUserTwo = ""
    qCountTechUserTwo = 1
    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            prompt = "\n".join([message["content"]
                                for message in conversation_history])
            prompt += '\n' + questions[q]

            print(prompt)
            output = generate_response(
                metatag_system_prompt, prompt, model)
            storeResponsesTechUserTwo += f'Q{qCountTechUserTwo}. ' + \
                questions[q] + '\n\n' + output + '\n\n\n\n'
            qCountTechUserTwo += 1
            with st.expander(questions[q]):
                st.write(output)
                if q in ['README', 'Code']:
                    st.button("Download " + q)

        st.sidebar.download_button(
            "Download Responses", data=storeResponsesTechUserTwo)


def tech(model, metatag_system_prompt, init_prompt):
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    # conversation_history.append({"role": "assistant", "content": init_prompt})
    st.title("For Technical User")
    st.sidebar.markdown("----")

    query = st.sidebar.text_input('Input your query')
    queryButton = st.sidebar.button("Get SQL code")

    st.sidebar.markdown('----')

    uploaded_files = st.sidebar.file_uploader(
        "Select the source code to interpret", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        code_txt = uploaded_file.getvalue()
        content = str(uploaded_file.name) + " " + str(code_txt)
        conversation_history.append({"role": "user", "content": content})
        st.write("filename:", uploaded_file.name)
        st.code(code_txt.decode("utf-8"), language='python')

    st.sidebar.markdown("----")

    questions = {'Summary': 'Can you give me a brief one paragraph summary of the data',
                 'Structure': 'How is the data file structured',
                 'Data_Description': 'Give me the data types of the data present inside the columns in proper format that can be used for database table in bullet points',
                 'Dependencies': 'Are there any dependencies present in the data?',
                 'Relationships': 'Can you find any relationship between the columns in this data',
                 'Tabular Data': 'Can you show the column names, their datatypes in SQL format and a brief description in a nice tabular format',
                 'SQL table': 'create a SQL table based on the above data in proper code format, breaking it into several tables with primary keys.',
                 'Data Model': 'Can you show the data model in tabular format if we create several SQL tables based on this data with primary key relationships in details'}

    # for the above table -> the input to the 'get SQL code'
    storeResponses = ""
    qCount = 1
    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            prompt = "\n".join([message["content"]
                                for message in conversation_history])
            prompt += '\n' + questions[q]

            # print(prompt)
            output = generate_response(
                metatag_system_prompt, prompt, model)
            storeResponses += f'Q{qCount}. ' + \
                questions[q] + '\n\n' + output + '\n\n\n\n'
            qCount += 1
            with st.expander(questions[q]):
                st.write(output)
                if q in ['README', 'Code']:
                    st.button("Download " + q)

    if queryButton or st.session_state.content_generated:

        prompt = "\n".join([message["content"]
                           for message in conversation_history])
        prompt += '\n' + query
        with st.expander('SQL code:'):
            st.write(generate_response(metatag_system_prompt, prompt, model))

        st.sidebar.download_button(
            "Download Responses", data=storeResponses)


if __name__ == "__main__":
    main()
