# VUBot
A script to post Quizzes, GDBs, and Assignments in Discord server to alert the student via WebHooks

### Features
- Fetching Student's assigned GDBs and Quizzes
- Posting all the stuff in Discord

### How it works?
<p>The script utilizies mobile API endpoints from VULMS Android application. First it authenticates the user with his userId and userPassword and then gets an accessToken from the returned JSON after successful login. After doing so, it hits the GDB and QUIZ endpoint to fetch all and post only first 3 into the discord server. 
    
The script keeps running in a `while True` loop and prints the assigned stuff every 6 hours every day.</p>

### How to use?
Add user's credentials and WebHook URL of Discord server in the `main()` function of the script. 

<img src="https://i.imgur.com/kB4cdyi.png">

After doing so, upload the script on Heroku, requirements, Procfile, and runtime.txt has already been added. You can either run the script on some other EC2 instance (which constantly runs) or on Heroku and configure Dyno to constantly run. 

### Output

<img src="https://i.imgur.com/AKfRaDJ.png">

<img src="https://i.imgur.com/HdwlM6t.png">

### To-implement
- Posting of assignments (since I don't have any assignment in portal can't parse that rn, DM me your creds if you want, I'll implement that as well)

### Changelog
| Changes                                                                                                   | Release                                             
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------- 
| [Major bug fix] Fixes time issue while execution in Heroku server | 0.3 - 13-02-2021
| Implements [#1](https://github.com/Anon-Exploiter/VUBot/issues/1), [#2](https://github.com/Anon-Exploiter/VUBot/issues/2), and [#3](https://github.com/Anon-Exploiter/VUBot/issues/3) -- Minor enhancements                                                           | 0.2 - 11-02-2021                                    
| Initial release containing VU Bot which lets one get discord post of Quizzes and Assignments              | 0.1 - 09-02-2021                                    

