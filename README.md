
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

## Usage
1.) Make a server online using AWS make necessary changes to allow inbound connections on port 8000 or the port of your choice.<br>
<br>
2.) In line 27 of the `stage2_keylogger.py` edit the url to match with your server ip and port. Obfuscate the stage2_keylogger.py file using the [FudCrypt](https://github.com/machine1337/fudcrypt) project. Then, serve it as a directly downloadable file on the flask app in the `/dwfile` route, you can do this by editing line 56 of `app.py` and providing the path to your edited and obfuscated `stage2_keylogger.py` stored on your AWS server.
<br><br>
3.) In line 106 of `app.py` add your username and password for route security<br>
<br>
4.) Create a sqlite3 database `dope.db` of the following schema - <br>
`sqlite> .schema`<br>
`CREATE TABLE data (pcname text, mac text , data text, time text);`<br>
`CREATE TABLE admin_users(username text primary key, hash text required);`<br>
`CREATE TABLE pslist(pcname text primary key, prcslist text, lastupdated text);`<br>
<br>
5.) Add an admin user to login into the admin plan `INSERT INTO admin_users(username, hash) VALUES ('your_username_here','your_complete_password_hash_generated_using_werkzeug.security_library')` <br>
<br>
6.) HOST the flask app on your AWS server for it to be accessible over the internet.<br>
<br> 
#### NOW YOUR SERVER AND PAYLOAD ARE READY!
#### Now we have to prepare the `stage1_payload` and deliver it to the target pc.
1.) In line 16 of the `stage1_payload.py` edit the url to match with your flask route `http://<ip>:<port>/dwfile`. The stage1 payload downloads the keylogger file using web requests and execute it in the memory without writing it on the disk.<br>
<br>

2.) Convert the `stage1_payload.py` in a standalone executable file using pyinstaller or any other tool of your choice. 
<br.

## Congratulations!! Your setup is done.
Now all you have to do is transfer the .exe file into the victim pc, preferably store it in the `startup` folder so that it is automatically started everytime the pc boots.


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
