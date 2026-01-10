from datetime import datetime,timedelta
import json
import os
r = None
order = {}
qty = 0
dish = 0
amt_payble = 0 # ((Make Sure this is getting reset before bill processing))


# ----------LOAD VENDOR DATA FROM FILE IF EXISTS----------


if os.path.exists("vendor_menu.json"):
    with open("vendor_menu.json", "r") as f:
        vendor_menu = json.load(f)
else:
    vendor_menu = {
        "Dish number 1":100,
        "Dish number 2":80
    }

if os.path.exists("vendor_stock.json"):
    with open("vendor_stock.json", "r") as f:
        vendor_stock = json.load(f)
else:
    vendor_stock = {
        "Dish number 1":50,
        "Dish number 2":50
    }


vendor_orders = {
    101: {
        "dish": "Dish number 1",
        "qty": 2,
        "time": datetime.now().strftime("%H:%M"),
        "status": 0
    },
    102: {
        "dish": "Dish number 2",
        "qty": 1,
        "time": datetime.now().strftime("%H:%M"),
        "status": 0
    },
    103: {
        "dish": "Dish number 1",
        "qty": 3,
        "time": datetime.now().strftime("%H:%M"),
        "status": 0
    }
    
}
last_topup_time=datetime.now()
#order_no. --> order details (This will be stored in data base later)





#---------- VENDOR DASHBOARD FOR NOW (new feature can be added later)-------------

def vendor_dashboard():
    print("\n--------VENDOR DASHBOARD----------\n")
    print("1) View orders")
    print("2) Update order status")
    print("3) Top-Up Stock")
    print("4) Reset Mock orders")
    print("5) Logout")
    print("6) Add new dish to menu")


    r=int(input("Enter choice number: "))
    if r==1:
        view_vendor_orders()
    elif r==2:
        update_order_status()
    elif r==3:
        topup_stock()
    elif r==4:
        reset_mock_orders()
    elif r==5:
        start()
    elif r == 6:
        add_new_dish()

    else:
        vendor_dashboard()


#--------------VIEW ORDERS------------



def load_vendor_orders():
    if not os.path.exists("vendor_orders.json"):
        return {}
    with open("vendor_orders.json", "r") as f:
        return json.load(f)



def save_vendor_orders(data):
    with open("vendor_orders.json", "w") as f:
        json.dump(data, f, indent=4)


def view_vendor_orders():
    vendor_orders = load_vendor_orders()

    if not vendor_orders:
        print("No orders received yet")
    else:
        print("----INCOMING ORDERS------")
        for order_id in vendor_orders:
            o = vendor_orders[order_id]
            print(f"""
            Order No : {order_id}
            Dish     : {o['dish']}
            Quantity : {o['qty']}
            Time     : {o['time']}
            Status   : {"PREPARED" if o['status']==1 else "PENDING"}
            """)
    input("Press any key to Continue ")
    vendor_dashboard()

     


#-------UPDATE ORDER STATUS--------


def update_order_status():
    vendor_orders = load_vendor_orders()
    order_id = input("Enter Order number: ")

    if order_id in vendor_orders:
        vendor_orders[order_id]['status'] = 1
        save_vendor_orders(vendor_orders)
        print("Order marked as 'PREPARED' (Saved Permanently)")
    else:
        print("Invalid Order Number")

    input("Press any key to Continue")
    vendor_dashboard()



 #-----------TOP_UP STOCK-----------


def topup_stock():
    global last_topup_time
    now = datetime.now()

    # Load last topup time from a file if exists
    if os.path.exists("last_topup_time.json"):
        with open("last_topup_time.json", "r") as f:
            last_topup_time_str = f.read()
            if last_topup_time_str:
                last_topup_time = datetime.fromisoformat(last_topup_time_str)

    if now - last_topup_time < timedelta(hours=1):
        print("Top-Up allowed only once per hour")
        input("Press any key to continue")
        vendor_dashboard()
        return

    print("\nCurrent Stock:")
    for dish, qty in vendor_stock.items():
        print(f"{dish}: {qty}")

    choice = input("Press 1 to Top-Up or 0 to skip: ").strip()
    
    if choice == '1':
        # Let vendor select dish from menu to avoid typos
        print("\nSelect dish to top-up:")
        dishes_list = list(vendor_stock.keys())
        for i, d in enumerate(dishes_list, 1):
            print(f"{i}) {d}")
        try:
            dish_choice = int(input("Enter number of dish: "))
            if 1 <= dish_choice <= len(dishes_list):
                dish = dishes_list[dish_choice - 1]
                qty = int(input(f"Enter quantity to add for {dish}: "))
                if qty > 0:
                    vendor_stock[dish] += qty
                    save_vendor_stock()
                    last_topup_time = now

                    # Save last top-up time to file
                    with open("last_topup_time.json", "w") as f:
                        f.write(last_topup_time.isoformat())

                    print(f"Successfully Updated! New stock of {dish}: {vendor_stock[dish]}")
                else:
                    print("Quantity must be greater than 0")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter valid numbers")
    else:
        print("Top-Up skipped. Stock remains unchanged.")

    input("Press any key to continue")
    vendor_dashboard()




#--------------- ADD NEW DISH---------------

def save_vendor_menu():
    with open("vendor_menu.json", "w") as f:
        json.dump(vendor_menu, f, indent=4)

def save_vendor_stock():
    with open("vendor_stock.json", "w") as f:
        json.dump(vendor_stock, f, indent=4)



def add_new_dish():
    global vendor_menu, vendor_stock
    dish_name = input("Enter new Dish name: ")
    
    if dish_name in vendor_menu:
        print("Dish already exists! You can top-up stock instead.")
    else:
        try:
            price = int(input("Enter price of the dish: "))
            qty = int(input("Enter initial stock quantity: "))
        except ValueError:
            print("Please enter valid numbers for price and quantity.")
            add_new_dish()
            return
        
        vendor_menu[dish_name] = price
        vendor_stock[dish_name] = qty
        save_vendor_menu()             
        save_vendor_stock()  
        print(f"Dish '{dish_name}' added successfully with stock {qty} and price {price}")
    
    input("Press any key to continue")
    vendor_dashboard()




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
                if payment():
                    # Reduce stock automatically
                    for item, q in order.items():
                        if item in vendor_stock:
                            vendor_stock[item] -= q
                    save_vendor_stock()  # Save updated stock

                    print("YaY ! Payment Successful, Order Placed")   
                    order.clear()  # Clear previous order
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
                if payment():
                    # Reduce stock automatically
                    for item, q in order.items():
                        if item in vendor_stock:
                            vendor_stock[item] -= q
                    save_vendor_stock()  # Save updated stock

                    print("YaY ! Payment Successful, Order Placed")   
                    order.clear()  # Clear previous order
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


#---------storing orders:------------

def reset_mock_orders():
    mock_orders = {
        "101": {
            "dish": "Dish number 1",
            "qty": 2,
            "time": datetime.now().strftime("%H:%M"),
            "status": 0
        },
        "102": {
            "dish": "Dish number 2",
            "qty": 1,
            "time": datetime.now().strftime("%H:%M"),
            "status": 0
        },
        "103": {
            "dish": "Dish number 1",
            "qty": 3,
            "time": datetime.now().strftime("%H:%M"),
            "status": 0
        }
    }
    save_vendor_orders(mock_orders)
    print("Mock orders reset successfully")
    input("Press any key to continue")
    vendor_dashboard()



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

#import os
print(os.getcwd())
