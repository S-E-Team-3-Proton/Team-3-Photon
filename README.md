# Team-3-Proton
# Repository made by Nathan Fuhrman
# Note 1: We increased the allotted VB memory to 8 GB


 install psycopg2(Python postgreSQL adapter):
 pip install psycopg2-binary

 use:
 psql -d photon -U student
 \d players
 to connect to database as student and observe column names. (id, codename)

 The password field is set as student. I don't think thats what it is as defaut for the password, but i've changed it on my system so I dodn't know what it was.
 Use:
 \password student
 to update the password.

 In the main() first checks if there is a player with ID 1, which in fact there is: "Opus", unsure what to do about him. You can change the vT value from 1 to 2 for example to get it to print a new id & name.
