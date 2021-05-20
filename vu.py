from bs4 import BeautifulSoup

import requests
import urllib3
import datetime, pytz
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fixAndReturnDates(start, end):
    start       = datetime.datetime.strptime("-".join(start.split(",")[::-1]), '%d-%m-%Y').strftime("%d-%m-%Y")
    end         = (datetime.datetime.strptime("-".join(end.split(",")[::-1]), '%d-%m-%Y') - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    dateToday   = datetime.datetime.now(pytz.timezone('Asia/Karachi')).strftime("%d-%m-%Y")

    # print(start, end, dateToday)
    return(start, end, dateToday)

def returnRequestDetailsOnFailure(url, customString, requestObj):
    string      =  f"\n[!] {customString}: {url}\n"
    string      += f"[!] Status Code: {requestObj.status_code}\n"
    string      += f"[!] Response Headers: {requestObj.headers.items()}\n"
    string      += f"[!] Some text of the body: {requestObj.text[:200]}\n"
    print(string)

def loginIntoWebApplication(studentId, password):
    loginURL    = "https://vulms.vu.edu.pk:443/LMS_LP.aspx"

    session             = requests.session()
    getLoginParameters  = session.get(loginURL,
        # proxies = {
        #     'http': '127.0.0.1:8080',
        #     'https': '127.0.0.1:8080',
        # },
        verify  = False,
    )

    if getLoginParameters.status_code == 200:
        soup        = BeautifulSoup(getLoginParameters.text, 'html.parser')
        viewstate   = soup.find_all('input', {'id': '__VIEWSTATE'})[0]['value']
        eventvalid  = soup.find_all('input', {'id': '__EVENTVALIDATION'})[0]['value']

        # Login form won't work without these params

        print(f"[%] __VIEWSTATE: {viewstate}")
        print(f"[%] __EVENTVALIDATION: {eventvalid}")

        # Loggin in with the viewstate and eventvalidation parameters. 

        login       = session.post(loginURL,
            # proxies = {
            #     'http': '127.0.0.1:8080',
            #     'https': '127.0.0.1:8080',
            # },
            verify  = False,
            data    = {
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalid,
                "txtStudentID": studentId,
                "txtPassword": password,
                "cbKeepMeLogin": "on",
                "ibtnLogin": "Sign In"
            }
        )

        if login.status_code == 200:
            cookies     = dict(login.cookies)

            if 'stdUserName' in cookies:
                print(f"\n[#] User ({cookies['stdUserName']}) logged in!")

                # Need to give /Home.aspx a hit with some token without that, the cookies don't work lol! (found after hella debuggin)
                locationHref    = re.findall(r'window\.top\.location\.href=\'Home\.aspx\?id\=(.*?)\'\;', login.text)[0]

                homePath        = f'https://vulms.vu.edu.pk/Home.aspx?id={locationHref}'
                homeRequest     = session.get(homePath,
                    # proxies = {
                    #     'http': '127.0.0.1:8080',
                    #     'https': '127.0.0.1:8080',
                    # },
                    verify  = False,
                )

                return(session)

        else:
            returnRequestDetailsOnFailure(url = loginURL, customString = "There was an error trying to fetch params", requestObj = getLoginParameters)

    else:
        returnRequestDetailsOnFailure(url = loginURL, customString = "There was an error trying to login", requestObj = login)

def fetchCalendarAndDetails(session):
    calendarURL     = 'https://vulms.vu.edu.pk/ActivityCalendar/ActivityCalendar.aspx'
    request         = session.get(calendarURL,
        # proxies = {
        #     'http': '127.0.0.1:8080',
        #     'https': '127.0.0.1:8080',
        # },
        verify  = False,
    )

    if request.status_code == 200:
        post            = ""
        source          = request.text
        jsonData        = re.findall(r'var\sJsonData\s\=\s(.*?)\;', source)[0]
        
        calendarJSON    = json.loads(jsonData)
        print(json.dumps(calendarJSON, indent=4))
        print()

        for subjects in calendarJSON:
            coursecode  = subjects['coursecode']
            title       = subjects['title']
            url         = subjects['url']
            start       = subjects['start']
            end         = subjects['end']

            startDate, endDate, dateToday   = fixAndReturnDates(start, end)

            if startDate == dateToday:
                startDate += " **(today)**"

            if endDate == dateToday:
                endDate   += " __**(today)**__"  

            post        += f"[#] **{title}**\n"
            post        += f"Start date: {startDate}\n"
            post        += f"End date: {endDate}\n\n"

        print(post)
        return(post)

    else:
        returnRequestDetailsOnFailure(url = calendarURL, customString = "There was an error trying to fetch calendar", requestObj = request)

def postIntoDiscord(post, webHookURL):
    discordPost     = requests.post(webHookURL, {
        "content": post
    })

    if discordPost.status_code == 204:
        print("[#] Posted in discord!")

    else:
        returnRequestDetailsOnFailure(url = webHookURL[:10], customString = "There was an error trying to post on webhook", requestObj = discordPost)

def main():
    with open('config.json', 'r') as f: configContents = json.loads(f.read().strip())

    studentId   = configContents['studentId']
    password    = configContents['password']
    webHookURL  = configContents['discordWebHookURL']

    print("[&] Logging into the Web application...\n")

    session     = loginIntoWebApplication(studentId, password)
    post        = fetchCalendarAndDetails(session)

    postIntoDiscord(post, webHookURL)

if __name__ == '__main__':
    main()