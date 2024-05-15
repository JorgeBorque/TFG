# Bienvenido al simulador de paciente virtual! 🚀🤖

Buenas, médico 👋 Vas a tener una conversación con un paciente que puede tener una insuficiencia cardíaca o no, tendrás que averiguar si tiene esta enfermedad o no.

## Links del proyecto 🔗

- **Github:** Todos los programas y documentación se encuentran en la siguiente dirección: (https://github.com/JorgeBorque/TFG/tree/main)

## Uso del programa 
  - Primero, debes cumplimentar los ajustes en el icono que se encuentra a mitad de los tres iconos al lado del chat y confirmarlos para que se cree el paciente con el que hablar. (La explicación de los ajustes viene abajo)
  - A continuación podrás empezar a escribirle al paciente, recuerda que el primer mensaje siempre debe de funcionar como introducción.
  - Cuando pienses que la conversación ha acabado, recarga la página o cumplimenta un nuevo conjunto de ajustes y confírmalos para comenzar una nueva simulación
  - Repite este proceso tantas veces como quieras.
 
## Las opciones disponibles son las siguientes:
  - Selecciona el modelo a utilizar, si seleccionas gpt-4 tendrás que rellenar la clave (key). El modelo cargado por defecto es "AI-Growth-Lab_llama-2-7b-clinical-innovation" y si se quiere cambiar hay que hacerlo desde la siguiente dirección: http://curie.ita.es:7880/ .
  - Selecciona el método para extraer los datos del paciente: 
        - charge1Each: El paciente escogerá dos conjuntos de datos médicos, uno con insuficiencia y otro sin y elegirá uno de ellos. 
        - chargeFromSpecific: El paciente escogerá un conjunto de datos de la carpeta que se le indique .
        - chargeSpecificFileICC: El paciente escogerá un conjunto de datos de la carpeta de insuficiencia cardíaca.
        - chargeSpecificFileNOICC: El paciente escogerá un conjunto de datos de la carpeta de los pacientes sin insuficiencia cardíaca.
    - Selecciona el directorio del que escoger los datos
    - Enumera el número de historiales entre los que el paciente elegirá.
    - Clave para el modelo gpt-4
    - Seleccionar el comportamiento del paciente (Se recomienda comprobar el funcionamiento de por defecto). Cabe destacar que los comportamientos del paciente se modifican con respecto al modelo usado.

