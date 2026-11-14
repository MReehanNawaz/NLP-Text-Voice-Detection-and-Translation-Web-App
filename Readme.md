

             MULTILINGUAL NLP APPLICATION
                       |
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   TEXT INPUT      VOICE INPUT     VOICE INPUT
        ↓              ↓              ↓
  langdetect       WHISPER          WHISPER
        ↓              ↓              ↓
 Translation     Language Detect   Language Detect
        ↓              ↓              ↓
     TEXT          Recognized       Recognized
                     Text             Text
                                      ↓
                                  Translation
                                      ↓
                                    Text
                                      ↓
                                    gTTS
                                      ↓
                                Audio Output 


# Language Detection and Translation

# Language translation is the process of converting a text or speech into particular language 

# We have two tasks

# 1. Language detection
# To detect a language for particular text or data simple python package langdetect is used
# It supports the 55 languages
# af, ar, bg, ca, cs, da, french, urdu, english 

# pip install langdetect
# 
# Second Task is Language Translation
# To translate a text or data from one language to another by usong python built in package google_trans_new
# google_trans_new is a free unlimited package which implementd Google Translate API and it performs language audio detection

# Install google_trans_new
# #  
# pip install googletrans==4.0.0-rc1 


from langdetect import detect, detect_langs

Arb_sent ='بيانات ومهندس ذكاء اصطناعي، ولدي القدرة على تحويل الأفكار الجديدة إلى واقع.'

print('Detected_language : ',detect(Arb_sent))

sentenc1 = 'Today is a very beautiful day and weather is also good'

print('Detect_lang : ', detect(sentenc1))

sen2 = 'నేను ఒక డేటా శాస్త్రవేత్త మరియు ఏఐ ఇంజనీర్‌ని. కొత్త ఆలోచనలను వాస్తవంగా మార్చే సామర్థ్యం నాకు ఉంది.'

print(detect(sen2))

# Audio, Text translation by google_trans_new built in package 


from googletrans import Translator

trans = Translator()

data = 'Today is very beautiful day'

translated = trans.translate(data,  dest='ur')

print(translated) 