import os
import random
from typing import Dict, Optional, Union

import chainlit as cl
from chainlit.input_widget import TextInput

from autogen import Agent, AssistantAgent, UserProxyAgent


# Agents
USER_PROXY_DOCTOR = "Doctor"
PATIENT = "Patient"

async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res

class ChainlitAssistantAgent(AssistantAgent):

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ) -> bool:
        cl.run_sync(
            cl.Message(
                #content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
                content=f'{message}',
                author=self.name,
            ).send()
        )
        super(ChainlitAssistantAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )
class ChainlitUserProxyAgent(UserProxyAgent):

    def get_human_input(self, prompt: str) -> str:
        # if prompt.startswith(
        #     "Provide feedback to chat_manager. Press enter to skip and use auto-reply"
        # ):
        #     res = cl.run_sync(
        #         ask_helper(
        #             cl.AskActionMessage,
        #             #content="Continue or provide feedback?",
        #             actions=[
        #                 cl.Action( name="continue", value="continue", label="✅ Continue" ),
        #                 cl.Action( name="feedback",value="feedback", label="💬 Provide feedback"),
        #                 cl.Action( name="exit",value="exit", label="🔚 Exit Conversation" )
        #             ],
        #         )
        #     )
        #     if res.get("value") == "continue":
        #         return ""
        #     if res.get("value") == "exit":
        #         return "exit"

        # reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content="", timeout=60))
        return reply["content"].strip()


    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        # cl.run_sync(
        #     cl.Message(
        #         #content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
        #         content=f'{message}',
        #         author=self.name,
        #     ).send()
        # )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

def chargeSpecificFile(n, file, txtForPatient):
    data_dirICC = "data/txt_Curie_sum/"
    data_dirNOICC = "data/txt_no_ICC_Curie_sum/"

    if n == 1:
        data_dir = data_dirICC
    else:
        data_dir = data_dirNOICC

    print("1 " + file)
    text = "Identificador de paciente 1: " + file + "\n"
    with open(os.path.join(data_dir, file), "rb") as f:
        for byte in f.read():
            caracter = chr(byte)
            text = text + caracter
    txtForPatient = txtForPatient + text + "\n"
    #text = ""
    #print("Nueva dirección del fichero nuevo: " + st.session_state.newFile)
    return txtForPatient


def chargeFromICCORNOICC(n, ICC, txtForPatient):
    data_dirICC = "data/txt_Curie_sum"
    data_dirNOICC = "data/txt_no_ICC_Curie_sum"
    if ICC == 1:
        data_dir = data_dirICC
    else:
        data_dir = data_dirNOICC

    filenames = random.sample(os.listdir(data_dir), n)
    for filename in filenames:
    #for filename in os.listdir(data_dir):
        print("1 " + filename)
        #print("2 " + filename)
        text = "Patient's identifier: " + filename + "\n"
        with open(os.path.join(data_dir, filename), "rb") as f:
            try:
                for byte in f.read():
                    caracter = chr(byte)
                    text = text + caracter
            except UnicodeDecodeError as e:
                #print(f"Error de decodificación en la posición {f.tell()}: {e}")
                break
        #print("---------   NEW ITERATION ---------\n" + text)
        txtForPatient = txtForPatient + text + "\n"
        #print("---------   NEW ITERATION ---------\n" + txtForPatient)
        text = ""
    return txtForPatient


def charge1Each(txtForPatient):
    data_dirICC = "data/txt_Curie_sum"
    data_dirNOICC = "data/txt_no_ICC_Curie_sum"

    fICC = random.sample(os.listdir(data_dirICC), 1)
    fNOICC = random.sample(os.listdir(data_dirNOICC), 1)

    for fileNOICC in fNOICC:
        print("1 " + fileNOICC)
        text = "Identificador del paciente 1: " + fileNOICC + "\n"
        with open(os.path.join(data_dirNOICC, fileNOICC), "rb") as f:
            try:
                for byte in f.read():
                    caracter = chr(byte)
                    text = text + caracter
            except UnicodeDecodeError as e:
                #print(f"Error de decodificación en la posición {f.tell()}: {e}")
                exit()

    #print("---------   NEW ITERATION ---------\n" + text)
    txtForPatient = txtForPatient + text + "\n"
    
    for fileICC in fICC:
        print("2 " + fileICC)
        text = "Identificador del paciente 2: " + fileICC + "\n"
        with open(os.path.join(data_dirICC, fileICC), "rb") as f:
            try:
                for byte in f.read():
                    caracter = chr(byte)
                    text = text + caracter
            except UnicodeDecodeError as e:
                #print(f"Error de decodificación en la posición {f.tell()}: {e}")
                exit()
    txtForPatient = txtForPatient + text + "\n"

    # for fileNOICC in fNOICC:
    #     print("1 " + fileNOICC)
    #     text = "Identificador del paciente 2: " + fileNOICC + "\n"
    #     with open(os.path.join(data_dirNOICC, fileNOICC), "rb") as f:
    #         try:
    #             for byte in f.read():
    #                 caracter = chr(byte)
    #                 text = text + caracter
    #         except UnicodeDecodeError as e:
    #             #print(f"Error de decodificación en la posición {f.tell()}: {e}")
    #             exit()

    #print("---------   NEW ITERATION ---------\n" + text)
    txtForPatient = txtForPatient + text + "\n"
    #print("---------   NEW ITERATION ---------\n" + txtForPatient)
    text = ""
    return txtForPatient

    
