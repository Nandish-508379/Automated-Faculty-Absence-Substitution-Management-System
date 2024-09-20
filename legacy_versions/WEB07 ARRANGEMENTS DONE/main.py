print("WELCOME TO TIMETABLE MANAGEMENT SOFTWARE | PROJECT ID: 006/2024 \nCopyright (c) 2024 M Nandish. All Rights Reserved.")

import mysql.connector as proj
print("\nWELCOME!!!")
## connection
con = proj.connect(host = "localhost" ,user = "root", passwd= "8379", database = "timetable" )
cur = con.cursor() # cursor
            
#code_______________________________________________________________
def admincode():
    global day
    print("login successfull")
    day =input("\nenter the day (** in lowercase only): ")
    if day == "monday" or "tuesday" or "wednersday" or "thursday" or "friday" or "saturday":    
        while True:
            print("\n__________________________________________________________________________':;")
            print(" ADMIN MODE!!!")
            print("\n1:ARRANGEMENT")
            print("2:INSERT DATA INTO DATABASE #USE EXEL IN PREFERED FORMAT ONLY (for otr day sel opt 5)")
            print("3:VIEW FULL DATA/LIST(exel form) OF TEACHERS TIMETABLE")
            print("4:TO REMOVE A TEACHER TIMETABLE ON THE SELECTED DAY")
            print("5:CHANGE DAY$$")
            print("6:TO DELETE COMPLETE DAY TIMETABLE")
            print("7:ADD NEW USER")
            print("8:REMOVE USER")
            print("0:EXIT")
            print("current selected day is ==", day)
            ch = int(input("enter your prefered choice: "))
            print("")

            if ch == 1:
                selection1()
                
            elif ch== 2:
                print("selected #2:INSERT DATA INTO DATABASE #USE EXEL IN PREFERED FORMAT ONLY")
                print("(**rename the file to 'newrec' with save as CSV[comma undefined] and paste in this code folder ).\n(***csv in this format only = ename,class(free period then put = null),period(all periods from 1 to 8).")

                from datetime import datetime
                now = datetime.now()
                print(now)
                password1 = int(now.strftime("%H%M"))
                pased1 = int(input("enter the 4 digit admin password(*CURRENT[at the time of open of this option] TIME IN'HHMM', 24H FORMAT): "))
                if pased1 == password1:
                    import csv 
                    with open("newrec.csv","r",newline="")as file1:
                        flrdr = csv.reader(file1)
                        for n in flrdr:
                            if n[1]== "null":
                                s3= "insert into {} values('{}',{},{});".format(day,n[0],n[1],str(n[2]) )
                                cur.execute(s3)
                                con.commit()
                                print("null record added successfully")
                            else:
                                s3= "insert into {} values('{}','{}',{});".format(day,n[0],n[1],str(n[2]) )
                                cur.execute(s3)
                                con.commit()
                                print("work record added successfully")
                else:
                    print("invalid password!! usspecious activity found now been logged out!!")
                    quit()
                    
            elif ch== 3:
                selection3()
                
            elif ch==4:
                print("selected #4:TO REMOVE A TEACHER TIMETABLE ON THE SELECTED DAY")
                delrec = input("enter the teachers name to delete from the already login day :")
                s4= "delete from {} where ename = '{}';".format(day,delrec)
                cur.execute(s4)
                con.commit()
                print("record deleted plz cheak by getting the data from option 3")
                
            elif ch==5:
                selection5()
                
            elif ch==6:
                from datetime import datetime
                now = datetime.now()
                password = int(now.strftime("%H%M"))
                pased = int(input("enter the 4 digit admin password(*CURRENT[at the time of open of this option] TIME IN'HHMM', 24H FORMAT): "))
                if pased == password:
                    sql6 = "delete from {};".format(day)
                    cur.execute(sql6)
                    print("TIME TABLE OF DAY DELETED!!")
                    con.commit()
                else:
                    print("wrong password")

            elif ch==7:
                print("7:ADD NEW USER")
                username_nusers = input("ENTER NEW USERS USERNAME(case sensitive): ")
                password_nusers = input("ENTER NEW USERS PASSWORD(case sensitive): ")
                mode_nusers = input("ENTER NEW USERS MODE('A' if Admin, 'U' if User.')(*cant be reversed**CASE SENSITIVE): ")
                print("selected to add user withe the following credentials;")
                print("USERNAME = ",username_nusers)
                print("PASSWORD = ",password_nusers)
                print("MODE/ROLE (DO CONFIRM IF ENTERED INPUT IS'A' if Admin, 'U' if User.)= ",mode_nusers,"\nDO YOU WANT TO CONTINUE?(PRESS 'YES' ID YOU WANT TO DO SO)")
                inp = input("\nENTER YOUR CHOICE: ")
                cond = inp.lower()
                if cond == "yes" :
                    sql27 = "insert into users value('{}','{}','{}');".format(username_nusers,password_nusers,mode_nusers)
                    cur.execute(sql27)
                    con.commit()
                    print("TRANSACTION COMPLETED!")
                    print("your session expired!!")
                    exit()
                    
                else:
                    print("ok, last txn cancelled!!! your session expired!!")
                    exit()

            elif ch==8:
                print("8:REMOVE USER")
                username_rusers = input("ENTER USERS USERNAME(case sensitive): ")
                print("SELECTED TO DELETE THE USER = ",username_rusers,", ARE YOU SURE IF YES TYPE 'yes' else 'no'")
                sel = input("enter your choice: ")
                select7 = sel.lower()
                recconter = 0
                if select7 == 'yes':
                    for p in recc:
                        if p[0]== username_rusers:
                                print("username found")
                                sql14 = "delete from users where username = '{}';".format(username_rusers)
                                cur.execute(sql14)
                                con.commit()
                                recconter = recconter + 1
                                print("username deletted successfully")
                                
                    if recconter == 0:
                        print("USERNAME NOT FOUND")
                    else:
                        print("TRANSACTION COMPLETE!. SESSION EXPIRED PLZ RE LOGIN.")
                        exit()
                else:
                    print("transaction cancelled")
                            
            elif ch==0:
                con.close()
                exit()
    else:
        print("INVALID DATE ENTERED PLZ RELOGIN!!")
        exit()

