from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from time import *
app = Flask(name)
greetings = """
היי שלום :)
הגעתם לבוט של אגודת הסטודנטים תל חי !
אוכל לעזור לך בכמה דברים :
למילוי פנייה השב : פנייה או 1.
לטלפון האגודה השב : טלפון או 2.
לפייסבוק האגודה השב : פייסבוק או 3."""

greet = ["היי" ,"שלום","?","??",".","בדיקה","הלו" ]
reqst = ["פנייה","פניה","1"]
telephone = ["2","טלפון","תלפון"]
facebook = ["3","פייסבוק","פיסבוק ","פסבוק"]

@app.route("/")

def hello():
    return "Hello, World!"
@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    if msg in greet:
        resp.message(greetings)
    elif msg in reqst:
        resp.message("אנא מלא את הפנייה בטופס הבא")
        user = request.POST.get('From')
        message = request.POST.get('Body')
        sleep(2.5)
        resp.message(user)
       # resp.message("https://bit.ly/30FDAJT")
    elif msg in telephone:
        resp.message("048181561")
    elif msg in facebook:
        resp.message("https://m.facebook.com/agudatelhai")
    else:
      resp.message(greetings)  
    return str(resp)

if name == "main":
    app.run(debug=True)