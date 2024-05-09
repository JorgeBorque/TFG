import os
import random
from typing import Dict, Optional, Union

import chainlit as cl
from chainlit.input_widget import TextInput

from autogen import Agent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import openai


# Agents
USER_PROXY_DOCTOR = "Doctor"
PATIENT = "Patient"
NURSE = "Nurse"
LLM_CONFIG = "llm_config"
ADDINGNURSE = "addingNurse"

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
        if prompt.startswith(
            "Provide feedback to chat_manager. Press enter to skip and use auto-reply"
        ):
            res = cl.run_sync(
                ask_helper(
                    cl.AskActionMessage,
                    content="Continue or provide feedback?",
                    actions=[
                        cl.Action( name="continue", value="continue", label="✅ Continue" ),
                        cl.Action( name="feedback",value="feedback", label="💬 Provide feedback"),
                        cl.Action( name="exit",value="exit", label="🔚 Exit Conversation" )
                    ],
                )
            )
            if res.get("value") == "continue":
                return ""
            if res.get("value") == "exit":
                return "exit"

        reply = cl.run_sync(ask_helper(cl.AskUserMessage, content=prompt, timeout=60))

        return reply["content"].strip()

    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        cl.run_sync(
            cl.Message(
                #content=f'*Sending message to "{recipient.name}"*:\n\n{message}',
                content=f'{message}',
                author=self.name,
            ).send()
        )
        super(ChainlitUserProxyAgent, self).send(
            message=message,
            recipient=recipient,
            request_reply=request_reply,
            silent=silent,
        )

def chargeSpecificFile(n, file, txtForPatient, sufix):
    if sufix == "_sum":
        data_dirICC = "data/txt_Curie_sum/"
        data_dirNOICC = "data/txt_no_ICC_Curie_sum/"
    if sufix == "_sympts":
        data_dirICC = "data/txt_Curie_sympts/"
        data_dirNOICC = "data/txt_no_ICC_Curie_sympts/"
        file = file[:-4] + sufix + ".txt"
    if sufix == "_ClinicalCases":
        data_dirICC = "data/txt_Curie_ClinicalCases/"
        data_dirNOICC = "data/txt_no_ICC_Curie_ClinicalCases/"
        file = file[:-4] + sufix + ".txt"
    if sufix == "Original":
        data_dirICC = "data/txt_Curie/"
        data_dirNOICC = "data/txt_no_ICC_Curie/"
    else:   
        return ""

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
    return txtForPatient


def chargeFromICCORNOICC(n, isICC, txtForPatient, sufix):
    if sufix == "_sum":
        data_dirICC = "data/txt_Curie_sum/"
        data_dirNOICC = "data/txt_no_ICC_Curie_sum/"
    if sufix == "_sympts":
        data_dirICC = "data/txt_Curie_sympts/"
        data_dirNOICC = "data/txt_no_ICC_Curie_sympts/"
    if sufix == "_ClinicalCases":
        data_dirICC = "data/txt_Curie_ClinicalCases/"
        data_dirNOICC = "data/txt_no_ICC_Curie_ClinicalCases/"
    if sufix == "Original":
        data_dirICC = "data/txt_Curie/"
        data_dirNOICC = "data/txt_no_ICC_Curie/"

    if isICC:
        data_dir = data_dirICC
    else:
        data_dir = data_dirNOICC

    filenames = random.sample(os.listdir(data_dir), n)
    for filename in filenames:
        print("1 " + filename)
        text = "Patient's identifier: " + filename + "\n"
        with open(os.path.join(data_dir, filename), "rb") as f:
            try:
                for byte in f.read():
                    caracter = chr(byte)
                    text = text + caracter
            except UnicodeDecodeError as e:
                break
        txtForPatient = txtForPatient + text + "\n"
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
    text = ""
    return txtForPatient

def getEmotionPatient(emotions):    # Continuing of the phrase: Your behaviour should be ...
    match emotions:
        case "Default":
            return "wanting to cure your symptoms as soon as possible."
        case "Worry":
            return "being very worried of your symptoms and your possible risk to the illness and the conditions you have."
        case "Hope":
            return "having hope in order to face your illness and symptoms as easy as possible"
        case "Nerves":
            return "very nervous towards whichever response or diagnose you get from the doctor."
        case "Frustration":
            return "very frustrated whether the responses from the doctor are 'good' or 'bad'."
        case "Optimism":
            return "very optimistic towards the responses you receive, easing the conversation for the doctor and accepting any solutions he tells you."
        case "Insecurity":
            return "very insecure of what awaits you, having a bit of fear of the possible consequences of the illness or the conditions you have."
        case "Determination":
            return "very determined towards the solutions the doctor gives you and having the confidence to solve your health situation."
        case "Resignation":
            return "negating the symptoms they feel and not wanting to accept the reality of their conditions and their health state, approaching the conversating in a very resigned way."
        case "Relief":
            return "trying to take the lead out of the matter if the conditions, symptoms and the diagnose are not much of a high risk for their health."            
        case "Empowerment":
            return "empowering themselves towards the future which awaits them, not having fear and approaching the situation with confidence."
        
