# Deployment:
# - change DOSUG_BOT_URL to "https://api.telegram.org/bot636977773:AAGLkv15VZalYNL7WWu4IRVvPb_Xakz79Zo"
# - change SLACK_DOSUG_URL to "https://hooks.slack.com/services/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"
# - uncomment "from botocore.vendored import requests"

import json
import os
import sys
import logging
import random

log = logging.getLogger()

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../"))
sys.path.append(os.path.join(here, "../vendored"))

import requests
#from botocore.vendored import requests

DOSUG_BOT_URL = "https://api.telegram.org/bot652834148:AAG8oRWknsoIDZGIJ7fcWP-KfFvSCFUzHYk" 
SLACK_DOSUG_URL = "https://hooks.slack.com/services/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"
SLACK_ANTON_URL = "https://hooks.slack.com/services/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"
SLACK_POKUPKI_URL = "https://hooks.slack.com/services/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"

MIN_MESSAGE_LENGTH = 50

def lambda_handler(event, context):
    try:

        log.critical("Received event {}".format(json.dumps(event)))
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        if message == "/start":
            postSlackMessage(SLACK_ANTON_URL, 
                "Message from "
                + str(data["message"]["chat"]["username"]) + " (" + str(chat_id) 
                + "): '" + message[0:MIN_MESSAGE_LENGTH] + "'.")

        sendBotOKResponse(first_name, message, chat_id)

        postSlackResponse(message, chat_id)

    except Exception as e:
        print(e)

    return {"statusCode": 200}

def postSlackResponse(message, chat_id):
    
    if message == "/start" or message == "ping" or  len(message) < MIN_MESSAGE_LENGTH:
        return

    postSlackMessage(SLACK_DOSUG_URL, message)

def postSlackMessage(url, message):
   
    data = {"text": message}
    requests.post(url, json.dumps(data))

def sendBotTooShortResponse(chat_id):

    responses = [
        "Можно чуточку подробнее?",
        "Хм.. давай добавим какой-то комментарий в это сообщение?",
        "Я не могу переправить сообщение длинной меньше " + str(MIN_MESSAGE_LENGTH) + " символов! Антон будет недоволен!",
        "Я не могу переправить сообщение длинной меньше "+ str(MIN_MESSAGE_LENGTH) + " символов! Люди меня не поймут!"]

    sendBotMessage(random.choice(responses), chat_id)

def sendBotOKResponse(first_name, message, chat_id):

    if message == "/start":
         sendBotMessage("Привет, {}!\n".format(first_name) +
         "Я отправляю любые сообщения длиннее " + str(MIN_MESSAGE_LENGTH) + " символов в канал 'досуг' в Slack.\n" +
         #"А также могу создавать добавить покупку в список покупок. Для этого напиши 'купить <что купить>'\n" +
         "Но вобще мне просто хочется с кем-то поболтать...", chat_id)
         return

    if len(message) > MIN_MESSAGE_LENGTH - 10 and len(message) < MIN_MESSAGE_LENGTH:
        sendBotTooShortResponse(chat_id)
        return

    responses_сhat = ["I Love You, {}".format(first_name),
        "Продолжай...",
        "C тобой так интересно болтать 😘"
        "Missing you...",
        "Я Люблю Тебя! ♥",
        "Мне просто хочется съесть тебя!!!",
        "😂",
        "😜",
        "Te Amo ♥",
        "А что ты делаешь на выходных?",
        "Что нового?",
        "Соскучился по тебе",
        "Чем займемся?",
        "Ты слишком много болтаешь, пора переходить к делу",
        "Скажу честно, я от тебя устал",
        "Ты разбиваешь мне сердце",
        "Какие планы на вечер?",
        "Скучаю..."]

    responses_dosug = ["Это по-настоящему интересно!",
        "Прикольная идея!",
        "Мне нравится, но предсказать реакцию сообщества сложно...",
        "👍🏻",
        "😳",
        "😍",
        "Может ты уже начинешь слать сообщения напрямую в Slack??",
        "Мы должны это увидеть!",
        "Хмм... ну если ты настаиваешь..."]

    responses = responses_dosug
    if len(message) < MIN_MESSAGE_LENGTH:
        responses = responses_сhat

    sendBotMessage(random.choice(responses), chat_id)

def sendBotMessage(message, chat_id):

    data = { "text": message.encode("utf8"), "chat_id": chat_id }
    url = DOSUG_BOT_URL + "/sendMessage"
    
    #json.dumps(data) ?
    requests.post(url, data)

######################## NOT INCLUDE ON DEPLYMENT BELOW ###################################

test_sample = {
  "resource": "/teleslack2",
  "path": "/teleslack2",
  "httpMethod": "POST",
  "headers": {
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/json",
    "Host": "vdd557qjo9.execute-api.us-east-2.amazonaws.com",
    "X-Amzn-Trace-Id": "Root=1-5b60834f-a987709772f0c4c55007ac74",
    "X-Forwarded-For": "149.154.167.212",
    "X-Forwarded-Port": "443",
    "X-Forwarded-Proto": "https"
  },
  #"queryStringParameters": null,
  #"pathParameters": null,
  #"stageVariables": null,
  "requestContext": {
    "resourceId": "v7grwy",
    "resourcePath": "/teleslack2",
    "httpMethod": "POST",
    "extendedRequestId": "K5l0XGCHCYcFjqw=",
    "requestTime": "31/Jul/2018:15:42:07 +0000",
    "path": "/default/teleslack2",
    "accountId": "048216035384",
    "protocol": "HTTP/1.1",
    "stage": "default",
    "requestTimeEpoch": 1533051727152,
    "requestId": "47b2634a-94d8-11e8-b19e-bd53dcaec9b9",
    "identity": {
   #   "cognitoIdentityPoolId": null,
    #  "accountId": null,
    #  "cognitoIdentityId": null,
    #  "caller": null,
      "sourceIp": "149.154.167.212",
    #  "accessKey": null,
     # "cognitoAuthenticationType": null,
     # "cognitoAuthenticationProvider": null,
     # "userArn": null,
     # "userAgent": null,
     # "user": null
    },
    "apiId": "vdd557qjo9"
  },
  "body": "{\"update_id\":327611454,\n\"message\":{\"message_id\":10,\"from\":{\"id\":124424632,\"is_bot\":false,\"first_name\":\"Anton\",\"last_name\":\"T\\ud83c\\udfb6\",\"username\":\"ant0nt\",\"language_code\":\"en-US\"},\"chat\":{\"id\":124424632,\"first_name\":\"Anton\",\"last_name\":\"T\\ud83c\\udfb6\",\"username\":\"ant0nt\",\"type\":\"private\"},\"date\":1533048726,"
  "\"text\":\""
  "ping"
  "\"}}",
  #"isBase64Encoded": false
}

lambda_handler(test_sample, "")