#______________user code_________________________________________________
        
def usercode():
    print("login successfull")
    global day
    day =input("\nenter the day (** in lowercase only): ")
    while True:
        print("\n__________________________________________________________________________':;")
        print(" USER ACCOUNT!!!")
        print("\n1:ARRANGEMENT")
        print("3:VIEW FULL DATA/LIST(exel form) OF TEACHERS TIMETABLE")
        print("5:CHANGE DAY$$")
        print("0:EXIT")
        print("\nSELECTED DAY=",day)
        ch= int(input("enter your choice: "))

        if ch==1:
            selection1()
        elif ch==3:
            selection3()
        elif ch==5:
            selection5()
        elif ch==0:
            con.close()
            exit()


#+_FUNCTIONS_+_______________________________________________________________
def selection1():
    print("selected 1:ARRANGEMENT")
    absent = input("enter the absent teacher: ")   #teacher name 

    #free classes
    free_class = []
    s2= "select * from {} where class is not null and ename ='{}' ;".format(day,absent)
    cur.execute(s2)
    recs = cur.fetchall()
    for rec in recs:
        free_class.append(rec[2])

    free_teacher =[]#free teacher classes
    for a in free_class :
        s3= "select * from "+day+" where class is null and period IN ("+str(a)+");"
        cur.execute(s3)
        recds = cur.fetchall()
        free_teacher.append(recds)
    print('\n')

    absent_class = [] #absent class
    freeclass = tuple(free_class)
    sql1 = "select class,period from {} where ename ='{}' and period IN {}; ".format(day,absent,freeclass)
    cur.execute(sql1)
    cls = cur.fetchall()
    for n in cls:
        absent_class.append(n)

    #output
    for m in absent_class:
        print("_____________________")
        print("#in period = ",m[1],"to class = ",m[0])
        for k in free_teacher:
            for a in k:           
                if m[1]==a[2]:
                    print("you can send ",a[0],", free in ",a[2],"period.")
    print("\n ___ if no value found then assume it as 'games' ")

#___________________________________
def selection3():
    from datetime import date
    print("selected #3:VIEW INSERTED DATA/FULL LIST OF TEACHERS TIMETABLE")
    print("selected to print all data with selected day")
    sql5 = "select * from {}".format(day)
    cur.execute(sql5)
    alldat = cur.fetchall()
    print("1:to open in this software ")
    print("2:to open in MS EXEL ")
    may = int(input("ENTER YOUR CHOICE: "))
    if may==1:
        #print data in table format \\\\\\$ from greeksforgreeks ok::
        from tabulate import tabulate
        lst=[]
        for n in alldat:
            lst.append(list(n))
        head = ["employee_code","class","period"]
        print(tabulate(lst , headers=head, tablefmt="grid"))
    elif may==2:
        #done by me
        import csv
        filename= str(date.today())
        lst2=[["TEACHER_NAME","CLASS","PERIOD"]]
        for n in alldat:
            lst2.append(n)
        with open(filename+".csv","w",newline="")as file1:
            csvwriter= csv.writer(file1)
            
            csvwriter.writerows(lst2)
        print("exel saved in the file whare this ropgram is stored named as "+filename+".csv")
    else:
        print("unknown option entered")
#__________________________________
def selection5():
    global day
    newday = input("enter the new day (in lower case only): ")
    day = newday


#+_____________login________________________+
def passwod():
    global userpwd
    global errcont
    userpwd = str(input("ENTER YOUR PASSWORD(case sensitive): "))
    if n[1]== userpwd:
        if n[2]== "A":
            admincode()
        elif n[2]== "U":
            usercode()
        else:
            print("invalid input")
    else:
        print("wrong password typed =",errcont+1,"times.")
        errcont+=1
        if errcont <3:
            passwod()
        else:
            print("due to reaching maximum number of attempts, the current session is beeing expired.")
            quit()
#__        
usernam = input("ENTER YOUR USERNAME(case sensitive): ")
errcont = 0
sql18 = "select * from users;"
cur.execute(sql18)
recc = cur.fetchall()
leng =  len(recc)
currleng = 0
for n in recc:
    if n[0]==usernam:
        print("username verified")
        passwod()   
    else:
        currleng = currleng + 1
        if currleng == leng:
            print("username not found")
            print("session expired")
            quit()
            

    
