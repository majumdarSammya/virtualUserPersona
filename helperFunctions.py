import streamlit as st
import os
import pandas as pd
import openai

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


# def business(folder, model, metatag_system_prompt, init_prompt):
#     st.title("For Business User")

#     if "data_loaded" not in st.session_state:
#         st.session_state.data_loaded = False
#     if "content_generated" not in st.session_state:
#         st.session_state.content_generated = False


#     conversation_history = []
#     conversation_history.append({"role": "assistant", "content": init_prompt})
#     df = pd.DataFrame()
#     st.sidebar.markdown("----")
#     if st.sidebar.button("Load Dataset") or st.session_state.data_loaded:
#         for filename in os.listdir(folder):
#             if filename.endswith('.csv'):
#                 file_path = os.path.join(folder, filename)
#                 df = pd.read_csv(file_path)
#                 non_null_rows = df.iloc[:5]
#                 st.markdown(f"### Dataset sample: `{filename}`")
#                 st.table(non_null_rows)
#         st.session_state.data_loaded = True

#     st.sidebar.markdown("----")
#     folder = str(Path.cwd()) + str(Path("/HR/TableScripts"))
#     file_name = next((filename for filename in os.listdir(folder) if filename.endswith('.txt')), None)

#     if file_name:
#         file_path = os.path.join(folder, file_name)

#         # Read the text file and store its contents as a string
#         with open(file_path, 'r') as file:
#             text = file.read()
#     query = st.text_input('Input your query')
#     queryButton = st.button("Get SQL code")
#     prompt =   query + f"""\n
#     - only provide a query for the first table.
#     - only provide the SQL code for the query. \n
#     Here is the table: \n
#     {text}
#     """
#     if queryButton or st.session_state.content_generated:
#          st.code(generate_response(metatag_system_prompt, prompt, model), language="sql")


#     questions = {'Summary': 'Give me the summary of the data in one paragraph',
#                  'Use_Case': 'Give me the potential use cases of this data',
#                  'Data_Description': 'Give me only the data description section',
#                  'Sensitive_Info': 'Which attributes contain personal sensitive information?'}

#     storeResponsesBizUser = ""
#     qCountBizUser = 1
#     if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
#         for q in questions:
#             # conversation_history.append({"role": "user", "content": questions[q]})
#             prompt = init_prompt + '\n' + questions[q]
#             print(prompt)
#             output = generate_response(metatag_system_prompt, prompt, model)
#             storeResponsesBizUser += f'Q{qCountBizUser}. ' + \
#                 questions[q] + \
#                 '\n\n' + output + '\n\n\n\n'
#             qCountBizUser += 1
#             # conversation_history.append({"role": "assistant", "content": output})
#             with st.expander(questions[q]):
#                 st.write(output)
#                 # st.button("Export " + q + " to Data Marketplace")
#         st.sidebar.download_button(
#             "Download Responses", data=storeResponsesBizUser)


# def business(folder, model, metatag_system_prompt, init_prompt):
#     st.title("Business View")

#     if "data_loaded" not in st.session_state:
#         st.session_state.data_loaded = False
#     if "content_generated" not in st.session_state:
#         st.session_state.content_generated = False

#     conversation_history = []
#     conversation_history.append({"role": "assistant", "content": init_prompt})

#     st.sidebar.markdown("----")
#     if st.sidebar.button("Load Dataset") or st.session_state.data_loaded:
#         for filename in os.listdir(folder):
#             if filename.endswith('.csv'):
#                 file_path = os.path.join(folder, filename)
#                 df = pd.read_csv(file_path)
#                 non_null_rows = df
#                 st.markdown(f"### Dataset sample: `{filename}`")
#                 st.table(non_null_rows)
#         st.session_state.data_loaded = True

#     st.sidebar.markdown("----")

#     questions = {

#         'Summary': 'Give me the summary of the data in one paragraph',
#         'Use_Case': 'Give me the potential use cases of this data',
#         'Tabular Data': 'Can you show all the column names, their datatypes in SQL format, brief description and PII in a nice tabular format',  # DATA CATALOGUE

#     }

