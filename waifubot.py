# complete rewrite using pyTelegramBotAPI wrapper

import telebot
import time
import codecs
import json
import os
import re
import random
import yaml
from urllib import request
from io import BytesIO
from PIL import Image
from booru import getImage
from datetime import datetime, timedelta
TOKEN = ''
tb = telebot.TeleBot(TOKEN)
mywaifus = {}
members_harem = {}
admins = ['1212327414','murcielago09z','793104432']
def get_the_waifu(m,twaifu):
    chatid = m.chat.id
    text = m.text
    name = m.from_user.first_name
    msgid = m.message_id
    with open('waifu.yml', 'r') as f:
        waifu = yaml.load(f)
        waifu_text = twaifu
        waifu_title = waifu[waifu_text][0]
    try:
        image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
        with open(image, 'rb') as photo:
            myfile = photo
            myname = waifu_text+' ('+waifu_title+')'
             #waifus.append({"photo":photo,"name":waifu_text+' ('+waifu_title+')'})
             # tb.send_photo(chatid, photo, caption=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
    except OSError:
         try:
            url = getImage(waifu_text.replace(" ", "_"))
            image = Image.open(BytesIO(request.urlopen(url).read()))
            resized = image.resize((423, 586), Image.ANTIALIAS)
            out = BytesIO()
            resized.save(out,'PNG')
            imgfile = 'temp' + str(random.randint(0,100)) + '.png'
            myfile = out.getvalue()
            myname = waifu_text+' ('+waifu_title+')'
         except (AttributeError, PermissionError) as e:
            pass
    return {"file":myfile,"name":myname}
@tb.message_handler(commands=['waifu'])
def waifus(m):
  global mywaifus
  if m.chat.type == 'private':
      tb.send_message(m.chat.id, 'Solo en grupos')
      return
  elif (str(m.from_user.id) in admins or str(m.from_user.username) in admins) or not m.text.startswith('/waifu'):
      chatid = m.chat.id
      text = m.text
      name = m.from_user.first_name
      msgid = m.message_id
      with open('waifu.yml', 'r') as f:
         waifu = yaml.load(f)
         waifu_text = random.choice(list(waifu.keys()))
         waifu_title = waifu[waifu_text][0]
         actual = datetime.now()
         mywaifus[str(chatid)] = {"Waifu":waifu_text,"Anime":waifu_title,"state":"open","time":actual}
         print(name + ": " + waifu_text + " (" + waifu_title + ")")
         try:
             image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
             with open(image, 'rb') as photo:
                 tb.send_chat_action(chatid, 'upload_photo')
                 # tb.send_photo(chatid, photo, caption=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
                 tb.send_photo(chatid,photo,'Nueva waifu aparecida pon */protecc nombre del personaje*',parse_mode='Markdown',reply_to_message_id=msgid)
         except OSError:
             try:
                 url = getImage(waifu_text.replace(" ", "_"))
                 image = Image.open(BytesIO(request.urlopen(url).read()))
                 resized = image.resize((423, 586), Image.ANTIALIAS)
                 out = BytesIO()
                 resized.save(out,'PNG')
                 imgfile = 'temp' + str(random.randint(0,100)) + '.png'
                 f = open(imgfile,'wb')
                 f.write(out.getvalue())
                 f.close()
                 img = open(imgfile, 'rb')
                 tb.send_chat_action(chatid, 'upload_photo')
                 tb.send_photo(chatid,img,'Nueva waifu aparecida pon */protecc nombre del personaje*',parse_mode='Markdown',reply_to_message_id=msgid)
                 #tb.send_photo(chatid, img, caption=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
                 f.close()
                 os.remove(imgfile)
             except (AttributeError, PermissionError) as e:
        #tb.send_message(chatid, text=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
                 pass
@tb.message_handler(commands=['getwaifu'])
def obtenerwaifu(m):
    if str(m.from_user.id) in admins or m.from_user.username in admins:
        if str(m.chat.id) in mywaifus:
            waifu = mywaifus[str(m.chat.id)]
            tb.send_message(m.chat.id,' La waifu es ' + waifu["Waifu"] + ' ('+waifu["Anime"]+ ')')
@tb.message_handler(commands=['stop'])
def stopbot(m):

    if m.from_user.id == 1212327414:
        os.sys.exit()
