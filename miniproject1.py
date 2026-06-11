import sqlite3
#Connect to database
con=sqlite3.connect("dbss.db")
c=con.cursor()
#Enable foreign key constraints
c.execute("PRAGMA foreign_keys=ON")
#create table user
c.execute("""
           CREATE TABLE IF NOT EXISTS user(
           username TEXT PRIMARY KEY, 
           password TEXT NOT NULL,
           usertype TEXT NOT NULL
           );
""")
#create table menu
c.execute("""
           CREATE TABLE IF NOT EXISTS menu(
           itemid INTEGER PRIMARY KEY, 
           item TEXT UNIQUE NOT NULL,
           price REAL NOT NULL
           );
""")
#create table orders
c.execute("""
           CREATE TABLE IF NOT EXISTS orders(
           orderid INTEGER PRIMARY KEY, 
           username TEXT NOT NULL,
           itemid INTEGER NOT NULL,
           item TEXT NOT NULL,
           quantity INTEGER NOT NULL,
           price REAL NOT NULL,
           FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE,
           FOREIGN KEY(itemid) REFERENCES menu(itemid) ON DELETE CASCADE,
           FOREIGN KEY(item) REFERENCES menu(item) ON DELETE CASCADE
           );
""")
con.commit()
#function to register user/staff
def register():
    u=input("Enter username:")
    p=input("Enter password:")
    #validate usertype
    while True:
        t=input("Enter usertype(user/staff):").lower()
        if t=="staff" or t=="user":
            break
        print("Invalid usertype")
    #insert user into database
    c.execute("INSERT INTO user(username,password,usertype) VALUES(?,?,?)",(u,p,t))
    con.commit()
    print("Registration Successful!")
#function to add an item
def add_item():
    #check whether itemid already exists
    while True:
        try:
            i=int(input("Enter the itemid:"))
            c.execute("SELECT * FROM menu WHERE itemid=?",(i,))
            r=c.fetchone()
            if r is not None:
                print("Itemid already exists")
            else:
                break
        except ValueError:
            print("Invalid itemid")
    n=input("Enter the item:")
    p=float(input("Enter the price:"))
    #insert item into menu
    c.execute("INSERT INTO menu(itemid,item,price) VALUES(?,?,?)", (i, n, p))
    con.commit()
    print("Item added successfully!")
#function to view the menu
def view_menu():
    c.execute("SELECT * FROM menu")
    print("====================MENU====================")
    print("--------------------------------------------")
    print("ITEMID\t|\t\tITEM\t\t|\tPRICE")
    print("--------------------------------------------")
    for i in c.fetchall():#display all menu items
        print (f"{i[0]:<10}{i[1]:<25}?{i[2]}")
def update_item():#function to update an item
    while True:#check validity of itemid
        try:
            i=int(input("Enter the itemid:"))
            c.execute("SELECT * FROM menu WHERE itemid=?",(i,))
            r=c.fetchone()
            if r is None:
                print("Invalid itemid")
            else:
                break
        except ValueError:
            print("Invalid itemid")
    p = float(input("Enter the new price:"))
    c.execute("UPDATE menu SET price=? WHERE itemid=?",(p,i) )#update price of item
    con.commit()
    print("Item updated successfully!")
def delete_item():#function to delete an item
    while True:#check valid itemid
        try:
            i=int(input("Enter the itemid:"))
            c.execute("SELECT * FROM menu WHERE itemid=?",(i,))
            r=c.fetchone()
            if r is None:
                print("Invalid itemid")
            else:
                break
        except ValueError:
            print("Invalid itemid")
    c.execute("DELETE FROM menu WHERE itemid=?", (i,))#delete an item
    con.commit()
    print("Item deleted successfully!")
