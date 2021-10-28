# DarkLegend Discord Bot



 Hi! I'm The all in one open Source Discord Bot **Dark Legend**.
Feel free to join our discord if you got trouble setting up your own Bot.
[🆃🅴🅲🅷🅲🆁🅴🆆](https://discord.gg/3PCCPanvSm)

# Features:
### Welcome message 
###### Send New Users a welcome message and announces Join and Leave.
### Ticket System
###### Support Ticket and Support Channel for specific User
### Server Stats
###### Displays information about the server update included.
### User Info
###### Displays information about a specific User.
### Reaction System
###### create Reaction Roles
### Help System
###### multi side help menu. 
### Warning System
###### Warn Users.

# Installation:
Download the Package and extract. 

## Requirements:
Install following Python Moules:    
-    python -m pip install discord
-    python -m pip install aiofiles


## Setup Config File:
go to DLTV/config.json and edit following:
- (prefix) the Bot Prefix to Call
- replace "token not set" with your token from discord.
- replace "guild" with the Id of the Guild.
- replace "join_channel" with the Id of the Channel where you want the Join/Leave message to be send.   
- replace "stats_channel" with the Id of the Channel where you want the Stats message to be send. 
- replace "report_channel" with the Id of the Channel where you want the Report message to be send. 


# Discord Setup:
 Create a category for support:\
 Channels you have to create: 
+ join_channel
+ stats_channel
+ log_channel
+ report_channel
+ support_channel\

You can use this [template]([https://www.google.com/](template)).\
This template contains no roles or settings. 


# Commands:
List of commands the bot can proceed: 
- poll * topic  [create a poll]
- logout  [logout]
- clear * amount(default=1)  [delete message]
- create_reaction * role * message(id) + emoji [create reaction role]
- configure_ticket * message(id) * category(id) [create reaction for support]
- warn * user * reason [warn user]
- warn_show * user [show warning for user]
- report * reason [report to an admin]
- info * user [user info]
- ban * user * reason [ban user with reason]
- kick * user * reason [kick user with reason]
- emded * emded(gamerole, verify, rules, support) [create embed in channel]