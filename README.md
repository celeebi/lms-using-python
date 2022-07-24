# lms-using-python

LMS (Library management system) using python

i started by creating the mysql database, the schemas can be depicted from the db.jpg
so we have few tables, the user(anggota), book(buku), and loan status(pinjaman)

the flow goes like this, everytime we add new user the script will put it in the anggota table, 
and the book goes through the buku table, 

when one of the member borrow a book, we will reduce the stock from book table, and add the
borrow status in borrow table

in the lms.py i started by importing the necessary modules, and i used the script provided by pacman academy
for connecting the query to mysql,

i store the 9 function in a dictionary to be called upon the running of program, and run the program using while loop
for the user to decide which method they want to use