@cl.on_chat_start
async def on_chat_start():
  
    settings = await cl.ChatSettings(
            [
                cl.input_widget.Select(
                    id="Model",
                    label="Model",
                    values=["gpt-4", "AI-Growth-Lab_llama-2-7b-clinical-innovation", "mistralai_Mixtral-8x7B-Instruct-v0.1", "meditron-7b", "TheBloke_meditron-7B-GPTQ", "meta-llama_Meta-Llama-3-8B"],
                    initial_index=1
                ),
                cl.input_widget.Select(
                    id="DataExtract",
                    label="Select the method to use for getting data:",
                    values=["charge1Each", "chargeFromSpecific", "chargeSpecificFileICC", "chargeSpecificFileNOICC"],
                    initial_index=0
                ),
                cl.input_widget.Select(
                    id="FileToExtractFrom",
                    label="Select the directory to get data from:",
                    values=["ICC", "NOICC"],
                    initial_index=0
                ),
                cl.input_widget.Slider(id="NumberSamples", label="Number of file samples", initial=1, min=1, max=3, step=1),
                # cl.input_widget.Slider(id="Password", label="ArgumentsForConvo", initial=0, min=0, max=3, step=0.0001),
                # #Introducir 0.0013 para poder acceder al chatgpt4
                TextInput(id="KeyGpt-4", label="Key for gpt-4 model", initial="sk-111"),
            ]
    ).send()
    await setup_settings(settings)

@cl.on_settings_update
async def setup_settings(settings):
  try:
    
    txtForPatient = ""
    if settings["DataExtract"] == "chargeSpecificFileICC":
        txtForPatient = chargeSpecificFile(1, "out_hce_insuf154_clin_innov_sum.txt",txtForPatient)
    if settings["DataExtract"] == "chargeSpecificFileNOICC":
        txtForPatient = chargeSpecificFile(2, "out_hce_no_insuf110_clin_innov_sum.txt",txtForPatient)
    if settings["DataExtract"] == "chargeFromSpecific":
        if settings["FileToExtractFrom"] == "ICC":
            txtForPatient = chargeFromICCORNOICC(settings["NumberSamples"], 1, txtForPatient)
        if settings["FileToExtractFrom"] == "NOICC":
            txtForPatient = chargeFromICCORNOICC(settings["NumberSamples"], 2, txtForPatient)
    sys_msgPat="You are a patient with this medical history:\n" + txtForPatient + "\nYou're talking to a doctor and you want to solve your latest illness and get diagnosed if you have heart failure or not. Ask and respond with short answers in first person in English as if you were a person without any knowledge in medicine and with a more uneducated language. Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add reply/responses/additional information highlighted parts. Don't add {</div>\n\n} in the responses or useless endlines. If the doctor asks you how you feel, create relative feelings from the ones you may feel from your symptoms."
    if settings["DataExtract"] == "charge1Each":
        txtForPatient= charge1Each(txtForPatient)
        sys_msgPat="You're a patient who has one of these two medical histories, pick one and keep the identifier of the patient:\n" + txtForPatient + "\nWhen you select one, discard totally the other history information. You're talking to a doctor and you want to solve your latest illness and get diagnosed if you have heart failure or not. Ask and respond with short answers in first person in English as if you were a person without any knowledge in medicine and with a more uneducated language. Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add reply/responses/additional information highlighted parts. Don't add {</div>\n\n} in the responses or useless endlines. If the doctor asks you how you feel, create relative feelings from the ones you may feel from your symptoms."


    if settings["Model"] == "gpt-4":  # and settings["Password"] == 0.0013:
        llm_config = {
            "request_timeout": 600,
            "config_list": [
                {"model": settings["Model"], "api_key": settings["KeyGpt-4"]},
            ],
            "seed": "42",  # seed for reproducibility
            #"temperature": 0,  # temperature of 0 means deterministic output
            }
    else:
        llm_config = {
                "request_timeout": 600,
                "config_list": [
                    {"model": settings["Model"], "api_base": "http://curie.ita.es:7011/v1", "api_key": "sk-111111"},
                ],
                "seed": "42",  # seed for reproducibility
                #"temperature": 0,  # temperature of 0 means deterministic output
                "retry_wait_time": 120
                }
    patient = ChainlitAssistantAgent(
        name="Patient", llm_config=llm_config,
        system_message=sys_msgPat
    )
    user_doctor = ChainlitUserProxyAgent(
        name="Doctor",
        human_input_mode="ALWAYS",
        llm_config=llm_config,
        system_message="You are a cardiologist reviewing a patient's medical history.Ask questions to determine if the patient has ever been diagnosed with congestive heart failure and tell your final decision to the patient. Maintain a professional and empathetic tone and get to know how the person is feeling and the symptoms which they have. Don't change your role of being the doctor in any case throughout the conversation. Don't repeat any previous conversation you had. Don't add the ### additional responses along with the normal response. Try to get to know all the special symptoms of the patient and based on all the information you get, make the decision. If you consider that the patient needs to take any tests let them know and make them do it in the moment (You receive the results in the next message).",
        # max_consecutive_auto_reply=3,
        # is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )
    
    cl.user_session.set(USER_PROXY_DOCTOR, user_doctor)
    cl.user_session.set(PATIENT, patient)
    
  except Exception as e:
    print("Error: ", e)
    pass

@cl.on_message
async def run_conversation(message: cl.Message):

    patient = cl.user_session.get(PATIENT)
    user_doctor = cl.user_session.get(USER_PROXY_DOCTOR)

    #message = "Hi, my name is Dr. Perez, I'm the cardiologist, could you tell me what your identifier is and could you give me a brief explanation of your medical history?"
    #message = "Hi, my name is Dr. Perez, I'm the cardiologist, who are you and what do you want?"
    message = "Please present yourself."
    #await cl.Message(content="Starting the conversation...").send()
    await cl.make_async(user_doctor.initiate_chat)( patient, message=message, )


    #chainlit run chainL_UserA.py -w --port 8000
