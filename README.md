# VUBot

A script to post `Quizzes`, `GDBs`, and `Assignments` in Discord channel via WebHooks to alert the assignee. 

### Features

- Fetching Student's assigned `GDBs`, `Quizzes` and `Assignments`
- From (v1.2), we get any **pending challans'** as well! 😄
- Posting all that stuff in a `Discord channel`

### How it works?

The script utilizies `Web Applications` source from VULMS. First it authenticates the user with his `studentId` and `studentPassword` and then creates and maintains a `session`. Utilizing that `session`, it accesses the **ActivityCalendar.aspx** file and gets the `JSON` containing the all data related to assigned stuff.

### How to use?

Add the following `environmental variables` according to your credentials and then execute the `script`.

```bash
export USERNAME=bcXXXXXXXX
export PASSWORD=XXXXXXXXXXX
export WEBHOOK_URL=https://discord.com/api/webhooks/XXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
```

```bash
python3 vu.py
```

Alternatively, you can hard-code the **credentials** in the `creds.sh` file, `source` it, and execute the script. 

```bash
source creds.sh
python3 vu.py
```

### Output

<img src="https://i.imgur.com/9TVTlgn.png">

<img src="https://i.imgur.com/GErG3xz.png">