#     storeResponsesBizUser = ""
#     qCountBizUser = 1
#     if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
#         for q in questions:
#             # conversation_history.append({"role": "user", "content": questions[q]})
#             prompt = init_prompt + '\n' + questions[q]
#             print(prompt)
#             output = generate_response(metatag_system_prompt, prompt, model)
#             storeResponsesBizUser += f'Q{qCountBizUser}. ' + \
#                 questions[q] + \
#                 '\n\n' + output + '\n\n\n\n'
#             qCountBizUser += 1
#             # conversation_history.append({"role": "assistant", "content": output})
#             with st.expander(questions[q]):
#                 st.write(output)
#                 # st.button("Export " + q + " to Data Marketplace")
#         st.sidebar.download_button(
#             "Download Responses", data=storeResponsesBizUser)

# REDACTED BUSINESS USER TWO

# def businessUserTwo(folder, model, metatag_system_prompt, init_prompt):
#     st.title("For Business User Two")

#     if "data_loaded" not in st.session_state:
#         st.session_state.data_loaded = False
#     if "content_generated" not in st.session_state:
#         st.session_state.content_generated = False

#     conversation_history = []
#     conversation_history.append({"role": "assistant", "content": init_prompt})

#     st.sidebar.markdown("----")
#     if st.sidebar.button("Load Dataset") or st.session_state.data_loaded:
#         for filename in os.listdir(folder):
#             if filename.endswith('.csv'):
#                 file_path = os.path.join(folder, filename)
#                 df = pd.read_csv(file_path)
#                 non_null_rows = df.iloc[:5]
#                 st.markdown(f"### Dataset sample: `{filename}`")
#                 st.table(non_null_rows)
#         st.session_state.data_loaded = True

#     st.sidebar.markdown("----")

#     questions = {'Summary': 'Give me the summary of the data in one paragraph',
#                  'Use_Case': 'Give me the potential use cases of this data',
#                  'Data_Description': 'Give me only the data description section',
#                  'Sensitive_Info': 'Which attributes contain personal sensitive information?'}

#     storeResponsesBizUserTwo = ""
#     qCountBizUserTwo = 1
#     if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
#         for q in questions:
#             # conversation_history.append({"role": "user", "content": questions[q]})
#             prompt = init_prompt + '\n' + questions[q]
#             print(prompt)
#             output = generate_response(metatag_system_prompt, prompt, model)
#             storeResponsesBizUserTwo += f'Q{qCountBizUserTwo}. ' + \
#                 questions[q] + \
#                 '\n\n' + output + '\n\n\n\n'
#             qCountBizUserTwo += 1
#             # conversation_history.append({"role": "assistant", "content": output})
#             with st.expander(questions[q]):
#                 st.write(output)
#                 # st.button("Export " + q + " to Data Marketplace")
#         st.sidebar.download_button(
#             "Download Responses", data=storeResponsesBizUserTwo)


def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


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

# REDACTED TECHNICAL USER TWO

# def techUserTwo(model, metatag_system_prompt, init_prompt):
#     if "content_generated" not in st.session_state:
#         st.session_state.content_generated = False

#     conversation_history = []
#     # conversation_history.append({"role": "assistant", "content": init_prompt})
#     st.title("For Technical User Two")
#     st.sidebar.markdown("----")

#     st.sidebar.markdown('----')

#     # downloadButton = st.sidebar.download_button("Download Responses")

#     # st.sidebar.markdown('----')

#     uploaded_files = st.sidebar.file_uploader(
#         "Select the source code to interpret", accept_multiple_files=True)

#     for uploaded_file in uploaded_files:
#         code_txt = uploaded_file.getvalue()
#         content = str(uploaded_file.name) + " " + str(code_txt)
#         conversation_history.append({"role": "user", "content": content})
#         st.write("filename:", uploaded_file.name)
#         st.code(code_txt.decode("utf-8"), language='python')

#     st.sidebar.markdown("----")

#     questions = {'Summary': 'give me a brief one paragraph summary of the uploaded data',
#                  'SQL table': 'create a SQL table based on the above data in proper code format, breaking it into several tables with primary keys and foreign keys if necessary.',
#                  'Data Model': 'Can you show the data model in tabular format if we create several SQL tables based on the above data dictionary with primary key relationships in details'}

#     # for the above table -> the input to the 'get SQL code'

