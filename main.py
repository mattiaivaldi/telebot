#=======START=======#

import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
from PIL import Image
import multipart

# for multiple output
from random import randint

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# fro epoch time conversion
from time import strftime
from datetime import datetime

# ================================

TOKEN = 'YOUR_BOT_TOKEN_HERE'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

array=[['1','2'],['3','4']]#for multiple choice buttons

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)

# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))

class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))
        
        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return
    
        def reply(msg=None, img=None, vid=None, voi=None):
            if msg:#to send message
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': 'true',
                    'reply_markup': json.dumps({'keyboard': array,'one_time_keyboard': True})
                    #'reply_to_message_id': str(message_id),,'one_time_keyboard': True
                    })).read()
            elif img:#to send pictures
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id))
                #('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            elif vid:#to send videos
                resp = multipart.post_multipart(BASE_URL + 'sendVideo', [
                    ('chat_id', str(chat_id))
                #('reply_to_message_id', str(message_id)),
                ], [
                    ('video', 'video.mp4', vid),
                ])
            elif voi:#to send audio as vocal messages
                resp = multipart.post_multipart(BASE_URL + 'sendVoice', [
                    ('chat_id', str(chat_id))
                #('reply_to_message_id', str(message_id)),
                ], [
                    ('voice', 'voice.mp3', voi),
                ])
            elif aud:#to send audio
                 resp = mltipart.post_multipart(BASE_URLS + 'sendAudio', [
                      ('chat_id', str(chat_id))
                 #('reply_to_message_id', str(message_id)),
                 ], [
                      ('audio', 'audio.mp3', aud),
                 ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
    
# ================================ '/' starting commands

        if text.startswith('/'):
            if text.lower() == '/start':
                array=[]
                reply("Hi, I'm your groundbreaking bot! Ask me everything. To start you can take a look to /basic.\n\n[Add explanation]]\n\n*This is a beta version: some comands could not work!*")
                setEnabled(chat_id, True)
            
            if '/basiccomand' in text.lower() or '/listofcomand' in text.lower() or '/basic' in text.lower():
                array=[]
                reply("Here's a list of basic comands:\n\n/comand1 to know [...]].\n/comand2 to know [...].\n\nLet's discover the others! We can also talk in a more friendly way, without the /-starting comands.")
            
            elif text.lower() == '/stop':
                array=[]
                reply("You are turning me off! Please type /start.")
                setEnabled(chat_id, False)
            
            # =============== PROGRAM (all, today, tomorrow, now)
            
            #the bot can be used to display the program of an event
            
            elif text.lower() == '/program':
                array=[]
                reply(img=open('program.jpg').read())
        
            elif text.lower() == '/today':
                array=[]
                if int(datetime.fromtimestamp(int(str(date))).strftime('%H'))==22:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))+1
                    H=0
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                elif int(datetime.fromtimestamp(int(str(date))).strftime('%H'))==23:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))+1
                    H=1
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                else:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))
                    H=int(datetime.fromtimestamp(int(str(date))).strftime('%H'))+2
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                if d>31:
                    reply("Saturday 12 August 2017\n\n*08:00* at /residenceborsellino Breakfast\n\n*09:30* at /campusluigieinaudi Guest Lecture: Tiling the Universe by /francescoprino\n\n*11:00* Coffee Break\n\n*11:30* at /campusluigieinaudi Parallel Session: /parallelA1\n\n*13:30* Lunch\n\n*14:30* at /campusluigieinaudi IAPS Workshop\n\n*16:30* at /campusluigieinaudi Parallel Session: /parallelA2\n\n*18:30* at /campusluigieinaudi Workshop\n\n*20:30* at /residenceolimpia Italian Food Night")
                else:
                    reply(img=open('program.jpg').read())
                    reply("The Conference will start on August 7, 2017. Look at the program!")
    
            elif text.lower() == '/now' or text.lower() == '/tomorrow':
                array=[]
                if int(datetime.fromtimestamp(int(str(date))).strftime('%H'))==22:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))+1
                    H=0
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                elif int(datetime.fromtimestamp(int(str(date))).strftime('%H'))==23:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))+1
                    H=1
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                else:
                    d=int(datetime.fromtimestamp(int(str(date))).strftime('%d'))
                    H=int(datetime.fromtimestamp(int(str(date))).strftime('%H'))+2
                    M=int(datetime.fromtimestamp(int(str(date))).strftime('%M'))
                if d>31:
                    if H<8:
                        reply("Breakfast will be served at 08:00 at /residenceborsellino")
                    elif H==8 or (H==9 and M<30):
                        reply("*Ongoing* Breakfast at /residenceborsellino\n\n_Next_ 09:30 at /campusluigieinaudi Guest Lecture: Tiling the Universe by /francescoprino")
                    elif (H==9 and M>=30) or H==10:
                        reply("*Ongoing* at /campusluigieinaudi Guest Lecture: *Tiling the Universe* by /francescoprino\n\n_Next_ 11:00 Coffee Break")
                    elif H==11 and M<30:
                        reply("*Ongoing* Coffee Break\n\n_Next_ 11:30 at /campusluigieinaudi Parallel Session /parallelA1")
                    elif (H==11 and M>=30) or H==12 or (H==13 and M<30):
                        reply("*Ongoing* at /campusluigieinaudi Parallel Session /parallelA1\n\n_Next_ 13:30 Lunch")
                    elif (H==13 and M>=30) or (H==14 and M<30):
                        reply("*Ongoing* Lunch\n\n_Next_ 14:30 at /campusluigieinaudi IAPS Workshop")
                    elif (H==14 and M>=30) or H==15 or (H==16 and M<30):
                        reply("*Ongoing* at /campusluigieinaudi IAPS Workshop\n\n_Next_ 16:30 at /campusluigieinaudi Parallel Session: /parallelA2")
                    elif (H==16 and M>=30) or H==17 or (H==18 and M<30):
                        reply("*Ongoing* at /campusluigieinaudi Parallel Session: /parallelA2\n\n_Next_ 18:30 at /campusluigieinaudi Workshop")
                    elif (H==18 and M>=30) or H==19 or (H==20 and M<30):
                        reply("*Ongoing* at /campusluigieinaudi Workshop\n\n_Next_ 20:30 at /residenceolimpia Italian Food Night")
                    elif (H==20 and M>=30) or H==21 or H==22 or H==23:
                        reply("*Ongoing* at /residenceolimpia Italian Food Night")
                    else:
                    reply(img=open('program.jpg').read())
                    reply("The Conference will start on August 7, 2017. Look at the program!")
    
            # =============== SINGLE IMAGE
    
            elif '/image' in text.lower():
                array=[]
                reply(img=open('img.jpg').read())

            # =============== VOICE MESSAGE

            elif '/voice' in text.lower():
                array=[]
                reply(voi=open('voice.mp3').read())

            # =============== AUDIO

            elif '/audio' in text.lower():
                array=[]
                reply(aud=open('audio.mp3').read())

            # =============== MULTIPLE CHOICE

            elif text.lower() == '/choice':#you can also ask that the user's message equals the comand
                array = [['CHOICE1'], ['CHOICE2'], ['CHOICE3'], ['CHOICE4']]
                reply("Make your choice!")

            # =============== RANDOM OUTPUT

            elif '/random' in text.lower():
                array=[]
                myoutput = randint(0,3)
                if myoutput == 1:
                    del myoutput
                    reply(img=open('img.jpg').read())
                elif myoutput == 2:
                    del myoutput
                    reply(img=open('img.jpg').read())
                elif myoutput == 3:
                    del myoutput
                    reply(img=open('img.jpg').read())

            # =============== HELP

            elif '/help' in text.lower():
                array=[["The bot does not work!"],["How to use the bot?"],["I said HELP!"]]
                reply("In which way can I be useful to you?")
    
