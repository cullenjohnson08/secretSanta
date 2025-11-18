from family import *
import smtplib
import random
import yagmail
from time import sleep,strftime


sent = []

familySize = len(family)-1

year = strftime('%Y')

print("Another year, another heap of bugs to circumvent google security")

def generateTestEmail(giverName, receiverName):
    body = "Hi, " + giverName + "!\n\n"
    body += "This is a TEST email to ensure server functionality, if it weren't a test you would be assigned " + receiverName + "!\n\n"
    body += "Thank you for your attention to this matter\n\n  <3 Cullen"
    return body

def generateEmailText(giverName, receiverName):
    body = "Hi, " + giverName + "!\n\n"
    body += "This is an automated email to inform you that you have been tasked to buy a gift for " + receiverName + "!\n\n"
    body += "Please remember:\n1. Keep this information strictly confidential!\n2. Don't drastically exceed the spending limit of $" + str(capAmount)
    body += "!\n\nA list of nifty gift ideas can be found at: (make sure to put in what you want, if you haven't already!)\n" + familyLink + "\n"
    body += "\n\nDon't be the one that ruins Chrismas this year!\n\n\n"
    body += "Best Wishes!\nYour friendly neighborhood santaBot"
    return body

def sendTestEmail(giver, receiver):
    subject = "**TEST** This is your " + year + " TEST Email **TEST**"
    content = generateTestEmail(giver[0], receiver[0])
    with yagmail.SMTP(serverEmail, serverPass) as yag:
        yag.send(giver[1], subject, content)
    sleep(20)
    return receiver[0]

def sendEmail(giver, receiver):
    subject = "**TOP SECRET** Your " + year + " Secret Santa Assignment **TOP SECRET**"
    content = generateEmailText(giver[0], receiver[0])
    with yagmail.SMTP(serverEmail, serverPass) as yag:
        yag.send(giver[1], subject, content)
    sleep(20)
    return receiver[0]

def coupleChecker():
    bool = False
    for person in family[:familySize]:
        if ((person[0], family[family.index(person)+1][0])) in couples:
            bool = True
        elif ((family[family.index(person)+1][0], person[0])) in couples:
            bool = True
    if ((family[familySize][0], family[0][0])) in couples:
        bool = True
    elif ((family[0][0], family[familySize],[0])) in couples:
        bool = True
    return bool


def assignAndSend():
    random.shuffle(family)
    while (coupleChecker() == True):
        print("couple checker failed, randomizing.......")
        print(family)
        random.shuffle(family)
    for person in family[:familySize]:
        sendEmail(person, family[family.index(person)+1])
        sent.append(family[family.index(person)+1][0])

    sendEmail(family[familySize], family[0])
    sent.append(family[0][0])
    random.shuffle(sent)
    print(sent)
    print("Above are those that are getting gifts")

def Test():
    random.shuffle(family)
    while (coupleChecker() == True):
        print("couple checker failed, randomizing.......")
        print(family)
        random.shuffle(family)
    for person in family[:familySize]:
        sendTestEmail(person, family[family.index(person)+1])
        sent.append(family[family.index(person)+1][0])

    sendTestEmail(family[familySize], family[0])
    sent.append(family[0][0])
    random.shuffle(sent)
    print(sent)
    print("Above are those that are getting gifts")
