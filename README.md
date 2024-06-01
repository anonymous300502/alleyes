
<p align="left">
	<h1 align="left"> AllEyes </h2>
	<h4 align="left"> A python spyware which acts as a keylogger and logs keys from the target PC using REST APIs made in flask,
  the payload has been divided into a two stage payload and instructions to use are given below.<h4>
</p>

---
## Problem Statement. 
A spyware developed to hack hardware device(keyboard) and send it's data to the online attacker's server.
  (STRICTLY DEVELOPED FOR EDUCATIONAL PURPOSES ONLY)

## Functionalities
#### Users can do the following:
- [ ] View the keylogs of each target PC arranged in sqlite tables in the database by their usernames.
- [ ] Get a view of the top 10 processes running on the target system along with their uptime arranged by there memory consumption 
- [ ] An Extensive admin panel on the webapp with login functionalities and route secrutiy to view keylogs. 
- [ ] A database to store keylogs along with username and timestamp. 

## USAGE:
1.) Make a server online using AWS make necessary changes to allow inbound connections.<br>
<br>
2.) In line 27 of the `stage2_keylogger.py` edit the url to match with your server ip and port and store it on your online server.<br>
<br>
3.) In line 56 of `app.py` provide the path to your `stage2_keylogger.py` stored on your server and in line 106 of `app.py` add your username and password for route security<br>
<br>
4.) Create a sqlite3 database `dope.db` of the following schema - <br>
`sqlite> .schema`<br>
`CREATE TABLE data (pcname text, mac text , data text, time text);`<br>
`CREATE TABLE admin_users(username text primary key, hash text required);`<br>
`CREATE TABLE pslist(pcname text primary key, prcslist text, lastupdated text);`<br>
<br>
5.) Add an admin user to login into the admin plan `INSERT INTO admin_users(username, hash) VALUES ('your_username_here','your_complete_password_hash_generated_using_werkzeug.security_library')` <br>
<br>
6.) HOST the flask app on your online server for it to be accessible over the internet.<br>


## Built with
- `Python` - for the spyware scripts. 
- `AWS` - for hosting.
- `sqlite3` - for database.
- `flask` - for Webapp and REST API developement.
- `gunicorn` - for implimenting WSGI ( Web Server Gateway Interface ).
- `nginx` - for webserver acting as a reverse proxy to AWS.

  FOR CREATING THE VIRUS EXE, EDIT THE VIRUS CODE AND CREATE AN EXE USING PYINSTALLER 
## Contributors
* [Abhishek Sharma](https://github.com/anonymous300502)

* [Manaswi Sharma](https://github.com/manaswii)

<br>
<br>
<p align="center">
	Made during 🌙 by flat chicklets
</p>