#     storeResponsesTechUserTwo = ""
#     qCountTechUserTwo = 1
#     if st.sidebar.button("Generate Contents") or st.session_state.content_generated:
#         for q in questions:
#             prompt = "\n".join([message["content"]
#                                 for message in conversation_history])
#             prompt += '\n' + questions[q]

#             print(prompt)
#             output = generate_response(
#                 metatag_system_prompt, prompt, model)
#             storeResponsesTechUserTwo += f'Q{qCountTechUserTwo}. ' + \
#                 questions[q] + '\n\n' + output + '\n\n\n\n'
#             qCountTechUserTwo += 1
#             with st.expander(questions[q]):
#                 st.write(output)
#                 if q in ['README', 'Code']:
#                     st.button("Download " + q)

#         st.sidebar.download_button(
#             "Download Responses", data=storeResponsesTechUserTwo)


def business(model, metatag_system_prompt, init_prompt):
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    # conversation_history.append({"role": "assistant", "content": init_prompt})
    st.title("Business View")
    st.sidebar.markdown("----")

    uploaded_files = st.sidebar.file_uploader(
        "Select the source code to interpret", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        code_txt = uploaded_file.getvalue()
        content = str(uploaded_file.name) + " " + str(code_txt)
        conversation_history.append({"role": "user", "content": content})
        st.write("filename:", uploaded_file.name)
        st.code(code_txt.decode("utf-8"), language='python')

    st.sidebar.markdown("----")

    # Predefined question set
    questions = {

        'Summary': 'Give me the summary of the data in one paragraph',
        'Use_Case': 'Give me the potential use cases of this data',
        'Tabular Data': 'Can you show all the column names, their datatypes in SQL format, brief description and PII in a nice tabular format',  # DATA CATALOGUE

    }

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
            st.sidebar.download_button(
                "Download Responses", data=storeResponses)


def tech(model, metatag_system_prompt, init_prompt):
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []
    # conversation_history.append({"role": "assistant", "content": init_prompt})
    st.title("Technical View")
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

    # Predefined question set
    questions = {


        'SQL table': 'create a SQL table based on the above data in proper code format, breaking it into several tables with primary keys.',
        'SQL code': 'Provide the SQL code to create tables with the columns in the ACTUAL_COLUMN column in the data splitting the tables with assumed primary and foreign keys',
        # 'Data Model': 'Can you show the data model in tabular format if we create several SQL tables based on this data with primary key relationships in details',
        'Tabular Data': 'Can you show all the column names, their datatypes in SQL format, brief description and PII in a nice tabular format'
    }

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
        st.sidebar.download_button(
            "Download Responses", data=storeResponses)

    if queryButton or st.session_state.content_generated:

        prompt = "\n".join([message["content"]
                           for message in conversation_history])
        prompt += '\n' + query
        with st.expander('SQL code:'):
            st.write(generate_response(metatag_system_prompt, prompt, model))

        st.sidebar.download_button(
            "Download Responses", data=storeResponses)


def customUser(model):
    if "content_generated" not in st.session_state:
        st.session_state.content_generated = False

    conversation_history = []

    st.title("SQL Code Converter")
    # downloadButton = st.sidebar.download_button("Download Responses")
    bytes_data = None
    uploaded_files = st.file_uploader(
        "Upload database tables", accept_multiple_files=True)
    for file in uploaded_files:
        bytes_data = file.read()
        # st.write("filename:", file.name)

    question = st.text_area(
        label="Enter SQL script", key="question", height=100)
    submit = st.button(label='Submit')

    if uploaded_files is not None:
        custom_user_prompt = f"""You are a data assistant. Your task is to do the following: 
                                - You are given two SQL tables created with the following SQL code:
                                        {bytes_data}
                                - Examine the SQL code provided to you: {question}
                                - The provided SQL code makes a query to the first table. You should respond with an equivalent SQL code that does the exact same thing from the second table.
                                - Ask to clarify if you did not understand the question
                                  """
    else:
        pass
    conversation_history.append(
        {"role": "assistant", "content": custom_user_prompt})
    questions = {
        "user_question": question
    }
    if submit or st.session_state.content_generated:
        for q in questions:
            prompt = "\n".join([message["content"]
                                for message in conversation_history])
            prompt += '\n' + questions[q]

            print(prompt)
            output = generate_response(
                custom_user_prompt, prompt, model)
            with st.expander("SQL code:"):
                st.code(output, language='sql')
