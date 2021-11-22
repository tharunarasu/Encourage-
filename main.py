import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

#my_secret = os.environ['TOKEN']
BOT_token="OTA4MzgzMjU0NDA5Nzk3NzI0.YY071A.lrehy213jyYAOMwth6QAAJaSPfs"
client=discord.Client()

sad_words=["depressed","miserable","unhappy","depressing","unfit",
"demotivated","angry","sad","bitter","dismal","heartbroken","broken"]
starter_encouragements=["Don’t stress. You got this!","This is tough, but you’re tougher.","It takes serious courage to get on this path and stay on it. Good for you!","Cheer up Lad"," This totally sucks, but you totally don’t suck!","Don’t be afraid to try. Be afraid to fail"," Don’t try to be perfect. Just try to be better than you were yesterday."," You have my full support, no matter what you do."," You are in charge of your own happiness.","Keep fighting!"," Come on! You can do it!."]

if "responding" not  in db.keys():
  db["responding"]= True


def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + "-" + json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]= encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  msg=message.content
  if message.content.startswith('inspire'):
    quote=get_quote()
    await message.channel.send(quote)
  #if db["responding"]:
    #options=starter_encouragements
    #if "encouragements" in db.keys():
      #options=options + db["encouragements"]
    
  if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
  
  if msg.startswith("new"):
    encouraging_message=msg.split("new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")
  
  if msg.startswith("del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("del",1)[1])
      delete_encouragements[index]
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  if msg.startswith("responding"):
    value=msg.split("responding ",1)[1]

    if value.lower()=="true":
      db["responding"]= True
      await message.channel.send("Respomding on")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off")
  
keep_alive()

client.run(BOT_token)


