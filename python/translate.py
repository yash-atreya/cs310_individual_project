from operator import index
from google.cloud import translate
from nltk.tokenize import wordpunct_tokenize
from stopwords import stopwords

def parse_text(msg: str):
    # text_tokens = wordpunct_tokenize(msg)
    # tokens_without_sw = [word for word in text_tokens if not word in stopwords]
    # index = tokens_without_sw.index('translate')
    # if(index == len(tokens_without_sw) - 1):
    #     print("No text found to translate, please provide text in this format $translate <text>")
    #     return None
    # full_text = "".join(tokens_without_sw[index + 1:])
    # print("FULL_TEXT {}".format(full_text));
    msg = msg.replace("$translate", "")
    return msg




def translate_text(text="Hello, world!", project_id="cs310-chat-bot"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "en-US",
                "target_language_code": "es",
            }
    )

    translated_text = ""
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))
        translated_text = translated_text + translation.translated_text
    
    return translated_text

translate_text()
