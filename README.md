*Instalación del entorno de conda con el fichero yml*: Únicamente hay que instalar conda en nuestro ordenador y crear un entorno de conda con el siguiente comando: conda env create -f condaEnv.yml 

Una vez instalado el entorno, se deben ejecutar los programas desde la carpeta TFG (tener en cuenta que la carpeta de datos "data" debe de estar al mismo nivel que los programas para su acceso adecuado.

Descripción del objetivo:
Se busca representar una cita de un médico con un paciente en la que el médico intenta preguntar al paciente sobre sus síntomas y su estado con respecto a su enfermedad.

La idea es utilizar los dos programas con emociones pero por ahora se mantienen las versiones antiguas sin emociones en el repositorio.

Detalle a tener en cuenta: El mensaje inicial de todos los programas tiene que ser el mismo en todas las ejecuciones y tiene que estar indicado desde el código y no se puede cambiar en el programa ejecutado. El enfoque del mensaje es una presentación del paciente. 

Escenarios disponibles:

- Programas UserA: Escenario en el que sólo existe un agente independiente, que está representando al paciente. El otro usuario participante en la conversación es el usuario real, enfocado para que participe un médico para su entrenamiento ante un caso virtual pero con datos reales.

  Ejecución de estos programas :  
    - chainlit run chainL_UserA.py               - Versión básica del programa
    - chainlit run chainL_UserA_Emotions.py      - Versión con posibilidad de añadir un comportamiento al paciente -- Selección de las emociones en el apartado Emotions de los ajustes del programa.

  Mensaje inicial incluido: "Please present yourself"
  
- Programas UserN: Escenario en el que participan como mínimo dos agentes independientes, que representarán a un paciente y a un médico.

  Ejecución de estos programas :  
    - chainlit run chainL_UserN.py               - Versión básica del programa
    - chainlit run chainL_UserN_Emotions.py      - Versión con posibilidad de añadir un comportamiento al paciente y al médico -- Selección de las emociones del paciente en el apartado EmotionsPat y las emociones del médico en el apartado EmotionsDoct de los ajustes del programa.

  *** Alternativa de uso: Capacidad de añadir a un enfermero en la conversación como puente al comienzo de la conversación entre paciente y médico (No participaría en la parte 'interesante' de la conversación)

  Mensaje inicial incluido sin enfermero/a : "Please present yourself"
  Mensaje inicial incluido con enfermero/a : "Please present yourself to the others and begin the conversation."
  
Modos de uso de los programas - Casos de uso (Apartado DataExtract en las opciones dentro del programa) (Común a los dos escenarios disponibles) :
  - charge1Each: Carga dos conjuntos de datos, uno de la carpeta de ICC y otro de NOICC y encarga al agente paciente que seleccione uno de estos dos aleatoriamente y represente al paciente.
  - chargeFromSpecific: Carga un conjunto de datos de la carpeta que se le indica en el apartado FileToExtractFrom en ajustes del programa.
  - chargeSpecificFileICC: Carga un conjunto de datos específico de la carpeta de datos ICC indicado desde el código, no se puede cambiar desde el programa.
  - chargeSpecificFileNOICC: Carga un conjunto de datos específico de la carpeta de datos NOICC indicado desde el código, no se puede cambiar desde el programa.


Datos utilizados en cada programa:
  - Para programa UserA:
      - Conjunto de datos sum (resúmenes extraídos de los historiales completos) -- Carpeta con sufijo _sum
  - Para programa UserN:
      - Datos de los historiales médicos completos. -- Carpeta sin sufijo
      - Conjunto de datos con únicamente síntomas del paciente extraídos a partir de una consulta a uno de los modelos utilizados a partir del fichero del historial completo. -- Carpeta con sufijo _sympts
      - Conjunto de preguntas resueltas por uno de los modelos utilizados a partir del fichero del historial completo. -- Carpeta con sufijo _ClinicalCase

Es adecuado tener la carpeta data organizada originalmente para tener el punto común de acceso a los datos en cualquier ejecución de todo programa.


Modelos disponibles para su uso (por ahora):

"gpt-4", "AI-Growth-Lab_llama-2-7b-clinical-innovation", "meditron-7b", "TheBloke_meditron-7B-GPTQ", "Kabster_BioMistral-MedicalQA-FT", "meta-llama_Meta-Llama-3-8B"

Todos los modelos menos gpt-4 deben de ser antes cargados en la siguiente dirección: http://curie.ita.es:7880/ 

Para gpt-4 haría falta una clave secreta.

Pruebas de las emociones con todos los modelos locales utilizados POR AHORA:

Prueba con UserA_Emotions -- Emociones en paciente únicamente
Modelos locales con emociones:
meta-llama_Meta-Llama-3-8B -- Mal reconocimiento de la emoción y mala representación
mistralai_Mixtral-8x7B-Instruct-v0.1 -- No se puede probar por límite del almacenamiento
Kabster_BioMistral-MedicalQA-FT -- Lento y respuestas que no tienen nada que ver
TheBloke_meditron-7B-GPTQ -- Parece que puede entenderlas pero no llega a escoger bien la emoción asignada, puede ser que dependa del historial médico / la información recibida -- Se descontrolan las salidas
meditron-7b -- Reconocimiento 50/50, a veces reconoce bien la emoción pero no la desarrolla en todas las respuestas, tienes que buscar específicamente lo que la sensación que le has introducido dice. No muy preciso por como tienes que averiguar la emoción escogida
AI-Growth-Lab_llama-2-7b-clinical-innovation -- Muy buena interpretación de los sentimientos y sus relaciones a otras emociones o sensaciones que siente el paciente. Las emociones "negativas" las representa muy bien y las positivas por ahora también -- Se queda parado en algun momento??? Igual es por el servidor o los datos???
PARECE QUE FUNCIONA TODO IGUAL CON EL Charge1Each