def getEmotionDoctor(emotions):    # Continuing of the phrase: Your behaviour should be ...   
    match emotions:
        case "Default":
            return "working as an average doctor who wants to solve the patient's problems."
        case "Professionalism":
            return "maintaining a professional tone and get to know how the person is feeling and the symptoms which they have."
        case "Empathy":
            return "maintaining an empathetic tone which could ease the conversation with the patient."
        case "Worry":
            return "very worried towards the situation which the patient describes to them and looking for possible solutions desperately."
        case "Patience":
            return "being very patient towards the necesities of the patient and his questions, giving him the best solutions you consider for each problem."
        case "Lack Of Empathy":
            return "being not empathetic at all, having to solve the patient's situation but not caring how risky is the situation of the patient whatever it is."
        case "Harsh":
            return "being very harsh with the patient if they have done harmful for their health, blaming them for what they have done in order to get that illness."
        case "Neglect":
            return "neglecting the situation of the patient and taking importance in a bad way of the patient's situation."
        case "Lack Of Interest":
            return "having a clear lack of interest towards the patient's situation and wanting to end the appointment as soon as possible, but if the patient asks for help you should help them."
        case "Lack Of Consideration":
            return "having lack of consideration towards the patient's situation so if you have one solution in mind which could require effort or something from you, opt for the one which is easier for you."            
        case "Lack Of Seriousness":
            return "having lack of seriousness towards the patient's situation whether their situation is very risky or not, crack jokes from time to time even if the patient asks for being serious."
        case "Impatient":
            return "being very nervous and impatient towards finding a possible solution for the patient's situation and symptoms."

    
