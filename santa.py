from family import *
import smtplib
import random
import yagmail


def generateEmailText(giverName, receiverName):
    body1 = "Hi, " + giverName + "!\n\n"
    body2 = "This is an automated email to inform you that you have been tasked to buy a gift for " + receiverName + "!\n\n"
    body3 = "Please remember:\n1. Keep this information strictly confidential!\n2. Don't drastically exceed the spending limit of $" + str(capAmount)
    body4 = "!\n\nDon't be the one that ruins Chrismas this year!\n\n\n"
    body5 = "Best Wishes!\nYour friendly neighborhood santaBot (aka SkyNet)"
    body = body1 + body2 + body3 + body4 + body5
    return body

def sendEmail(giver, receiver):
    subject = "**TOP Secret** Your 2021 Secret Santa Assignment **Top Secret**"
    content = generateEmailText(giver[0], receiver[0])
    with yagmail.SMTP(serverEmail, serverPass) as yag:
        yag.send(giver[1], subject, content)
    print("Sent assignment to " + giver[0])

def coupleChecker():
    bool = False
    for person in family[:7]:
        if ((person[0], family[family.index(person)+1][0])) in couples:
            bool = True
        if ((family[family.index(person)+1][0], person[0])) in couples:
            bool = True
    if ((family[7][0], family[0][0])) in couples:
        bool = True
    if ((family[0][0], family[7],[0])) in couples:
        bool = True
    return bool


def assignAndSend():
    random.shuffle(family)
    while (coupleChecker() == True):
        print("couple checker failed, randomizing.......")
        random.shuffle(family)
    for person in family[:7]:
        sendEmail(person, family[family.index(person)+1])
        #print(person[0] + " is giving to: " + family[family.index(person)+1][0])

    sendEmail(family[7], family[0])
    #print(family[7][0] + " is giving to: " + family[0][0])
