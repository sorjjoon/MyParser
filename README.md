[Heroku link](https://vast-refuge-33676.herokuapp.com/)


# MyParser
MyParser This project is for the interpretation (parsing) of combat logs provided by the role-playing game Star Wars The Old Republic (SWTOR). The goal is to provide users with statistics regarding their performance by analyzing logs provided by the user.

This project in particular deals with the storage of logs, and in particular logs for ranked pvp games and aims to provide the user statistics regarding played matches, win rate when playing with certain players etc.


[User stories](/documentation/stories.md)  
[Database](/documentation/data.png)  
[config](/documentation/config.md)  
[Example logs for testing](/documentation/Example-logs)  
[Insturctions](/documentation/help.md)
[Create table, and stats queries](/documentation/sql)
Example logs are split into two folders, based on which character they are for (for creating multiple characters)  
You can easily create logs for new characters by editing a log to replace all mentions of the char name with something else  
(eaisest to do for char 1, find and replace "Firaksian" with "Something", just make sure "something" is less than 30 letters)
