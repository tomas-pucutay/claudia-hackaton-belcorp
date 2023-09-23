## ClaudIA

Usa inteligencia artificial basada en GPT-3.5 para buscar el conocimiento disponible en los videos de internet

### Detalles tecnicos
* Langchain / OpenAI
* Chroma (vector store)
* Streamlit

### Como iniciar
* Se necesita python `==3.10`.
* Para obtener el repositorio y crear las dependencias en un entorno virtual
    ```
    git clone [repository-url]
    cd claudia-hackaton-belcorp
    pip install pipenv
    pipenv shell
    pipenv install -r requirements.txt
    ```
* Crear un archivo .env y agregar el token de OpenAI en la variable de entorno `OPENAI_API_KEY` en la forma `OPENAI_API_KEY=<token>
* Levantar el repositorio con
    ```
    streamlit run chatbot.py
    ```

### Embeddings

Este proyecto contiene las transcripciones de múltiples listas de reproducción de videos de Youtube mediante Whisper.
El resultado se encuentra en `ingestion/transcriptions`
Las listas usadas han sido:
- [Herramientas digitales](https://www.youtube.com/playlist?list=PLxF7HdNkCOLQOAOmQsR3I0I76qklNZucW)
- [Lanzamientos](https://www.youtube.com/playlist?list=PLxF7HdNkCOLRCoOL4jTdLWV7nJPHXJyCI)
- [#MinutoAcademico](https://www.youtube.com/playlist?list=PLxF7HdNkCOLTELPKp_nSyEduDJoIbXNG-)
La lógica construida permite agregar más playlist y evaluará que videos aun no ha consumido mediante su ID para ser eficiente en recursos

Se generaron embeddings de estas transcripciones usando OpenAI y Chroma como base de datos de vectores.
Chroma corre localmente con este proyecto, y la base de datos se encuentra en el directorio `db`
La secuencia de pasos para aumentar la base de datos es get_audio, get_transcriptions, save_embeddings de la carpeta ingestion

[Langchain QA docs](https://python.langchain.com/docs/use_cases/question_answering/)


### Frontend - Streamlit
El frontend se ha hecho de una manera estatica, por medio de bloques provistos por Streamlit. Cada vez que se quiere levantar el proyecto o actualizar alguna modificacion, se usa el comando streamlit run chatbot.py.`
