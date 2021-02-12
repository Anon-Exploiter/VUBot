from discord.ext import commands
from time import sleep

import requests
import json
import datetime, pytz
import discord

def login(loginEndpoint, username, password):
    response        = requests.post(loginEndpoint,
        headers     = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate"
        },
        data        = {
            "studentid": username,
            "appKey": password,
            "fcm_token": "null",
            "device_id": "123456"
        }
    )

    if response.status_code == 200:
        print("[#] Logged in successfully!\n")

        responseTxt = response.text
        jsonData    = json.loads(responseTxt)
        jsonFields  = jsonData['All'][0]

        NAME        = jsonFields['Name']
        AccessToken = jsonFields['AccessToken']

        return (NAME, AccessToken)

    else:
        print("[!] Login failed!")

def fetchGDB(gdbEndpoint, accessToken):
    response        = requests.post(gdbEndpoint,
        headers     = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate"
        },
        data        = {
            "accessToken": accessToken
        }
    )

    if response.status_code == 200:
        gdbJson     = json.loads(response.text)['All']
        fOutput     = ""

        print("[&] GDBs:\n")
        
        for gdbs in gdbJson[:3]:
            crs     = gdbs['CourseCode']
            sDate   = int(gdbs['StartDate'].replace('/Date(', '').replace(')/', '')[:-3])
            eDate   = int(gdbs['EndDate'].replace('/Date(', '').replace(')/', '')[:-3])

            stDate  = datetime.datetime.fromtimestamp(sDate).strftime('%d-%m-%Y')
            enDate  = datetime.datetime.fromtimestamp(eDate).strftime('%d-%m-%Y')
            dToday  = datetime.datetime.now(pytz.timezone('Asia/Karachi')).strftime("%d-%m-%Y")

            if stDate == dToday:
                stDate += " (today)"

            if enDate == dToday:
                enDate += " (today)"

            fOutput += f"[#] Course: {crs}\nStart Date: {stDate}\nEnd Date: {enDate}\n\n"

        print(fOutput)
        return(fOutput)

    else:
        print("[!] Can't load GDB endpoint..")

def fetchQuizzes(quizEndpoint, accessToken):
    response        = requests.post(quizEndpoint,
        headers     = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate"
        },
        data        = {
            "accessToken": accessToken
        }
    )

    if response.status_code == 200:
        fOutput     = ""
        quizJson    = json.loads(response.text)['All']

        print("[&] Quizzes:\n")
        
        for quizzes in quizJson[:3]:
            crs     = quizzes['courseCode']
            title   = quizzes['Title']
            sDate   = int(quizzes['StartDate'].replace('/Date(', '').replace(')/', '')[:-3])
            eDate   = int(quizzes['EndDate'].replace('/Date(', '').replace(')/', '')[:-3])

            stDate  = datetime.datetime.fromtimestamp(sDate).strftime('%d-%m-%Y')
            enDate  = datetime.datetime.fromtimestamp(eDate).strftime('%d-%m-%Y')
            dToday  = datetime.datetime.now(pytz.timezone('Asia/Karachi')).strftime("%d-%m-%Y")

            if stDate == dToday:
                stDate += " (today)"

            if enDate == dToday:
                enDate += " (today)"

            fOutput += f"[#] Course: {crs}\nTitle: {title}\nStart Date: {stDate}\nEnd Date: {enDate}\n\n"

        print(fOutput)
        return(fOutput)

    else:
        print("[!] Can't load GDB endpoint..")

def main():
    username        = "bcXXXXXX"       # VU User's ID
    password        = "XXXXXXXX"       # VU User's Password

    loginEndpoint   = "https://ws.vu.edu.pk/MobileApp/Student.asmx/GetStudent"
    gdbEndpoint     = "https://ws.vu.edu.pk/MobileApp/GradedActivitiesToDo.asmx/getGDB"
    quizEndpoint    = "https://ws.vu.edu.pk/MobileApp/GradedActivitiesToDo.asmx/getQuizzes"
    assignEndpoint  = "https://ws.vu.edu.pk/MobileApp/GradedActivitiesToDo.asmx/getAssignments"

    webHookURL      = "https://discord.com/api/webhooks/XXX/XXX"

    while True:
        name, token     = login(loginEndpoint, username, password)
        gdbs            = fetchGDB(gdbEndpoint, token)
        quizzes         = fetchQuizzes(quizEndpoint, token)

        requests.post(webHookURL, {
            "content": f"[&] GDBs: \n\n{gdbs}--\n\n[&] Quizzes: \n\n{quizzes}"
        })

        sleep(21600)    # 6 Hours of time -- to post updates

if __name__ == '__main__':
    main()
