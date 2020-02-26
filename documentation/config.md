## Configuration
  
Locally the only configuration needed is python runtime with version 3.7.x or newer, and dependencies listed in requirments.txt (install with pip -r)
  
Currently the app is configured to run in Heroku using postgresql (and psycopg), for configuration application __init__ should include all system variables needed by the application, mainly the DATABASE URL the application is supposed to use.  
Note: table creation, index creation and most sql queries are done with sqlalchemy core, so they should be independent of the database engine used, but the queires in database._stats are written by hand due to the complexity, so if the engine used is something other than postegre or sqlite3, these queires would need to be updated to match the new syntax
