from distutils.log import error
import requests
import os
import json
from nltk.tokenize import wordpunct_tokenize
from stopwords import stopwords

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get('BEARER_TOKEN')

def get_username_from_msg(msg):
    "Parses incoming msg to look for username"
    print("Looking for username in {}".format(msg))
    text_tokens = wordpunct_tokenize(msg)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords]
    index = tokens_without_sw.index('tweets')
    if(index == len(tokens_without_sw) - 1):
        print("No username found, please provide username in this format $tweets <username>")
        return None
    try:
        username = tokens_without_sw[index + 1]
    except:
        print("Error getting username from msg")
        return None
    else:
        return username


def get_user_id(username: str) -> str:
    endpoint = "https://api.twitter.com/2/users/by/username/{}".format(username)
    response = requests.request("GET", endpoint, auth=bearer_oauth)
    if(response.status_code != 200):
        raise Exception("Error getting user_id: {} {}", response.status_code, response.text)
    return response.json()['data']['id']

def create_url(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    
    r.headers["Authorization"] = "Bearer {}".format(bearer_token)
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.url)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweets_by_username(username):
    res_dict = {}
    res_dict['error'] = False
    res_dict['data'] = []
    res_dict['errorMsg'] = ""
    try:
        user_id = get_user_id(username)
    except: 
        res_dict['error'] = True
        res_dict['data'] = None
        res_dict['errorMsg'] = "User does not exist"
        return res_dict
    else:
        url = create_url(user_id)
        params = get_params()
        try: 
            json_response = connect_to_endpoint(url, params)
            print(json.dumps(json_response, indent=4, sort_keys=True))
        except:
            res_dict['error'] = True
            res_dict['data'] = None
            res_dict['errorMsg'] = "Unable to fetch tweets of {}".format(username)
            return res_dict
        else:
            res_dict['error'] = False
            res_dict['data'] = json_response['data'] if json_response['meta']['result_count'] > 0 else None
            res_dict['errorMsg'] = None
            return res_dict

def main():
    user_id = get_user_id("elonmusk")
    url = create_url(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()