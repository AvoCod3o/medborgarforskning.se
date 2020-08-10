The following are the notes to deploy the ARCS Core System as deployed on dev.medborgarforskning.se/ and medborgarforskning.se/.

Prerequisite:
1. Existing instance of Linux server
2. Docker configured on the hosts
3. 



# FIRST Deploy script - for first deploy - not update of the running site
#download the zip of the repo to the server (or copy git repo)
(if deploy is another branch the zip directory and extracted directory path need update)

#scp [local path to file] [remote file path]
scp ~/Downloads/medborgarforskning.se-master.zip arcs:/home/xbriej@GU.GU.SE/arcgit/

# on the server
sudo unzip ~/arcgit/medborgarforskning.se-master.zip -d /opt/ARCSystem/www/
# useradmin password here

# Permissions here may not need to be changed and are ok as root:root
sudo chown -R root:arcs .git/
sudo chown -R root:arcs medborgarforskning.se-master/

### ONLY WHILE DEV HACK in use has cert in it ###
# Check SELinux Status - we care about Enforcing or Permissive
getenforce

#Remove the temp certs

#limit the authorized hosts

#double check correct the domain for the cert and authorized hosts is right

#switch settings.py to use email backend
## Partial

#switch to postgresdb

#remove the debug flag
# - settings.py Set False to DEBUG flag

#all of this is configured in env variables in the initconfig branch... just need to wrap it up.

### END of DEV HACK ###

cd /opt/ARCSystem/www/medborgarforskning.se-master/nginx/init
# set domain in init-letsencrypt.sh
sudo sh init-letsencrypt.sh

# run the docker-compose file and disconnect from the shell
docker-compose up --build -d



### OTHER NOTES ###
docker-compose up doens't incorporate code changes - must do docker-compose up --build or just build the single image


### UPDATE SECOND RUN - you can just apply the code over the existing files with # Replace all ??? Yep with the "A"
# Also the certificate should still be there so no need to run init-security

# Need to enter the docker container to run collectstatic


### NOTE FOR LATER install script ###
# Check for SELinux
docker info | grep 'Security Options'

### END Note for later ###

SOOOO CLOOOSE

Now just doesn't get verified.

### Waiting for 35 seconds for nginx to start ###
### Requesting Let's Encrypt certificate for dev.medborgarforskning.se ...
### Requesting Let's Encrypt certificate for  -d dev.medborgarforskning.se for jonathan.brier@gu.se ...
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator webroot, Installer None
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for dev.medborgarforskning.se
Using the webroot path /var/www/certbot for all unmatched domains.
Waiting for verification...
Challenge failed for domain dev.medborgarforskning.se
http-01 challenge for dev.medborgarforskning.se
Cleaning up challenges
Some challenges have failed.

IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: dev.medborgarforskning.se
   Type:   unauthorized
   Detail: Invalid response from
   http://dev.medborgarforskning.se/.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0
   [130.241.135.142]: "<html>\r\n<head><title>403
   Forbidden</title></head>\r\n<body>\r\n<center><h1>403
   Forbidden</h1></center>\r\n<hr><center>nginx/1.17.10</c"

   To fix these errors, please make sure that your domain name was
   entered correctly and the DNS A/AAAA record(s) for that domain
   contain(s) the right IP address.

### Waiting for 10 seconds for certificates before reboot ###
### Reloading nginx ...
nginx: [emerg] cannot load certificate "/etc/letsencrypt/live/dev.medborgarforskning.se/fullchain.pem": BIO_new_file() failed (SSL: error:0200100D:system library:fopen:Permission denied:fopen('/etc/letsencrypt/live/dev.medborgarforskning.se/fullchain.pem','r') error:2006D002:BIO routines:BIO_new_file:system lib)

#### Looking at the nginx log all you see is the permission denied
2020/05/18 07:36:05 [warn] 7#7: "ssl_stapling" ignored, no OCSP responder URL in the certificate "/etc/letsencrypt/live/dev.medborgarforskning.se/fullchain.pem"
2020/05/18 07:36:47 [error] 9#9: *1 open() "/var/www/certbot/.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0" failed (13: Permission denied), client: 52.28.236.88, server: arcstest.brierjon.com, request: "GET /.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0 HTTP/1.1", host: "dev.medborgarforskning.se"
2020/05/18 07:36:47 [error] 9#9: *2 open() "/var/www/certbot/.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0" failed (13: Permission denied), client: 3.14.255.131, server: arcstest.brierjon.com, request: "GET /.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0 HTTP/1.1", host: "dev.medborgarforskning.se"
2020/05/18 07:36:48 [error] 9#9: *3 open() "/var/www/certbot/.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0" failed (13: Permission denied), client: 64.78.149.164, server: arcstest.brierjon.com, request: "GET /.well-known/acme-challenge/9XG0V6-y7IhBmheNAjZ9pcZgkftsNMuHeC5oWk_fHa0 HTTP/1.1", host: "dev.medborgarforskning.se"
2020/05/18 07:37:01 [emerg] 15#15: cannot load certificate "/etc/letsencrypt/live/dev.medborgarforskning.se/fullchain.pem": BIO_new_file() failed (SSL: error:0200100D:system library:fopen:Permission denied:fopen('/etc/letsencrypt/live/dev.medborgarforskning.se/fullchain.pem','r') error:2006D002:BIO routines:BIO_new_file:system lib)

#### Looking at the nginx container directory the permissions are odd with root:1000 set for the letsencrypt directory

#### Looking at the SELINUX Log I found the probable cause for the above error

[xbriej@GU.GU.SE@mbf01-p ~]$ sudo ausearch -m avc -ts today | audit2allow


#============= container_t ==============

#!!!! The file '/opt/ARCSystem/www/medborgarforskning.se-master/data/certbot/conf' is mislabeled on your system.
#!!!! Fix with $ restorecon -R -v /opt/ARCSystem/www/medborgarforskning.se-master/data/certbot/conf
#!!!! This avc is a constraint violation.  You would need to modify the attributes of either the source or target types to allow this access.
#Constraint rule:
#	mlsconstrain dir { ioctl read lock search } ((h1 dom h2 -Fail-)  or (t1 != mcs_constrained_type -Fail-) ); Constraint DENIED
mlsconstrain dir { write setattr append unlink link rename add_name remove_name } ((h1 dom h2 -Fail-)  or (t1 != mcs_constrained_type -Fail-) ); Constraint DENIED
mlsconstrain dir { relabelfrom } ((h1 dom h2 -Fail-)  or (t1 != mcs_constrained_type -Fail-) ); Constraint DENIED
mlsconstrain dir { create relabelto } ((h1 dom h2 -Fail-)  or (t1 != mcs_constrained_type -Fail-) ); Constraint DENIED

#	Possible cause is the source level (s0:c98,c729) and target level (s0:c119,c523) are different.
allow container_t container_file_t:dir setattr;

#!!!! WARNING: 'usr_t' is a base type.
allow container_t usr_t:dir write;



SERVER SELINUX CONFIG WARNING
[xbriej@GU.GU.SE@mbf01-p init]$ docker info | grep 'Security Options'
  WARNING: You're not using the default seccomp profile


OTHER SELINUX DOCKER Good Reference
https://serverfault.com/questions/540537/nginx-permission-denied-to-certificate-files-for-ssl-configuration

 SELINUX MOUNTS need z lower as it allows sharing while Z upper doesn't
 https://jaosorior.dev/2018/selinux-and-docker-notes/docker
