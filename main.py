# import streamlit as st
# from io import StringIO
# from prompt import Prompt
from llm_vm.client import Client
from fastapi import FastAPI
# from llm_vm.config import settings
import gradio as gr
import os
from dotenv import load_dotenv

"""st.set_page_config(
    page_title="Doc-string-ify! ",
    page_icon= "🪄",
    layout="centered",
    initial_sidebar_state="expanded",
    #menu_items={
     #   'Get Help': 'https://www.extremelycoolapp.com/help',
      #  'Report a bug': "https://www.extremelycoolapp.com/bug",
       # 'About': "# This is a header. This is an *extremely* cool app!"}
)"""

# Instantiate the client specifying which LLM you want to use
# client = Client(small_model='pythia', big_model='neo')

load_dotenv()
client = Client(big_model="chat_gpt")

"""code_input = str("code_input mu?")
input_method = st.sidebar.radio(
        "Choose a input method",
        ("Paste your code", "Choose your python file")
    )
if input_method == "Paste your code":
    code_input = st.text_area("Your cool code goes here! 🤘")
    # st.write(code_input)
    func_name = st.text_input("Function_name")
    docstring_prompt = Prompt(function_name=func_name, code= code_input)
    docstring_prompt.validate_input_variables()
    docstring = docstring_prompt.format()
    st.write(docstring)
else:
    uploaded_file = st.file_uploader("A python file goes here! ⚡️", type= "py")

    if uploaded_file is not None:
         # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        code_input = stringio.read()
        # st.write(code_input)
        func_name = st.text_input("Function_name")
        # docstring = generate_docstring(source_code=code_input, function_name=
        func_name)
        # st.write(docstring)"""

PROMPT = """\
            Given the function name and source code, generate an docstring, \
                explanation of the function.
            Function Name: {}
            Source Code:
            {}
            The source code with generated docstring and code:
            """
def validate_input_variables(function_name, codebase):
        """Validate that the input variables are correct."""
        if function_name not in codebase:
            raise ValueError(f"{function_name} must be inside the code!")
        

def anarchy_client(func_name, code, PROMPT = PROMPT):

    validate_input_variables(function_name=func_name, codebase=code)
    doc_prompt = PROMPT.format(func_name, code)


    response = client.complete(prompt = doc_prompt,
                               context = "",
                               
                               openai_key=os.getenv("OPENAI_API_KEY"))
    
    return response["completion"]



interface = gr.Interface(fn=anarchy_client,
                inputs=[gr.Textbox(lines=1, placeholder="Enter function_name here..."),
                        gr.Textbox(lines=6, placeholder="Give me the code!!!")],
                outputs=gr.Code())




CUSTOM_PATH = "/gradio"

app = FastAPI()


@app.get("/")
def read_main():
    return "Go to the /gradio!"
    #interface.launch(share = True)


# io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, interface, path=CUSTOM_PATH)


# interface.launch() for llm-vm
