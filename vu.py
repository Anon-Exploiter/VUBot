#!/usr/bin/python3

from bs4 import BeautifulSoup
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import requests
import datetime, pytz
import json
import re

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fixAndReturnDates(start, end):
    """Since the script runs on Gitlab - Time is in different time zone
    causing the script to provide wrong alerts or wrong dates/times.

    This function converts the time in Asia/Karachi timezone.

    Args:
        start ([str]): Starting date of the assigned task
        end ([str]): Ending date of the assigned task
    """
    start = datetime.datetime.strptime(
        "-".join(start.split(",")[::-1]), "%d-%m-%Y"
    ).strftime("%d-%m-%Y")
    end = (
        datetime.datetime.strptime("-".join(end.split(",")[::-1]), "%d-%m-%Y")
        - datetime.timedelta(days=1)
    ).strftime("%d-%m-%Y")
    dateToday = datetime.datetime.now(pytz.timezone("Asia/Karachi")).strftime(
        "%d-%m-%Y"
    )

    # print(start, end, dateToday)
    return (start, end, dateToday)


def returnRequestDetailsOnFailure(url, customString, requestObj):
    """For debugging request/response being sent/recieved from the
    VU application.

    Args:
        url ([str]): URL the request sent to
        customString ([str]): Indicating where it's happening
        requestObj ([object]): request object containing all methods
    """
    string = f"\n[!] {customString}: {url}\n"
    string += f"[!] Status Code: {requestObj.status_code}\n"
    string += f"[!] Response Headers: {requestObj.headers.items()}\n"
    string += f"[!] Some text of the body: {requestObj.text[:200]}\n"
    print(string)


def loginIntoWebApplication(studentId, password):
    """Login into the application and return the sesion to use for
    further requests

    Args:
        studentId ([str]): Username/VU ID
        password ([str]): Login password

    Returns:
        [object]: Requests' Session object
    """
    loginURL = "https://vulms.vu.edu.pk:443/LMS_LP.aspx"

    session = requests.session()
    getLoginParameters = session.get(
        loginURL,
        # proxies = {
        #     'http': '127.0.0.1:8080',
        #     'https': '127.0.0.1:8080',
        # },
        verify=False,
    )

    if getLoginParameters.status_code == 200:
        soup = BeautifulSoup(getLoginParameters.text, "html.parser")
        viewstate = soup.find_all("input", {"id": "__VIEWSTATE"})[0]["value"]
        eventvalid = soup.find_all("input", {"id": "__EVENTVALIDATION"})[0][
            "value"
        ]

        # Login form won't work without these params

        # print(f"[%] __VIEWSTATE: {viewstate}")
        # print(f"[%] __EVENTVALIDATION: {eventvalid}")

        # Loggin in with the viewstate and eventvalidation parameters.

        login = session.post(
            loginURL,
            # proxies = {
            #     'http': '127.0.0.1:8080',
            #     'https': '127.0.0.1:8080',
            # },
            verify=False,
            data={
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalid,
                "txtStudentID": studentId,
                "txtPassword": password,
                "cbKeepMeLogin": "on",
                "ibtnLogin": "Sign In",
            },
        )

        if login.status_code == 200:
            cookies = dict(login.cookies)

            if "stdUserName" in cookies:
                # print(f"\n[#] User ({cookies['stdUserName']}) logged in!")

                # Need to give /Home.aspx a hit with some token without that, the cookies don't work lol! (found after hella debuggin)
                locationHref = re.findall(
                    r"window\.top\.location\.href=\'Home\.aspx\?id\=(.*?)\'\;",
                    login.text,
                )[0]

                homePath = (
                    f"https://vulms.vu.edu.pk/Home.aspx?id={locationHref}"
                )
                homeRequest = session.get(
                    homePath,
                    # proxies = {
                    #     'http': '127.0.0.1:8080',
                    #     'https': '127.0.0.1:8080',
                    # },
                    verify=False,
                )

                return session

        else:
            returnRequestDetailsOnFailure(
                url=loginURL,
                customString="There was an error trying to fetch params",
                requestObj=getLoginParameters,
            )

    else:
        returnRequestDetailsOnFailure(
            url=loginURL,
            customString="There was an error trying to login",
            requestObj=login,
        )


def fetchCalendarAndDetails(session):
    """Fetches the Calendar for all the tasks assigned

    Args:
        session ([object]): Requests session to do further requests

    Returns:
        [str]: Returns the Discord post
    """
    calendarURL = (
        "https://vulms.vu.edu.pk/ActivityCalendar/ActivityCalendar.aspx"
    )

    try:
        request = session.get(
            calendarURL,
            # proxies = {
            #     'http': '127.0.0.1:8080',
            #     'https': '127.0.0.1:8080',
            # },
            verify=False,
        )

        if request.status_code == 200:
            post = ""
            source = request.text
            jsonData = re.findall(r"var\sJsonData\s\=\s(.*?)\;", source)[0]

            calendarJSON = json.loads(jsonData)
            print(json.dumps(calendarJSON, indent=4))
            print()

            for subjects in calendarJSON:
                coursecode = subjects["coursecode"]
                title = subjects["title"]
                url = subjects["url"]
                start = subjects["start"]
                end = subjects["end"]

                startDate, endDate, dateToday = fixAndReturnDates(start, end)
                # print(title, startDate, endDate, dateToday, subtDate)

                subtDate = datetime.datetime.strptime(
                    endDate, "%d-%m-%Y"
                ) - datetime.datetime.strptime(dateToday, "%d-%m-%Y")
                subtDate = str(subtDate).split(" ")[0]

                if "0:00:00" in subtDate:
                    subtDate = 1

                subtDate = int(subtDate)

                if startDate == dateToday:
                    startDate += " **(today)**"

                if endDate == dateToday:
                    endDate += " __**(today)**__"

                if subtDate == -1:
                    if startDate != endDate:
                        post += f"[#] **{title}**\n"
                        post += f"Start date: {startDate}\n"

                        if startDate < endDate:
                            post += f"End date: {endDate}\n\n"

                if subtDate > 0:
                    if subtDate == 1:
                        post += (
                            f"[#] **{title}** (_**{subtDate}** day left_)\n"
                        )

                    else:
                        post += (
                            f"[#] **{title}** (_**{subtDate}** days left_)\n"
                        )

                    post += f"Start date: {startDate}\n"
                    post += f"End date: {endDate}\n\n"

            print(post)
            return post

        else:
            returnRequestDetailsOnFailure(
                url=calendarURL,
                customString="There was an error trying to fetch calendar",
                requestObj=request,
            )

    except AttributeError:
        print("\n[!] Did you forget to add credentials in config.json?")


def postIntoDiscord(post, webHookURL):
    """Posts the given string into discord channel through webhook

    Args:
        post ([str]): Summary/Data to post
        webHookURL ([str]): Webhook URL of discord channel
    """
    discordPost = requests.post(webHookURL, {"content": post})

    if discordPost.status_code == 204:
        print("[#] Posted in discord!")

    else:
        returnRequestDetailsOnFailure(
            url=webHookURL[:31],
            customString="There was an error trying to post on webhook",
            requestObj=discordPost,
        )


def main():
    with open("config.json", "r") as f:
        configContents = json.loads(f.read().strip())

    studentId = configContents["studentId"]
    password = configContents["password"]
    webHookURL = configContents["discordWebHookURL"]

    print("[&] Logging into the Web application...\n")

    session = loginIntoWebApplication(studentId, password)
    post = fetchCalendarAndDetails(session)

    postIntoDiscord(post, webHookURL)


if __name__ == "__main__":
    main()