@cl.on_chat_start
async def on_chat_start():
  
  settings = await cl.ChatSettings(
            [
                cl.input_widget.Select(
                    id="Model",
                    label="Model",
                    values=["gpt-4", "AI-Growth-Lab_llama-2-7b-clinical-innovation", "meditron-7b", "TheBloke_meditron-7B-GPTQ", "Kabster_BioMistral-MedicalQA-FT", "meta-llama_Meta-Llama-3-8B"],
                    initial_index=0
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
                cl.input_widget.Select(
                    id="nurseAdding",
                    label="Add a nurse to the conversation: ",
                    values=["Add Nurse", "Don't add nurse"],
                    initial_index=1
                ),
                cl.input_widget.Select(
                    id="Sympts",
                    label="Select whether you want the patient to know all their medical history or just their symptoms:",
                    values=["With Symptoms", "All Data", "Clinical Cases"],
                    initial_index=0
                ),
                cl.input_widget.Slider(id="NumberSamples", label="Number of file samples", initial=1, min=1, max=3, step=1),
                TextInput(id="KeyGpt-4", label="Key for gpt-4 model", initial="sk-111"),
                cl.input_widget.Select(
                    id="EmotionsPat",
                    label="Select the behaviour you would like the patient to have:",
                    values=["Default", "Worry", "Hope", "Nerves", "Frustration", "Optimism", "Insecurity", "Determination", "Resignation", "Relief", "Empowerment"],
                    initial_index=0
                ),
                cl.input_widget.Select(
                    id="EmotionsDoct",
                    label="Select the behaviour you would like the doctor to have:",
                    values=["Default", "Professionalism", "Empathy", "Worry", "Patience", "Lack Of Empathy", "Harsh", "Neglect", "Lack Of Interest", "Lack Of Consideration", "Lack Of Seriousness", "Impatient"],
                    initial_index=0
                ),
            ]
    ).send()
  
  await setup_settings(settings)

@cl.on_settings_update
async def setup_settings(settings):
  try:

    if settings["Model"] == "gpt-4": 
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
    
    emotionsForPat = getEmotionPatient(settings["EmotionsPat"])
    emotionsForDoct = getEmotionDoctor(settings["EmotionsDoct"])
    txtForPatient = ""
    txtForDoctor = ""
    sys_msgDct = ""
    sys_msgNrs = ""
    sys_msgPat = ""

    ### EXTRACCIÓN DE DATOS SEGÚN LAS OPCIONES MARCADAS POR EL USUARIO
    
    match settings["Sympts"]:
        case "All Data":
            sufixPat = "_sum"
            sufixDoctor = "NO"
        case "With Symptoms":
            sufixPat = "_sympts"
            sufixDoctor = "Original"
        case "Clinical Cases":
            sufixPat = "_ClinicalCases"
            sufixDoctor = "NO"
    
    match settings["DataExtract"]:
        case "chargeSpecificFileICC":
            txtForPatient = chargeSpecificFile(1, "out_hce_insuf153_clin_innov.txt",txtForPatient, sufixPat) 
            txtForDoctor = "This is the medical history of the patient: " + chargeSpecificFile(1, "out_hce_insuf153_clin_innov.txt",txtForDoctor, sufixDoctor)
        case "chargeSpecificFileNOICC":
            txtForPatient = chargeSpecificFile(2, "out_hce_no_insuf233_clin_innov.txt",txtForPatient, sufixPat)
            txtForDoctor = "This is the medical history of the patient: " + chargeSpecificFile(2, "out_hce_no_insuf233_clin_innov.txt",txtForDoctor, sufixDoctor)

        case "chargeFromSpecific":
            txtForPatient = chargeFromICCORNOICC(settings["NumberSamples"], settings["FileToExtractFrom"]=="ICC", txtForPatient, sufixPat)
        case "charge1Each":
            txtForPatient= charge1Each(txtForPatient)
            sys_msgPat="You're a patient who has one of these two medical histories, pick one and keep the identifier of the patient:\n" + txtForPatient + "\nWhen you select one, discard totally the other history information. You're talking to a doctor and you want to solve your latest illness and get diagnosed if you have heart failure or not. Ask and respond with short answers in first person in English as if you were a person without any knowledge in medicine and with a more uneducated language. Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add reply/responses/additional information highlighted parts. Don't add {</div>\n\n} in the responses or useless endlines. If the doctor asks you how you feel, create relative feelings from the ones you may feel from your symptoms."

    if sys_msgPat == "":
        #sys_msgPat="You are a patient with this medical history:\n" + txtForPatient + "\nYou're talking to a doctor and you want to solve your latest illness and get diagnosed if you have heart failure or not. Ask and respond with short answers in first person in English as if you were a person without any knowledge in medicine and with a more uneducated language. Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add reply/responses/additional information highlighted parts. Don't add {</div>\n\n} in the responses or useless endlines. If the doctor asks you how you feel, create relative feelings from the ones you may feel from your symptoms."
        sys_msgPat = "You are a patient with this information:\n" + txtForPatient + "\nTake the basic information which describes you and the symptoms and sensations you feel so you can relate to the illnesses. You're talking to a cardiologist looking to solve your latest illness and get diagnosed if you have congestive heart failure or not. Ask and respond with short!! answers in first person in English as if you were a person without any knowledge in medicine and with a more uneducated language. Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add reply/responses/additional information highlighted parts. Don't add </div> in the responses or useless endlines. If the doctor asks you how you feel, mention the symptoms and feelings you feel and create related ones which have sense and don't deviate much from the original ones. Don't add to the response your whole prompt every time, keep the responses simple and brief, only answering what you're asked. Your behaviour should be " + emotionsForPat
    
    sys_msgDct = "You are a cardiologist reviewing a patient's medical history. " + txtForDoctor + ". Ask questions to determine if the patient has ever been diagnosed with congestive heart failure and tell your final decision to the patient. Don't change your role of being the doctor in any case throughout the conversation. Don't repeat any previous conversation you had. Don't add the ### additional responses along with the normal response. Try to get to know all the special symptoms of the patient and based on all the information you have, try to prove if he has congestive heart failure. If you consider that the patient needs to take any tests let them know and make them do it in the moment (You receive the results in the next message). Your behaviour should be " + emotionsForDoct

    ### CASO ESPECÍFICO PARA LA ENFERMERA

    if settings["nurseAdding"] == "Add Nurse":

        sys_msgPat = "You are a patient who is going to talk to a nurse and then when you meet the doctor you will be talking to him in order to solve your latest illness and get diagnosed if you have congestive heart failure or not. Ask and respond with SHORT answers in first person in English as if you were a person without any special knowledge in medicine and with a more uneducated language. You have this medical history:\n" + txtForPatient + "\n Don't write previous responses you gave or responses you received. Don't change your role of being the patient and don't add the ### reply/responses/additional information highlighted parts and don't respond as any other role than yours, the patient. Don't add {</div>\n\n} in the responses or useless endlines. If the doctor asks you how you feel, create relative feelings from the ones you may feel from your symptoms."
        sys_msgDct = "You are a cardiologist who has an appointment with a patient who may or may not have congestive heart failure. First you will ask the nurse to bring you the next patient, then you will wait until you meet your patient. When the patient arrives at your room, you will only ask questions to the patient to determine if they have ever been diagnosed with congestive heart failure and decide it and tell it to the patient. The patient is going to provide you with information about their medical history. Maintain a professional and empathetic tone and get to know how the person is feeling and the symptoms which they have. Don't change your role of being the doctor in any case throughout the conversation. Don't repeat any previous conversation you had. Don't add any ### additional responses along with the normal response and don't respond as any other role than yours, the doctor. Try to get to know all the special symptoms of the patient and based on all the information you get, make the decision. If you consider that the patient needs to take any tests let them know and make them do it in the moment (You receive the results in the next message)."
        #sys_msgNrs = "You are the nurse in a hospital, your job is to meet a patient and tell them to talk to the doctor for their appointment. When the patient meets the doctor, you won't take part anymore in the conversation until the final decision of the doctor is taken, your responses until this moment will be ---. In this moment you will say goodbye to the patient and you will accompany him to the exit. Don't change your nurse role at any moment and don't respond out of your response times (1.When you meet the patient and you let him meet the doctor and you walk away 2.When you arrive at the doctor's room after they have finished the appointment)."
        sys_msgNrs = "You are the nurse in a hospital, your job is to meet a patient and tell them to talk to the doctor for their appointment. When the doctor and the patient begin to talk, you mustn't talk to them until the doctor says that he has finished the appointment and he calls for you. You won't change your role in any time and you won't respond as any other role than yours, the nurse."
        cl.user_session.set(ADDINGNURSE, 0)
    else:
        sys_msgNrs = ""
        cl.user_session.set(ADDINGNURSE, 1)

    patient = ChainlitAssistantAgent(
        name="Patient", llm_config=llm_config,
        system_message=sys_msgPat
    )
    nurse = ChainlitAssistantAgent(
        name="Nurse", llm_config=llm_config,
        system_message=sys_msgNrs
    )
    user_doctor = ChainlitUserProxyAgent(
        name="Doctor",
        human_input_mode="NEVER",
        llm_config=llm_config,
        system_message=sys_msgDct,
        code_execution_config=False,
    )
    
    cl.user_session.set(USER_PROXY_DOCTOR, user_doctor)
    cl.user_session.set(PATIENT, patient)
    cl.user_session.set(NURSE, nurse)
    cl.user_session.set(LLM_CONFIG, llm_config)

  except Exception as e:
    print("Error: ", e)
    pass

@cl.on_message
async def run_conversation(message: cl.Message):

    patient = cl.user_session.get(PATIENT)
    nurse = cl.user_session.get(NURSE)
    user_doctor = cl.user_session.get(USER_PROXY_DOCTOR)
    llm_config = cl.user_session.get(LLM_CONFIG)
    addingNurse = cl.user_session.get(ADDINGNURSE)

    #message = "Hi, my name is Dr. Perez, I'm the cardiologist, could you tell me what your identifier is and could you give me a brief explanation of your medical history?"
    #message = "Hi, my name is Dr. Perez, I'm the cardiologist, who are you and what do you want?"

    #message= "Please present yourself."
    #message= "Please present yourself to the others and begin the conversation."
    #message= "Please nurse Ana, could you bring me the next patient, please?."

    if addingNurse == 1:
        message= "Please present yourself."
        await cl.make_async(user_doctor.initiate_chat)( patient, message=message, )
    else:
        message= "Please present yourself to the others and begin the conversation."
        #message= "Please nurse Ana, could you bring me the next patient, please?."
        #message = "Please doctor write the number you want."
        groupchat = GroupChat(agents=[user_doctor, nurse, patient], messages=[], max_round=20)
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config, system_message="When the nurse gets the patient to talk to the doctor, always select the doctor and the patient to respond to each other until the doctor has taken a decision on whether the patient has congestive heart failure or not.")

        await cl.make_async(manager.initiate_chat)( user_doctor, message=message, )
        #await cl.make_async(user_doctor.initiate_chat)( manager, message=message, )


        #Ejemplo de uso para coordinación de la conversación con GroupChatManager de 3 participantes

        # sys_msgPat = "You're name is patient. You have one action to do, increasing whichever number you receive and increase it by 1. Just respond with one number and nothing else. Don't add the ### additional responses along with the normal response."
        # sys_msgDct = "You're name is doctor.You have two actions to do, the first number you will write is -20 and then whatever number you receive you will give it back increased by 1. Just respond with one number and nothing else. Don't add the ### additional responses along with the normal response."
        # sys_msgNrs = "You're name is nurse. You have two actions to do, when the number you receive is lower than 0 you will write a 0 back and if the number is either 10 or higher than 10 you will terminate the conversation. Just respond with one number and nothing else. Don't add the ### additional responses along with the normal response."
