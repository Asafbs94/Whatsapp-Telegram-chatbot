from telegram.ext import *
from datetime import datetime
import pickle
import threading
import time
API_KEY = ''
dict = {}
greetings = """
אוכל לעזור לך בכמה דברים :
למילוי פנייה השב : 1.
לטלפון האגודה השב : 2.
לפייסבוק האגודה השב : 3.
למציאת כיתה בקמפוס : 4
"""

message = """ הגעתם לבוט אגודת הסטודנטים תל חי
              כדי להמשיך אנא רשום מאיזה חוג אתה מגיע.
              [לדוגמה : מדעי המחשב]
"""

greet = ["היי" ,"שלום","?","??",".","בדיקה","הלו" ]
reqst = ["פנייה","פניה","1"]
telephone = ["2","טלפון","תלפון"]
facebook = ["3","פייסבוק","פיסבוק ","פסבוק"]
location = ['4' ,'מיקום']
classes = ['צוערים','חינוך גופני','חינוך','מדעי הסביבה','מדעי המחשב' , 'מדעי החי','מדעי המזון','ביוטכנולוגיה','שירותי אנוש','פסיכולוגיה','מזרח אסיה','עבודה סוציאלית','רב תחומי','שלטון מקומי','אחר',]

formsUsers = {}

#print to chat by the level
def forms_online(update, context):
    if(dict[update.message.chat.id]['level'] == 1):
        update.message.reply_text(":) בוא/י נעבור על השלבים לאט ")
        update.message.reply_text(":אנא כתבו את פנייתכם/ן כאן")
    elif(dict[update.message.chat.id]['level'] == 2):
        update.message.reply_text("אנא מלאו שם ושם משפחה")
    elif(dict[update.message.chat.id]['level'] == 3):
        update.message.reply_text("אנא מלאו חוג")
    elif(dict[update.message.chat.id]['level'] == 4):
        update.message.reply_text("באיזו שנה אתם?")
    elif(dict[update.message.chat.id]['level'] == 5):
        update.message.reply_text("מלא מייל:")

#check if 1 minute passed
def minutePassed(oldminute):
    if(oldminute == 0):
        return False
    currentminute = time.gmtime()[4]
    if ((currentminute - oldminute) >= 1) or (oldminute == 59 and currentminute >= 0):
        return True
    else:
        return False

#get the input text from the user and return the information to the main
def sample_responses(input_text , id = ''):
    # response handling "input text" is the user massage
    user_messages = str(input_text)

    if user_messages == "/start":
        if dict[id]['level'] == 0:
            dict[id]['level'] = 1
            return str(dict[id]['name'])+ ' ' + 'שלום'+ '\n' + message
        else:
            dict[id]['level'] = 1
            return str(dict[id]['name'])+ ' ' + 'שלום' + '\n' + '  אני כבר מכיר אותך אתה בטח לומד בחוג :' + '\n' + dict[id]['class'] + '\n' + greetings
        
    elif dict[id]['level'] == 0:
        returnMessage = ""
        if user_messages in classes:
            dict[id]['class'] = str(input_text)
            dict[id]['level']  = 1
            returnMessage = 'תודה על הבחירה נתונך נשמרו במערכת' + '\n' + greetings
        else:
            returnMessage = """חוג זה לא קיים במערכת, אנא נסה שוב או הקלד אחר"""
        return returnMessage
    elif  dict[id]['level'] >1:
        return 1
    elif user_messages in reqst:
        return 1

    elif user_messages in telephone:
        return "048181561"
    elif user_messages in facebook:
        return "https://m.facebook.com/agudatelhai"
    elif user_messages in location:
        return ' תודה על בחירתך ' + '\n' + 'שירות זה יתאפשר בקרוב'
    else:
        return  str(dict[id]['name'])+ ' ' + 'שלום'+ '\n' + greetings


def start_command(update, context):
    update.message.reply_text('היי אני הבוט של תל חי ואני כאן כדי לעזור')


def help_command(update, context):
    update.message.reply_text('אפשר לקבל פרטים כגון: .............')

#get the inforamion about the user from the dict and react to user by the level.
def handle_message(update, context):
    print(dict)
    text = str(update.message.text).lower()
    if not update.message.chat.id in dict.keys():
        dict[update.message.chat.id] = {}
        dict[update.message.chat.id]['name'] = update.message.chat.first_name
        dict[update.message.chat.id]['level'] = 0

    response = sample_responses(text,update.message.chat.id)
    if(response == 1):
        if not update.message.chat.id in formsUsers.keys():
            formsUsers[update.message.chat.id] = []
        if(not minutePassed(dict[update.message.chat.id]['time'])):    
            forms_online(update , context)
        else:
            update.message.reply_text("הזמן שהוקדש למילוי הטופס נגמר נא התחל מחדש.")
            dict[update.message.chat.id]['level'] = 1
            dict[update.message.chat.id]['time'] = 0
            return
        dict[update.message.chat.id]['time'] = time.gmtime()[4]
        if(dict[update.message.chat.id]['level']>1):
            formsUsers[update.message.chat.id].append(update.message.text)
        
        if(dict[update.message.chat.id]['level'] == 6):
            dict[update.message.chat.id]['level'] = 1
            update.message.reply_text("תודה פנייתך התקבלה בהצלחה")
            update.message.reply_text("המידע שמסרת:")
            update.message.reply_text("\n".join(formsUsers[update.message.chat.id]))
            updater.bot.sendMessage(chat_id=272273445, text=":התקבלה פניה חדשה")
            updater.bot.sendMessage(chat_id=272273445, text="\n".join(formsUsers[update.message.chat.id]))
            formsUsers[update.message.chat.id].clear()
        else:
            dict[update.message.chat.id]['level'] += 1

    else:
        
        update.message.reply_text(response)


def error(update, context):
    print(f"caused an error {context.error}")

def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    threading.Thread(target=shutdown).start()

def update_msg():
    pass

#save all the new info to the file
def saveAllDataOnFile():
    writefile = open('users.txt', 'wb')
    pickle.dump(dict, writefile)
    writefile.close()
    print("Log :")

#get all the info from the file
def getAllDataFromFile():
    readfile = open('users.txt', 'rb')
    tmp = pickle.loads(readfile.read())
    readfile.close()
    print("Log :")
    print(dict)
    return tmp

def main():
    print("LIVE")
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("stopBot123456", stop))#string to stop the bot
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    
    print("Bot Stop")

dict = getAllDataFromFile()
updater = Updater(API_KEY, use_context=True)


main()
saveAllDataOnFile()
