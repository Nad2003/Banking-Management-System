import mysql.connector
import random
from decimal import Decimal
from reportlab.platypus import SimpleDocTemplate , Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
try:
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nadeem@786",
        database="NEWDB"
    )
except mysql.connector.errors as err:
    print("CONNECTION FAILED : ",err )
    

cursor=connection.cursor()



# This Section only for the SQL Query 
Create_account_query="INSERT INTO ACCOUNT(account_id,NAME,ACCOUNT_TYPE) VALUES (%s,%s,%s) "
transection_query="INSERT INTO Transactions(transaction_id,account_id,amount) VALUES(%s,%s,%s)"
# show_query="SELECT amount FROM Transactions where transaction_id=%s"
transection_debit_update="UPDATE Transactions SET amount= %s WHERE  transaction_id=%s"

check_user="SELECT * FROM ACCOUNT AS AC INNER JOIN Transactions AS TC ON AC.account_id=TC.transaction_id"

delete_transection_query=" DELETE FROM Transactions WHERE transaction_id =%s"
delete_account=" DELETE FROM ACCOUNT WHERE account_id =%s"

# this function Gernrate an auto and unique account number 
def genrate():
    
    str="0123456789"
    ans=""
    for i in range(3):
        ans+=random.choice(str)
    return int("78103"+ans)


# def transection_history():
    


def Transfer_money():
    send=int(input("ENTER ACCOUNT NUMBER TO SEND MONEY  : "))
    recive=int(input("ENTER ACCOUNT NUMBER TO RECIEVE MONEY : "))
    cursor.execute("SELECT amount FROM Transactions WHERE transaction_id=%s",(send,))
    Sendrow =cursor.fetchone()
    cursor.execute("SELECT amount FROM Transactions WHERE transaction_id=%s",(recive,))
    recivedrow =cursor.fetchone()
    if Sendrow != None or recivedrow !=None:
        sendAmount=float(Sendrow[0])
        reciveAmount=float(recivedrow[0])
        
        if len(Sendrow)<1:
            print("ACCOUNT NOT EXISTS ")
            return
        if len(recivedrow)<1:
            print("ACCOUNT NOT EXISTS ")
            return
            
        if len(Sendrow)==1 and len(recivedrow)==1:
            amount=float(input("ENTER AMOUNT TO TRANSFER : "))
            if sendAmount > amount:
                sendAmount-=amount
                reciveAmount+=amount
                
                cursor.execute("UPDATE Transactions SET amount= %s WHERE  transaction_id=%s ",(sendAmount,send))
                cursor.execute("UPDATE Transactions SET amount= %s WHERE  transaction_id=%s ",(reciveAmount,recive))
                cursor.execute("INSERT INTO TRANSECTION_HISTORY(account_id,amount,TRANSECTION_TYPE) VALUES(%s,%s,%s)",(send,amount,"WIDROW"))
                cursor.execute("INSERT INTO TRANSECTION_HISTORY(account_id,amount,TRANSECTION_TYPE) VALUES(%s,%s,%s)",(recive,amount,"CRADIT"))
                connection.commit()
                print("AMOUNT IS TRANSFER SUCCESSFULLY ! ")
            else:
                print(f"ENTER A VALID AMOUNT {amount} IS NOT VALID  TO TRANSFER \n YOUR CURRENT AMOUNT IS {sendAmount}")
        else:
            print("-- ACCOUNTS NOT EXITS --")
            
    else:
        print("!--PLEASE CHECK ACCOUNT NUMBERS--!")
        
        
        
        

