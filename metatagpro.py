import openai
import pandas as pd
import os
import streamlit as st

from streamlit_chat import message

openai.api_key = "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"


@st.cache_data
def generate_response(system_prompt, user_prompt, model):

    response = openai.ChatCompletion.create(
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
        model=model,
        max_tokens=2048,
        temperature=0.3,
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

    menu = ["Home", "Business User", "Technical User"]
    choice = st.sidebar.selectbox("Select your role", menu)
    st.sidebar.markdown("----")

    model = st.sidebar.radio('Pick a model version',
                             ('gpt-3.5-turbo', 'gpt-4'))
    data_string = read_dataset(demo_folder)
    init_prompt = generate_response(metatag_system_prompt, data_string, model)

    if choice == "Home":
        home()
    elif choice == "Business User":
        business(demo_folder, model, metatag_system_prompt, init_prompt)
    elif choice == "Technical User":
        tech(model, metatag_system_prompt, init_prompt)


def home():

    st.title("MetaTagPro - Data Assistant")
    st.markdown("""MetaTagPro - Data Assistant is a powerful tool that drives data management efficiency, assists with data analysis, providing SQL code by leveraging cutting-edge LLMs. \n
• Easily understand existing datasets with structured, human-readable descriptions and automated metadata management. \n
• Advanced capabilities include generating data product descriptions, creating data dictionaries and suggesting potential use cases and improvements, accelerating technical documentation creation. \n
• Identify PII and sensitive information, providing an extra layer of governance to your data management processes. \n
• For the technical user, the Data Assistant can provide SQL code based on plain english user input in proper code format from the data provided. \n
• The Data Assistant can propose potential improvements in the structure/architecture of the data provided. \n
""")


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

    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            # conversation_history.append({"role": "user", "content": questions[q]})
            prompt = init_prompt + '\n' + questions[q]
            print(prompt)
            output = generate_response(metatag_system_prompt, prompt, model)
            # conversation_history.append({"role": "assistant", "content": output})
            with st.expander(questions[q]):
                st.write(output)
                # st.button("Export " + q + " to Data Marketplace")


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
                 'SQL table': 'create a SQL table based on the above data in proper code format, breaking it into several tables with primary keys.',
                 'Data Model': 'Can you show the data model in tabular format if we create several SQL tables based on this data with primary key relationships in details'}

    # for the above table -> the input to the 'get SQL code'

    if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
        for q in questions:
            prompt = "\n".join([message["content"]
                                for message in conversation_history])
            prompt += '\n' + questions[q]

            print(prompt)
            output = generate_response(
                metatag_system_prompt, prompt, model)
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


if __name__ == "__main__":
    main()
