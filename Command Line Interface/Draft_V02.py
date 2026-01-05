
# Hardcoding Username & Password for the sake of Demonstration and formation of initial Draft.

#students_data = {"student01":"1234"}

#vendors_data = {"vendor01" : "5678"}
import json

r = None
order = {}
qty = 0
dish = 0
amt_payble = 0 # ((Make Sure this is getting reset before bill processing))


# ---------------Under Construction Zone--------------

def vendor_dashboard() :
    print("Sorry this one is currently under Construction")
    start()



#-------Payment (Subject to Heavy Modification)-------

def payment() :
    p = input("Enter 1 to make Payment or 0 to Cancel payment\n")
    
    if int(p) == 1 :
        return 1 
    
    else :
        return 0


#-------------------Most Ordered----------------------

def most_ordered() :
   print('''1. Dish no.2 of Vendor no. 1
            2. Dish no.1 of Vendor no. 2''')
   
   r = input("Press Any Key to continue Ordering")
   student_dashboard()

#-----------------------Menus-------------------------

def menu1() :
    m1 = {"Dish no. 1" : 100, "Dish no. 2" : 80}
    print("Menu :",m1)
    r = int(input("Enter Dish no."))
    qty = int(input("Enter Quantity"))

    if r == 1 :
        dish = "Dish no. 1"
        order[dish] = qty
    
    elif r == 2 :
        dish = "Dish no. 2"
        order[dish] = qty
    
    else :
        print("Masti Nahi")
        menu1()
    
    r = int(input("Press 1 to Review order and Checkout or Press 0 to Modify Order"))
    if r == 1 :
            amt_payble = 0
            print("Order Summary :",order)
        
            for item in order :
                amt_payble = amt_payble + int(m1[item])*order[item]

            print(f"Total = {amt_payble}")

            r = int(input("Press 1 to Proceed to Payment or Press 0 to Cancel Order"))
            if r == 1 :
                print('''Sending order details to Vendor for Confirmation ....
                         Vendor Confirmed the Availability 
                         Estimated Time : 30 mins''')
                if payment() :
                    print("YaY ! Payment Successful, Order Placed")   
                    r = input("Press Any key to Continue")
                    student_dashboard()

                else :
                    print("Payment Failed") 
                    menu1()
                           
            elif r == 0 :
                student_dashboard()
            
            else :
                print("Masti Nhi")
                
   
    elif r == 0 :
        print("Current Order :",order)
        print("To Remove an Item Select it and Enter its Quantity = 0")
        menu1()
    
    else :
        print("Masti Nhi")
    


def menu2() :
    m2 = {"Dish no. 1" : 120, "Dish no. 2" : 140}
    print("Menu :",m2)
    r = int(input("Enter Dish no."))
    qty = int(input("Enter Quantity"))

    if r == 1 :
        dish = "Dish no. 1"
        order[dish] = qty
    
    elif r == 2 :
        dish = "Dish no. 2"
        order[dish] = qty
    
    else :
        print("Masti Nahi")
        menu2()
    
    r = int(input("Press 1 to Review order and Checkout or Press 0 to Modify Order"))

    if r == 1 :
            amt_payble = 0
            print("Order Summary :",order)
        
            for item in order :
                amt_payble = amt_payble + int(m2[item])*order[item]

            print(f"Total = {amt_payble}")
            r = int(input("Press 1 to Proceed to Payment or Press 0 to Cancel Order"))
            if r == 1 :
                print('''Sending order details to Vendor for Confirmation ....
                         Vendor Confirmed the Availability 
                         Estimated Time : 30 mins''')
                if payment() :
                    print("YaY ! Payment Successful, Order Placed")   
                    r = input("Press Any key to Continue")
                    student_dashboard()

                else :
                    print("Payment Failed") 
                    menu2()
                           
            elif r == 0 :
                student_dashboard()
            
            else :
                print("Masti Nhi")
   
    elif r == 0 :
        print("Current Order :",order)
        print("To Remove an Item Select it and Enter its Quantity = 0")
        menu2()
    
    else :
        print("Masti Nhi")
    




