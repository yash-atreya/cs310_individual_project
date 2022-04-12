from google.cloud import translate
from nltk.tokenize import wordpunct_tokenize

# Language codes: https://cloud.google.com/translate/docs/languages
def parse_text(msg: str):
    res_dict = {}
    res_dict['error'] = False
    res_dict['content'] = ""
    res_dict['errorMsg'] = ""
    try:
        msg = msg.replace("$translate", "")
        print("Removed $translate: {}".format(msg))
        fromIndex = msg.index("$from")
        content = msg[0:fromIndex]
        print("Content: {}".format(content))
        msg = msg.replace(content, "")
        print("Removed content: {}".format(msg))
        tokens = wordpunct_tokenize(msg)
        print("Tokens: {}".format(tokens))
        tokens.remove("$")
        fromLang = "".join(tokens[tokens.index("from") + 1: tokens.index("$")])
        print("From lang: {}".format(fromLang))
        tokens = tokens[tokens.index("$") + 1:]
        print("Tokens: {}".format(tokens))
        toLang = "".join(tokens[tokens.index("to") + 1:])
        print("To lang: {}".format(toLang))
        res_dict['content'] = content
        res_dict['fromLang'] = fromLang
        res_dict['toLang'] = toLang
        return res_dict
    except:
        res_dict['error'] = True
        res_dict['errorMsg'] = "Error parsing text: make sure you are strictly following the format: $translate <content> $from <language code> $to <language code>"
        return res_dict
    






def translate_text(text="Hello, world!", project_id="cs310-chat-bot", from_lang="en-us", to_lang="es"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": from_lang,
                "target_language_code": to_lang,
            }
    )

    translated_text = ""
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))
        translated_text = translated_text + translation.translated_text
    
    return translated_text

