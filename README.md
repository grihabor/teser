# Testing Server
Capabilities  
  - register participant
  - clone project repositories on schedule
  - run a testing script on a repository and save results
  - show summary

## Usage
  1. Install ```docker``` and ```docker-compose```
  2. Set up configuration: ```cp config.env.example config.env```
  3. ```docker-compose pull```
  4. ```docker-compose up```

## Config
 - postgres
  ```
  POSTGRES_PASSWORD=password
  POSTGRES_USER=postgres
  POSTGRES_DB=postgres
  POSTGRES_HOST=postgres:5432
  ```
 - mail
  ```
  MAIL_USERNAME=user@gmail.com
  MAIL_PASSWORD=user_password
  MAIL_SERVER=smtp.gmail.com
  MAIL_PORT=465
  MAIL_USE_SSL=1
  ```