@tb.message_handler(func=lambda e: e and e.text and not e.text.startswith('/'))
def aparecer(m):
    global mywaifus
    if m.chat.type != 'private':
        chatid = m.chat.id
        if str(chatid) in mywaifus:
             data = mywaifus[str(chatid)]
             waifutime = data["time"]
             state = data["state"]
             ahora = datetime.now()
             ten = timedelta(minutes=10)
             if (ahora > waifutime + ten) and state == "open":
                 tb.send_message(chatid, 'La waifu se ha ido')
                 mywaifus[str(chatid)]["state"] = "huida"
                 mywaifus[str(chatid)]["time"] = ahora
             elif (ahora> waifutime + ten):
                 waifus(m)
        else:
            waifus(m)
@tb.message_handler(func=lambda e: e and e.text and e.text.startswith('/protecc'))
def protecc(m):
  global mywaifus
  if m.chat.type == 'private':
      tb.send_message(m.chat.id, 'Solo en grupos')
      return
  elif str(m.chat.id) in mywaifus:
     msgid = m.message_id
     chatid = m.chat.id
     waifu = mywaifus[str(chatid)]
     mydate = waifu["time"]
     userid = m.from_user.id
     name = waifu["Waifu"]
     anime = waifu["Anime"]
     name_splitted = name.lower().split()
     text = m.text.replace('/protecc ','').lower().split()
     status = waifu["state"]
     actual = datetime.now()
     minutes_to_wait = timedelta(minutes=5)
     correct = False
     if actual<(mydate+minutes_to_wait) and status == "open":
         for x in text:
             if x in name_splitted:
                correct = True
         if correct:
             tb.send_message(chatid, 'has raptado exitosamente a '+ name + '(' + anime + '). ', reply_to_message_id=msgid)
             ahora = datetime.now()
             mywaifus[str(chatid)]["time"] = ahora
             mywaifus[str(chatid)]["state"] = "cazada"
             if str(chatid) in members_harem:
                 if userid in members_harem[str(chatid)]:
                     user = members_harem[str(chatid)][userid]
                     user.append(name+' ('+anime+')')
                 else:
                     tb.send_message(chatid, m.from_user.first_name + ' Ha conseguido su primera waifu')
                     members_harem[str(chatid)][userid] = []
                     members_harem[str(chatid)][userid].append(name+' ('+anime+')')
             else:
                 members_harem[str(chatid)] = {}
                 members_harem[str(chatid)][userid] = [name+' ('+anime+')']
         else:
             tb.send_message(chatid, 'No, esa no es', reply_to_message_id=msgid)
@tb.message_handler(commands=['viewharem'])
def viewharem(m):
    string = "(.*) \((.*)\)"
    global mywaifus
    waifus = []
    chatid = m.chat.id
    msgid = m.message_id
    userid = m.from_user.id
    nombre = m.from_user.first_name
    if str(chatid) in members_harem and userid in members_harem[str(chatid)]:
        waifus = members_harem[str(chatid)][userid]
        lista = []
        a = 1
        for x in waifus:
            captura = re.match(string,x)
            cap = captura.group(1)
            imagen = get_the_waifu(m,cap)
            tb.send_photo(chatid,imagen["file"],str(a)+'. '+imagen["name"],reply_to_message_id=msgid)
            a += 1
    else:
        tb.send_message(chatid,'No tienes waifus :(',reply_to_message_id=msgid)
@tb.message_handler(commands=['harem'])
def myharem(m):
    global mywaifus
    chatid = m.chat.id
    msgid = m.message_id
    userid = m.from_user.id
    nombre = m.from_user.first_name
    if str(chatid) in members_harem and userid in members_harem[str(chatid)]:
        waifus = members_harem[str(chatid)][userid]
        lista = []
        a = 1
        for x in waifus:
            lista.append(str(a)+'. '+x)
            a += 1
        thewaifus = '\n'.join(lista)
        texto = nombre+' Harem:\n'+thewaifus
        tb.send_message(chatid, texto,reply_to_message_id=msgid)
    else:
        tb.send_message(chatid,'No tienes waifus :(',reply_to_message_id=msgid)
@tb.message_handler(commands=['shipgirl'])
def shipgirl(m):
  with open('shipgirl.yml', 'r') as f:
    waifu = yaml.load(f)
    waifu_text = random.choice(list(waifu.keys()))
    waifu_title = waifu[waifu_text][0]
    try:
      image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
      photo = open(image, 'rb')
      tb.send_chat_action(chatid, 'upload_photo')
      tb.send_photo(chatid, photo, caption=name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
    except OSError:
      tb.send_message(chatid, text=name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)

tb.polling(none_stop=True)
while True:
          time.sleep(1)
