# VUBot
A script to post `Quizzes`, `GDBs`, and `Assignments` in Discord channel via WebHooks to alert the assignee. 

### Features
- Fetching Student's assigned `GDBs`, `Quizzes` and `Assignments`
- From (v1.2), we get any **pending challans'** as well! 😄
- Posting all that stuff in a `Discord channel`

### How it works?
The script utilizies `Web Applications` source from VULMS. First it authenticates the user with his `studentId` and `studentPassword` and then creates and maintains a `session`. Utilizing that `session`, it accesses the **ActivityCalendar.aspx** file and gets the `JSON` containing the all data related to assigned stuff.

### How to use?
Add `user's credentials` and `WebHook URL` of the Discord channel in the [config.json](https://github.com/Anon-Exploiter/VUBot/blob/main/config.json) file (it already has test data in it -- just populate it)

With docker:
```bash
docker run uexpl0it/vubot:0.1 username pswd webhookURL
```

<img src="https://i.imgur.com/E2a6DuM.png">

After doing so, upload the script on **Heroku**, `requirements`, `Procfile`, and `runtime.txt` has already been added. You can either run the script on some other `EC2 instance` (which constantly runs) or on Heroku and configure Dyno to constantly run (recommended and free way). 

### Output

<img src="https://i.imgur.com/9TVTlgn.png">

<img src="https://i.imgur.com/R6nl3G1.png">

### Todos
- Update screenshots of the README.md file

### Changelog
| Changes                                                                                                   | Release                                             
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------- 
|Jumped directly from mobile application's API endpoints to Web (easy life) |1.2 - 21-05-2021|
| [Major bug fix] Fixes time issue while execution in Heroku server | 0.3 - 13-02-2021
| Implements [#1](https://github.com/Anon-Exploiter/VUBot/issues/1), [#2](https://github.com/Anon-Exploiter/VUBot/issues/2), and [#3](https://github.com/Anon-Exploiter/VUBot/issues/3) -- Minor enhancements                                                           | 0.2 - 11-02-2021                                    
| Initial release containing VU Bot which lets one get discord post of Quizzes and Assignments              | 0.1 - 09-02-2021                                    