def deleteAccount():
    accountNum=int(input("ENTER YOUR ACCOUNT NUMBER TO DELETE : "))
    cursor.execute("SELECT amount FROM Transactions WHERE transaction_id=(%s)",(accountNum,))
    row =cursor.fetchone()
    if row != None:
        if len(row)>=1:
            print(F"ACCOUNT FOUND \nWITH INITIAL BALANCE IS {float(row[0])}")
            ch=input("ARE YOU SURE TO DELETE Y/N: \n")
            if ch=="Y":
                cursor.execute(delete_transection_query,(accountNum,))
                cursor.execute(delete_account,(accountNum,))
                cursor.execute("DELETE FROM TRANSECTION_HISTORY WHERE account_id=(%s)",(accountNum,))
                connection.commit()
                if float(row[0])>0:
                    print(f"YOUR ACCOUNT IS DELETED AND YOUR AMOUNT OF  : {float(row[0])} IS GIVEN")
                print("--- THANK YOU  ---- \n")
            else:
                print("--- THANKS FOR VISITING ---")
    else:
        print(f"ENTER A VALID ACCOUNT NUMBER {accountNum} NOT FOUND ") 

    
    

def checkBal():
    accountNumber=int(input("ENTER YOUR ACCOUNT NUMBER TO CHECK BALANCE: "))
    cursor.execute("SELECT amount FROM Transactions WHERE transaction_id=(%s)",(accountNumber,))
    row =cursor.fetchone()
    if row != None:
       
        print(f"TOTAL AMOUNT IN YOUR ACCOUNT  : {float(row[0])}")
    else:
        print(f"ENTER A VALID ACCOUNT NUMBER {accountNumber} NOT FOUND ") 


def transection_money():
    accountNumber=int(input("ENTER YOUR ACCOUNT NUMBER  : "))
    cursor.execute("SELECT amount FROM Transactions WHERE transaction_id=(%s)",(accountNumber,))
    row=cursor.fetchone()
    if row != None:
        balance=float(row[0])
        while True:
            print(f"DEBIT MONEY : 1")
            print(f"CRADIT  MONEY : 2")
            choice =int(input("ENTER YOUR CHOICE : "))
            
            if choice ==1:
                amount=float(input("ENTER AMOUNT TO DEBIT MORE THEN 50 : "))
                if amount > 0 and amount > 50:
                    val="DEBIT"
                    balance+=amount
                    cursor.execute(transection_debit_update,(balance,accountNumber))
                    
                    cursor.execute("INSERT INTO TRANSECTION_HISTORY(account_id,amount,TRANSECTION_TYPE) VALUES(%s,%s,%s)",(accountNumber,amount,val))
                    connection.commit()
                    print(f"YOUR TOTAL BALANCE IS : {balance} ")
                    break
                else:
                    print(f"PLEASE ENTER THE VALID AMOUNT {amount} IS NOT VALID :")
                    

            elif(choice ==2):
                amount=float(input("ENTER AMOUNT TO CRADIT MORE THEN 50 : "))
                if balance > amount and amount > 0 and amount >50:
                    val="widrow"
                    balance-=amount
                    cursor.execute(transection_debit_update,(balance,accountNumber))
                    cursor.execute("INSERT INTO TRANSECTION_HISTORY(account_id,amount,TRANSECTION_TYPE) VALUES(%s,%s,%s)",(accountNumber,amount,val))
                    connection.commit()
                    print(f"YOUR TOTAL BALANCE IS : {balance} ")
                    break
                else:
                    print(f"PLEASE ENTER THE VALID AMOUNT {amount} IS NOT VALID :")
            else:
                print(f"ENTER A VALID CHOICE {choice:^2} is not valid ")
    else:
        print(f"ENTER A VALID ACCOUNT NUMBER {accountNumber} NOT FOUND ")            
                 
def openingaccount(accountNumber):
    
    amount =int(input("ENTER SOME AMOUNT TO OPENING THE ACCOUNT : "))
    
    cursor.execute(transection_query,(accountNumber,accountNumber,amount))
    connection.commit()
    return amount
    
    
