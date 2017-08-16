# Testing Server
## Capabilities  
  - register participant
  - clone project repositories on schedule
  - run a testing script on a repository and save results
  - show summary

## Usage
  1. Install ```docker``` and ```docker-compose```
  2. Setup configuration (see section Config)
  3. ```make dev```

## Config  
### Minimum  
  1. ```cp config.env.example dev/config.env```  
  2. Create gmail account (or use your own) for email bot  
  3. Set variables ```MAIL_USERNAME``` and ```MAIL_PASSWORD```  

You are ready to run ```make dev```!

### Advanced   
 - postgres - [Postgresql](https://hub.docker.com/_/postgres/)
```
POSTGRES_PASSWORD=password
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=postgres:5432
```  
 - mail - [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
```
MAIL_USERNAME=user@gmail.com
MAIL_PASSWORD=user_password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=1
```  
