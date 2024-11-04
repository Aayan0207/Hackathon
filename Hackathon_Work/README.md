# Explorer's Cove 
## 1. Import the zip file into VSCode and extract the files or download this repository's files
## 2. Setting up Hackathon.sql
### Once the zip file is downloaded and extracted or the repository files are downloaded, open MySQL on your system and run the following commands
#### CREATE DATABASE Hackathon;
##### Name for the database can be something else but a change would be #required in the app.py then
#### USE Hackathon;
### Then open the command prompt and run this command:
#### “mysql_command_path” -u username -p Hackathon < “path_of_Hackathon.sql”
##### For example: "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p Hackathon < "C:\Users\Aayan Khan\OneDrive\Desktop\Computer Science\Hackathon_Work\Hackathon.sql"
###### You will prompted for the password of the username and after that the sql file will create the DB in MYSQL
## 3. App.py
#### In line 15, kindly update the user, password and database variables accordingly.
[!Image](https://drive.google.com/file/d/1-Dxh5aOWbkf4vB2UsKSVRnnkZpFCHrgX/view?usp=drive_link)
## 4. Ensuring the working directory is correct, execute the command: flask run in the VSCode terminal and click the corresponding link given.
