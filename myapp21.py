# Language detection and translation


import streamlit as st 

from langdetect import detect, detect_langs

from googletrans import Translator, LANGUAGES # A dictionary containing language codes and language names.

import whisper # convert speech to text and detect the voice

from gtts import gTTS # converts text to voice

import tempfile  # is a Python built-in module used to create temporary files.

import os 
import io  # provides tools for working with data in memory.


st.set_page_config(
    page_title= 'NLP Text,voice Detect',
    page_icon= '🎗️',
    layout= 'centered'
)

st.title('Text and Voice detection and Translation')


languages = dict(
    sorted(LANGUAGES.items(), key= lambda x: x[1])
)

st.markdown(""" 
<style>

.stApp {
background : Linear-gradient(#FFE6E9, #CAF1DE, #FFE6E9);
border : solid;
border-color : black;}


h1 {
    color: green;
   
    font-weight: bold;
    font-size : 24px;
}

 label {
        color: #1e293b;
        font-weight : bold;
        font-size : 18px;
    }


 .stButton > button {
        background-color: #6d28d9;
        color: white;
        border-radius: 40px;
        border: solid;
        border-color : black;
        padding: 10px 20px;
        border-width : 1px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: green;
        color: white;
        font-size : 15px;
        
    }


</style>

""", unsafe_allow_html= True)



@st.cache_resource # This is a Streamlit decorator.

# Its purpose is to cache the Whisper model 
# Without caching, Streamlit could reload the model every time the user interacts with the application


# Load a model 

def load_model():

    model = whisper.load_model('base')

    return model 

    # Loads the Whisper base model.
    # Whisper has different model sizes such as:


model = load_model()


# Creating 2 tabs 

tab1, tab2 = st.tabs([
    'Text detect & Translate',
    'Voice detect & Translate'
])

with tab1:
    st.header('Text Detection and Translation')


    text = st.text_area(
        'Enter your text',
        placeholder= 'Type your language here'
    )

    target_language = st.selectbox(
        'Select the translate language',
        list(languages.keys()),
        format_func= lambda x : languages[x].title()
    )

    # Create a translate button 

    if st.button('Detect & translate'):

        if text.strip() == '':
            st.warning('Please enter some text')

        else:

            try:
                detected_language = detect(text)

                translater  = Translator()

                translated = translater.translate(text, dest= target_language)

                st.subheader('Detected language')

                st.write(
                    languages.get(detected_language, detected_language).title()
                )

                # Displaying the translated text 

                st.subheader('Translate Text')

                st.success(translated.text)

            except Exception as e:

                st.error(f'Error : {e}')
                 # If something goes wrong inside try, Python comes here. e contains the error information.


with tab2:

    st.header('Voice detect & Translation')

    st.write(
        'Speak in any language and detect it'
    )

    target_language = st.selectbox(
        'Select the translate language',
        list(languages.keys()),
        format_func=lambda x: languages[x].title(),
        index=list(languages.keys()).index("hi"),
        key="voice_language"
    )

    audio = st.audio_input('Record your voice')

    if st.button('Voice button & Translate'):

        if audio is None:
            st.warning('Please record the audio')

        else:

            try: 
                # creates a tempfile and namedfile creates a temp file name
                with tempfile.NamedTemporaryFile(
                    delete = False, # don't automatically delete file until with block finishes
                    suffix= '.wav' # makes a audio file extension .wav
                ) as file :

                    # Write recorded audio into the file

                    file.write(audio.getvalue())

                    audio_path = file.name # writes that audio data into the temporary file


                    # whisper transcribe 

                    result = model.transcribe(
                        audio_path,
                        fp16 = False
                    )

                    # whisper receives the audio path and converts to 

                    # Extract the text
                    # whisper gives the recognised text in result['text']
                    speech_text = result['text'].strip()

                    # Extracted the detected language

                    detected_language = result['language']

                    # whisper automatically detects the spoken language

                    st.subheader('Recognised Text')

                    st.write(speech_text)

                    # Displaying the detected language 

                    st.subheader('Detected Language ')
                    
                    st.write(
                        languages.get(detected_language, detected_language).title()
                    )

                    # creating a translater

                    translater = Translator()

                    # Translate recognized speech 

                    transltd = translater.translate(speech_text, dest= target_language)

                    st.subheader('Translated text')

                    st.success(transltd.text)


                    # Convert translated text into voice 

                    tts = gTTS(
                        text = transltd.text ,
                        lang = target_language
                    )
                    # lang=target_language tells gTTS which language should be spoken
                    # Create audio in memory 
                    
                    audio_output = io.BytesIO()

                    # Creates an empty audio container in memory.
                    # Instead of saving another physical audio file to your computer,
                    #  we keep the audio in memory.

                    # Write TTS audio into memory 

                    tts.write_to_fp(audio_output)
                    # fp means file pointer
                    # This writes the generated speech into

                    audio_output.seek(0)

                    # Display translated voice heading

                    st.subheader('Translated voice')

                    # Play translated audio

                    st.audio(
                        audio_output,
                        format= 'audio/mp3'
                    )

                    # Delete temporary file 

                    os.remove(audio_path)


            except Exception as e:
                st.error(f'Error : {e}')


            finally:

                # Delete temporary audio file
                if audio_path and os.path.exists(audio_path):
                    try:
                        os.remove(audio_path)
                    except PermissionError:
                        st.warning('Temporary audio file could not be deleted.')
