# VUBot
A script to post Quizzes, GDBs, and Assignments in Discord server to alert the student via WebHooks

### Features
- Fetching Student's assigned GDBs and Quizzes
- Posting all the stuff in Discord

### How it works?
<p>The script utilizies mobile API endpoints from VULMS Android application. First it authenticates the user with his userId and userPassword and then gets an accessToken from the returned JSON after successful login. After doing so, it hits the GDB and QUIZ endpoint to fetch all and post only first 3 into the discord server.</p>

### To-implement
- Posting of assignments (since I don't have any assignment in portal can't parse that) 
