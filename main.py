from Database.Database import Database
import sys

db_name = input("Enter the Name of the Key value Store :")

if int(input("Press 1 to specify location 0 to skip :")) == 1:
    loc = input("Enter the location")
    db = Database(db_name, loc)
else:
    db = Database(db_name)

while (1):

    choice = int(input("1.Insert Record\n2.Read \n3.Delete\n4.Exit \n"))
    if choice == 1:
        db.create()
    elif choice == 2:
        db.read(input("Enter Key to be Read :"))
    elif choice == 3:
        db.delete(input("Enter Key to be Deleted :"))
    else:
        db.fileclose()
        sys.exit()
