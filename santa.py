from family import *
import smtplib
import random
import yagmail

sent = ["hello"]

def generateEmailText(giverName, receiverName):
    body1 = "Hi, " + giverName + "!\n\n"
    body2 = "This is an automated email to inform you that you have been tasked to buy a gift for " + receiverName + "!\n\n"
    body3 = "Please remember:\n1. Keep this information strictly confidential!\n2. Don't drastically exceed the spending limit of $" + str(capAmount)
    body4 = "!\n\nA list of nifty gift ideas can be found at: (make sure to put in what you want, if you haven't already!)\n" + familyLink + "\n"
    body5 = "\n\nDon't be the one that ruins Chrismas this year!\n\n\n"
    body6 = "Best Wishes!\nYour friendly neighborhood santaBot (aka SkyNet)"
    body = body1 + body2 + body3 + body4 + body5 + body6
    return body

def sendEmail(giver, receiver):
    subject = "**TOP Secret** Your 2022 Secret Santa Assignment **Top Secret**"
    content = generateEmailText(giver[0], receiver[0])
    with yagmail.SMTP(serverEmail, serverPass) as yag:
        yag.send(giver[1], subject, content)
    return receiver[0]

def coupleChecker():
    bool = False
    for person in family[:familySize]:
        if ((person[0], family[family.index(person)+1][0])) in couples:
            bool = True
        if ((family[family.index(person)+1][0], person[0])) in couples:
            bool = True
    if ((family[familySize][0], family[0][0])) in couples:
        bool = True
    if ((family[0][0], family[familySize],[0])) in couples:
        bool = True
    return bool


def assignAndSend():
    random.shuffle(family)
    while (coupleChecker() == True):
        print("couple checker failed, randomizing.......")
        random.shuffle(family)
    for person in family[:familySize]:
        sendEmail(person, family[family.index(person)+1])
        sent.append(family[family.index(person)+1][0])

    sendEmail(family[familySize], family[0])
    sent.append(family[0][0])
    random.shuffle(sent)
    print(sent)
