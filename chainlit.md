# Welcome to gthe virtual patient simulator! 🚀🤖

Hi there, Doctor! 👋 You're going to have a brief talk with a patient who may be possibly diagnosed with congestive heart failure or not.

## Useful Links 🔗

- **Github:** All the programs and documentation is in our github (https://github.com/JorgeBorque/TFG/tree/main)

## Welcome screen

The simulation you are going to take part in consists in adopting the role of a cardiologist in his office. 
You are going to talk to a patient who has or hasn't a congestive heart failure disease and you'll have to diagnose them with it or not.


## Settings explanation  IMPORTANT!! : YOU'LL HAVE TO ACCEPT THE SETTINGS IN ORDER TO CONVERSATION POSSIBLE 

The process is the following: 

- First you'll have to select the options for the simulation which you would desire to try out. The options available are the following:
    - Selecting a model, this is the controller of the patient, you can assign either the gpt-4 one which would require you to enter the key in the key section or a local model which are all the remaining ones. The model loaded by default is the "AI-Growth-Lab_llama-2-7b-clinical-innovation" one and it is also the most interesting one! If you want to try out other local models change it in http://curie.ita.es:7880/ .
    - Select the method to use to get data: As the data for the patient has to be assigned you will pick the medical history from which the patient is going to act like. 
        - charge1Each: The patient will decide whether to have a congestive heart failure or not.
        - chargeFromSpecific: The patient will take a medical history from the directory you choose in the options.
        - chargeSpecificFileICC: The patient will take a random medical history from the congestive heart failure directory.
        - chargeSpecificFileNOICC: The patient will take a random medical history from the not congestive heart failure directory.
    - Select the directory to get data from: Being ICC (Having congestive heart failure) and NOICC (Not having congestive heart failure).
    - Pick the number of samples you want the patient to choose from. From now the best examples come from 1 sample.
    - Key for gpt-4 model
    - Selecting the behaviour you would like the patient to have. It varies depending on the model used (The best patient behaviours com from the gpt-4 model and the AI-Growth-Lab_llama-2-7b-clinical-innovation model)

- After picking the options, you will begin to talk with the patient. Take into account that the first message written has to be "Please present yourself." which will help you to get a brief introduction from the patient.

## Finish the conversation
- When you feel that the conversation has finished, you can restart the program by reloading the page or by selecting new settings in the settings section.


If you're in the middle of the conversation and you want to check out these instructions again please select the readme option on the top side of the screen.