def place_order(username):#function to place an order
    sum=0
    while True:
        view_menu()
        try:
            i=int(input("Enter the itemid:"))
            q=int(input("Enter the quantity(no):"))
            c.execute("SELECT item,price FROM menu WHERE itemid=?",(i,))#get item details
            r=c.fetchone()
            if r is None:
                print("Invalid itemid")
            else:
                item=r[0]
                price=r[1]
                total=price*q
                sum=sum+total
            c.execute("INSERT INTO orders(username,itemid,item,quantity,price) VALUES (?,?,?,?,?)",(username,i,item,q,total))#save an order
            con.commit()
            ch=input("Order another item?(yes/no):").lower()
            if ch=="no":
                break
        except ValueError:
            print("Invalid itemid")
    print("Order placed successfully!")
    print("Total Amount=?",sum)
def view_orders():# function to view all orders by staff
    c.execute("SELECT * FROM orders")
    print("============================================ORDERS============================================")
    print("----------------------------------------------------------------------------------------------")
    print("ORDERID\t|\tUSERNAME\t|\tITEMID\t|\t\tITEM\t\t|\t\tQUANTITY(NO)\t|\tPRICE")
    print("----------------------------------------------------------------------------------------------")
    for i in c.fetchall():
        print(f"{i[0]:<10}{i[1]:<18}{i[2]:<12}{i[3]:<30}{i[4]:<15}?{i[5]:<10}")
def my_orders(username):#function to view order history by user
    c.execute("SELECT * FROM orders WHERE username=?",(username,))
    print("============================================ORDERS============================================")
    print("----------------------------------------------------------------------------------------------")
    print("ORDERID\t|\tUSERNAME\t|\tITEMID\t|\t\tITEM\t\t|\t\tQUANTITY(NO)\t|\tPRICE")
    print("----------------------------------------------------------------------------------------------")
    for i in c.fetchall():
        print(f"{i[0]:<10}{i[1]:<18}{i[2]:<12}{i[3]:<30}{i[4]:<15}?{i[5]:<10}")
def login():#function for login
    u=input("Enter username:")
    p=input("Enter password:")
    c.execute("SELECT * FROM user WHERE username=? AND password=?",(u,p))#check username and password
    r=c.fetchone()
    if r:
        print("Login Successful.Hello,",r[0])
        if r[2]=="staff":#staff login
            print("Staff access granted!")
            staff()
        elif r[2]=="user":#user login
            print("User access granted!")
            user(r[0])
    else:
        print("Invalid credentials")
def user(username):#function for user
    while True:
        print("======USER MENU======")
        print("1.VIEW MENU")
        print("2.PLACE AN ORDER")
        print("3.MY ORDER HISTORY")
        print("4.LOGOUT")
        c=int(input("Enter your choice(1/2/3/4):"))
        if c==1:
            view_menu()
        elif c==2:
            place_order(username)
        elif c==3:
            my_orders(username)
        elif c==4:
            print("EXITING.....")
            break
        else:
            print("Invalid choice")
def staff():#function for staff
    while True:
        print("========STAFF MENU=======")
        print("1.VIEW MENU")
        print("2.ADD AN ITEM")
        print("3.UPDATE AN ITEM")
        print("4.DELETE AN ITEM")
        print("5.VIEW ALL ORDERS")
        print("6.LOGOUT")
        d=int(input("Enter your choice(1/2/3/4/5/6):"))
        if d==1:
            view_menu()
        elif d==2:
            add_item()
        elif d==3:
            update_item()
        elif d==4:
            delete_item()
        elif d==5:
            view_orders()
        elif d==6:
            print("EXITING.....")
            break
        else:
            print("Invalid choice")
while True:#main menu
    print("=======RESTAURANT MENU SYSTEM=======")
    print("1.REGISTER")
    print("2.LOGIN")
    print("3.EXIT")
    f=int(input("Enter your choice(1/2/3):"))
    if f==1:
        register()
    elif f==2:
        login()
    elif f==3:
        print("EXITING.....")
        break
    else:
        print("Invalid choice")