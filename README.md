# Testing Server
## Capabilities  
  - register participant
  - clone project repositories on schedule
  - run a testing script on a repository and save results
  - show summary

## Usage
  1. Install `docker` and `docker-compose`
  2. Setup configuration (see section [Config](#config))
  3. `make dev-up`

## Config  
### Minimum  
  1. `cp config.env.example docker/dev/config.env`
  2. Create gmail account (or use your own) for email bot  
  3. Set variables `MAIL_USERNAME` and `MAIL_PASSWORD`  

You are ready to run `make dev-up`!

### Advanced  

[Postgresql](https://hub.docker.com/_/postgres/) config  

```bash
POSTGRES_PASSWORD=password
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=postgres:5432
```    

[Flask-Mail](https://pythonhosted.org/Flask-Mail/) config  

```bash
MAIL_USERNAME=user@gmail.com
MAIL_PASSWORD=user_password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=1
```

  1. Setup docker/test/config.env file
  2. Get sertificate for your domain (e.g. via [Certbot](https://certbot.eff.org/))
  3. Place **cert.key** and **cert.crt** into **test/nginx/**
  4. Modify **test/nginx/nginx.conf** to use your own domain (replace *grihabor.tk*)

Now you are ready to run `make test-up`!