# ================================ NO /

        #you can repeat all the comand without the /-paradigma. For instance you can look for a particular combination of words in the user's message.
            
        elif "give" in text.lower() and "picture" in text.lower():
            array=[]
            reply(img=open('img.jpg').read())

        # =============== HELP

        elif "the bot does not work!" in text.lower():
            array=[]
            reply("There could be an overload problem. Wait few minutes, if the problem persists you can contact /mattiaivaldi.")

        elif "How to use the bot?" == text:
            array=[]
            reply("[how to use the bot]\n\nEnjoy!")

        elif "I said HELP!" == text:
            array=[]
            reply("You can contact the /organizingcommittee at icps2017@ai-sf.it.\n\nFor emergency you can call +39 112.")

        elif "help" == text.lower():
            array=[["The bot does not work!"],["How to use the bot?"],["I said HELP!"]]
            reply("In which way can I be useful to you?")

        elif "help" in text.lower() or "need help" in text.lower():
            array=[["The bot does not work!"],["How to use the bot?"],["I said HELP!"]]
            reply("In which way can I be useful to you?")

        # =============== MISCELLANEA

        elif "whoami" in text.lower():
            array=[]
            reply(str(fr))#returns the username

        else:
            if getEnabled(chat_id):
                reply('')
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)



#====================