def Create_account():
    name =input("ENTER YOUR NAME : ").upper()
    acc_type=input("ENTER YOUR ACCOUNT TYPE - SAVING/ CURRENT : ").upper()
    account_number=genrate()
    cursor.execute(Create_account_query,(account_number,name,acc_type))
    connection.commit()
    print(f"ACCOUNT IS CREATED WITH ACCOUNT NUMBER: {account_number}")
    amount=openingaccount(account_number)
    print(f" ACCOUNT IS OPEN WITH BALANCE AMOUNT : {amount} ")
   
   
   
 
def admin():
    id=int(input("ENTER YOUR ID : "))
    if id==2003:
        cursor.execute(check_user)
        rows=cursor.fetchall()
        print("--------------------------------------------------------------------------------")
        for i,row in enumerate(rows ,start=1):
            
            print(f"{i:^3}| ACCOUNT ID : {row[0]:^3}| NAME: {row[1]:^3}| ACCOUNT TYPE: {row[2]:^3}| BALANCE: {row[5]:^3}|")
            i+=1
        print("--------------------------------------------------------------------------------")

def show_transection():
    accountNumber=int(input("ENTER YOUR ACCOUNT NUMBER TO SEE TRANSECTIONS : "))
    cursor.execute("SELECT * FROM TRANSECTION_HISTORY WHERE account_id=(%s)",(accountNumber,))
    rows =cursor.fetchall()
    print("YOUR ACCOUNT NUMBER IS:",accountNumber)
    print("---------------------------------------------------------")
    for row in rows:
        print(f"AMOUNT : {row[2]:^5}\n TRANSECTION : {row[3]:^3} \n DATE: {row[4].strftime('%d-%m-%Y ') :^3}\n TIME : {row[4].strftime('%H:%M:%S'):^3}")
        print("------------------")
    print("---------------------------------------------------------")


def BankStatment():
    accountNumber=int(input("ENTER YOUR ACCOUNT NUMBER TO SEE TRANSECTIONS : "))
    cursor.execute("SELECT * FROM TRANSECTION_HISTORY WHERE account_id=(%s)",(accountNumber,))
    rows =cursor.fetchall()
    pdf=SimpleDocTemplate(f"STATMENT_{accountNumber}.pdf")
    style=getSampleStyleSheet()
    content=[]
    content.append(Paragraph("BANK STATMENT ",style["Title"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"ACCOUNT No:{accountNumber} ",style["Normal"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"TRANSECTIONS ",style["Heading2"]))
    content.append(Spacer(1, 12))
    
    for row in rows:
        date=row[4].strftime('%d-%m-%Y ')
        time=row[4].strftime('%H:%M:%S')
        line=f"Rupees:{row[2]:<10}| Transection: {row[3]:<10} | DATE: {date :^3}\n TIME : {time:^3} "
        content.append(Paragraph(line,style["Normal"]))
        content.append(Spacer(1,5))
    pdf.build(content)
    
    print("PDF IS GENRATED SUCCESSFULLY !")
        
    
 

def main():
    while True:
        print(f"ENTER {1:^4} FOR CREAT ACCOUNT: ")
        print(f"ENTER {2:^4} FOR CRADIT / DABIT: ")
        print(f"ENTER {3:^4} FOR SHOW BALANCE IN  ACCOUNT: ")
        print(f"ENTER {4:^4} FOR ADMIN: ")
        print(f"ENTER {5:^4} FOR DELETE ACCOUNT : ")
        print(f"ENTER {6:^4} FOR TRANSFER MONEY TO ANOTHER ACCOUNT : ")
        print(f"ENTER {7:^4} FOR TRANSECTION HISTORY : ")
        print(f"ENTER {8:^4} BANK STATMENT : ")
        print(f"ENTER {9:^4} FOR EXIT : ")
        choice = int(input("ENTER YOUR CHOICE : "))
        match choice:
            case 1: Create_account()
            case 2: transection_money()
            case 3: checkBal()
            case 4: admin()
            case 5:deleteAccount()
            case 6:Transfer_money() 
            case 7: show_transection()
            case 8: BankStatment()
            case 9: break
main()       
            
    
connection.close()