# -----------------User Dashboards--------------------

def student_dashboard() :
    
    #print("Under Construction")
    r = int(input("Enter 1 to View most Ordered Dishes or Press 2 to Browse Vendor\n") )
    if r == 1 :
        most_ordered()

    elif r == 2:
        r = int(input("Press 1 for Vendor no.1 or 2 for Vendor no.2\n"))
        if r == 1 :
            menu1()


        elif r == 2 :
            menu2() 

        else :
            print("Masti nahi")

    else :
        print("Masti nahi")


# --------------------- Login ------------------------

def login() :

    user_type = input("Enter 'S' or 's' for student else Enter 'V' or 'v' for Vendor ") 
    # We'll Query the required Database based on the User Type

    username = input("Enter Username :")
    password = input("Enter Password :")

    if user_type == 's' or user_type == 'S' :

        f = open("students_data.json","r")
        data = f.read()
        f.close()

        students_data = json.loads(data)

        if username in students_data :

            if students_data[username] == password :
                student_dashboard()
            
            else :
                print("Incorrect Password")
                r = input("Preess Any Key to Continue")
                login()

        else : 
            print("Incorrect Username")
            r = input("Preess Any Key to Continue") 
            login()  

    elif user_type == 'v' or user_type == 'V' :

        f1 = open("vendors_data.json","r")
        data = f1.read()
        f1.close()

        vendors_data = json.loads(data)

        if username in vendors_data :

            if vendors_data[username] == password :
                vendor_dashboard()

            else :
                print("Incorrect Password")
                r = input("Preess Any Key to Continue") 
                login()

        else : 
            print("Incorrect Username")
            r = input("Preess Any Key to Continue") 
            login()  
    
    else : 
        print("Masti nahi")
        r = input("Preess Any Key to Continue")
        login() 


#----------------New User Registeration---------------

def register() :

    

    user_type = input("Enter 'S' or 's' for student else Enter 'V' or 'v' for Vendor\n") 
    # We'll Modify the required Database based on the User Type

    if user_type == 's' or user_type == 'S' :

        f = open("students_data.json","r")
        data = f.read()
        f.close()

        students_data = json.loads(data)

        u1 = input("Enter Username\n")
        if (not u1 in students_data) :
            p1 = input("Enter your Password\n")
            p2 = input("Confirm Password\n")

            if p1 == p2 :
                students_data[u1]=p1
                data1 = json.dumps(students_data)
                f = open("students_data.json","w")
                f.write(data1)
                f.close()
                print("Registration Successful")
                start()
            
            else :
                print("Both of Your Entered Passwords must match")
                r = input("Preess Any Key to Continue") 
                register()




        else : 
            print("ENTERED Username Not AVAILABLE")
            r = input("Preess Any Key to Continue") 
            register()  

    elif user_type == 'v' or user_type == 'V' :

        f1 = open("vendors_data.json","r")
        data = f1.read()
        f1.close()

        vendors_data = json.loads(data)

        v1 = input("Enter Username\n")
        if (not v1 in vendors_data) :
            vp1 = input("Enter your Password\n")
            vp2 = input("Confirm Password\n")

            if vp1 == vp2 :
                vendors_data[v1]=vp1
                data1 = json.dumps(vendors_data)
                f = open("vendors_data.json","w")
                f.write(data1)
                f.close()
                print("Registration Successful")
                start()
            
            else :
                print("Both of Your Entered Passwords must match")
                r = input("Preess Any Key to Continue") 
                register()  

        else :
            print("ENTERED Username Not AVAILABLE")
            r = input("Preess Any Key to Continue") 
            register()


    else : 
        print("Masti nahi")
        r = input("Preess Any Key to Continue")
        register()

    

#----------------------Start--------------------------

def start () :
    r = int(input("Press 1 to Regiser or 2 to Login\n"))

    if r == 1 :
        register()
    
    elif r == 2 :
        login()
    
    else :
        print("Mast Nahi")
#-----------------------------------------------------

start()

# import os 
# print(os.getcwd())