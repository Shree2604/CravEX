from datetime import datetime,timedelta
import json
import os

r = None
order = {}
qty = 0
dish = 0
amt_payble = 0 # ((Make Sure this is getting reset before bill processing))
vendor_menu = {}
vendor_stock = {}

def read_int(prompt):
    while True:
        try:
            l= int(input(prompt))
            if l>=0 :
                return l
        except ValueError:
            print("Invalid input. Enter a positive integer.")

vendor_map = {
    1: "vendor1",
    2: "vendor2"
}
current_vendor = None

def vendor_file(filename):
    return f"{current_vendor}_{filename}"

#-------------------VENDOR LOAD & SAVE---------------


def load_vendor_menu():
    global vendor_menu
    file = vendor_file("menu.json")
    if os.path.exists(file):
        with open(file, "r") as f:
            vendor_menu = json.load(f)
    else:
        vendor_menu = {
            "Dish number 1": 100,
            "Dish number 2": 80
        }
        save_vendor_menu()


def save_vendor_menu():
    with open(vendor_file("menu.json"), "w") as f:
        json.dump(vendor_menu, f, indent=4)

def load_vendor_stock():
    global vendor_stock
    file = vendor_file("stock.json")
    if os.path.exists(file):
        with open(file, "r") as f:
            vendor_stock = json.load(f)
    else:
        vendor_stock = {dish: 50 for dish in vendor_menu}
        save_vendor_stock()

def save_vendor_stock():
    with open(vendor_file("stock.json"), "w") as f:
        json.dump(vendor_stock, f, indent=4)
      
last_topup_time=datetime.now()
#order_no. --> order details (This will be stored in data base later)

#---------- VENDOR DASHBOARD FOR NOW (new feature can be added later)-------------

def vendor_dashboard():

    load_vendor_menu()
    load_vendor_stock()

    print("\n--------VENDOR DASHBOARD----------\n")
    print("1) View orders")
    print("2) Update order status")
    print("3) Top-Up Stock")
    print("4) Logout")
    print("5) Add new dish to menu")


    r= input("Enter choice number: ")
    if r=='1':
        view_vendor_orders()
    elif r=='2':
        update_order_status()
    elif r=='3':
        topup_stock()
    elif r=='4':
        start()
    elif r=='5':
        add_new_dish()
    else:
        vendor_dashboard()


#--------------VIEW ORDERS------------

def load_vendor_orders():
    file = vendor_file("orders.json")
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}


def save_vendor_orders(data):
    with open(vendor_file("orders.json"), "w") as f:
        json.dump(data, f, indent=4)

def view_vendor_orders():
    vendor_orders = load_vendor_orders()

    if not vendor_orders:
        print("No orders received yet")
    else:
        print("----INCOMING ORDERS------")

    for order_id, o in vendor_orders.items():
        print(f"\nOrder No: {order_id}")

        # NEW FORMAT
        if "items" in o:
            for item, q in o["items"].items():
                print(f"  {item} x {q}")
            print(f"Total: ₹{o['total']}")

        # OLD / MOCK FORMAT
        else:
            print(f"  {o['dish']} x {o['qty']}")
            print("Total: ₹N/A")

        print(f"Time: {o['time']}")
        print(f"Status: {'PREPARED' if o['status'] else 'PENDING'}")

    input("Press any key to Continue ")
    vendor_dashboard()


#-------UPDATE ORDER STATUS--------


def update_order_status():
    vendor_orders = load_vendor_orders()
    order_id = input("Enter Order number: ").strip()

    if order_id in vendor_orders:
        vendor_orders[order_id]['status'] = 1
        save_vendor_orders(vendor_orders)
        print("Order marked as PREPARED")
    else:
        print("Invalid Order Number")

    input("Press any key to Continue")
    vendor_dashboard()


#-----------TOP_UP STOCK-----------


def topup_stock():
    global last_topup_time
    now = datetime.now()

    # Load last topup time from a file if exists
    if os.path.exists(vendor_file("last_topup_time.json")):
        with open(vendor_file("last_topup_time.json"), "r") as f:

            last_topup_time_str = f.read()
            if last_topup_time_str:
                last_topup_time = datetime.fromisoformat(last_topup_time_str)

    if now - last_topup_time < timedelta(minutes=1):      #can be fixed later
        print("Top-Up allowed only once per minute")
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
            dish_choice = read_int("Enter number of dish: ")
            if 1 <= dish_choice <= len(dishes_list):
                dish = dishes_list[dish_choice - 1]
                qty = read_int(f"Enter quantity to add for {dish}: ")
                if qty > 0:
                    vendor_stock[dish] += qty
                    save_vendor_stock()
                    last_topup_time = now

                    # Save last top-up time to file
                    with open(vendor_file("last_topup_time.json"), "w") as f:

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


def add_new_dish():
    global vendor_menu, vendor_stock
    dish_name = input("Enter new Dish name: ")
    
    if dish_name in vendor_menu:
        print("Dish already exists! You can top-up stock instead.")
    else:
        try:
            price = read_int("Enter price of the dish: ")
            qty = read_int("Enter initial stock quantity: ")
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
    
    if p == '1' :
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

    global order
    order = {}


    global current_vendor
    current_vendor = "vendor1" 

    load_vendor_menu()
    load_vendor_stock()


    m1 = vendor_menu #{"Dish no. 1" : 100, "Dish no. 2" : 80}
    while True:
        print("Menu :", m1)
        dish = input("Enter Dish name")
        qty = read_int("Enter Quantity")

        # if r == 1:
        #     dish = "Dish no. 1"
        order[dish] = order.get(dish, 0) + qty

        # elif r == 2:
        #     dish = "Dish no. 2"
        #     order[dish] = order.get(dish, 0) + qty

        # else:
        #     print("Masti Nahi")
        #     continue

        more = input("Add more dishes? (y/n): ")
        if more.lower() != 'y':
            break

    
    r = input("Press 1 to Review order and Checkout or Press 0 to Modify Order")
    if r == '1' :
            amt_payble = 0
            print("Order Summary :",order)
        
            for item in order :
                amt_payble = amt_payble + int(m1[item])*order[item]

            print(f"Total = {amt_payble}")

            r = input("Press 1 to Proceed to Payment or Press 0 to Cancel Order")
            if r == '1' :
                # print('''Sending order details to Vendor for Confirmation ....
                #          Vendor Confirmed the Availability 
                #          Estimated Time : 30 mins''')
                if payment():
                    # Reduce stock automatically
                    for item, q in order.items():
                        #stock_item = item.replace("Dish no.", "Dish number")

                        if item not in vendor_stock:
                            print(f"{item} not available in stock")
                            menu1()
                            return

                        if vendor_stock[item] < q:
                            print(f"Not enough stock for {item}")
                            menu1()
                            return


                    for item, q in order.items():
                        #stock_item = item.replace("Dish no.", "Dish number")
                        vendor_stock[item] -= q

                    save_vendor_stock()

                    print("YaY ! Payment Successful, Order Placed")  
                    orders = load_vendor_orders()
                    order_id = str(len(orders) + 101)

                    orders[order_id] = {
                    "items": order.copy(),   # FULL ORDER
                    "total": amt_payble,
                    "time": datetime.now().strftime("%H:%M"),
                    "status": 0
                                       }
                    
                    save_vendor_orders(orders)
 
                    order.clear()  # Clear previous order
                    r = input("Press Any key to Continue")
                    student_dashboard()

                else :
                    print("Payment Failed") 
                    menu1()
                           
            elif r == '0' :
                student_dashboard()
            
            else :
                print("Masti Nhi")
                
   
    elif r == '0' :
        print("Current Order :",order)
        print("To Remove an Item Select it and Enter its Quantity = 0")
        menu1()
    
    else :
        print("Masti Nhi")
    


def menu2() :

    global order
    order = {}

    global current_vendor
    current_vendor = "vendor2"
    load_vendor_menu()
    load_vendor_stock()

    m2 = vendor_menu #{"Dish no. 1" : 120, "Dish no. 2" : 140}
    while True:
        print("Menu :", m2)
        dish = input("Enter Dish name")
        qty = read_int("Enter Quantity")

        # if r == 1:
        #     dish = "Dish no. 1"
        order[dish] = order.get(dish, 0) + qty

        # elif r == 2:
        #     dish = "Dish no. 2"
        #     order[dish] = order.get(dish, 0) + qty

        # else:
        #     print("Masti Nahi")
        #     continue

        more = input("Add more dishes? (y/n): ")
        if more.lower() != 'y':
            break

    
    r = input("Press 1 to Review order and Checkout or Press 0 to Modify Order")

    if r == '1' :
            amt_payble = 0
            print("Order Summary :",order)
        
            for item in order :
                amt_payble = amt_payble + int(m2[item])*order[item]

            print(f"Total = {amt_payble}")
            r = input("Press 1 to Proceed to Payment or Press 0 to Cancel Order")
            if r == '1' :
                # print('''Sending order details to Vendor for Confirmation ....
                #          Vendor Confirmed the Availability 
                #          Estimated Time : 30 mins''')
                if payment():
                    # Reduce stock automatically
                    for item, q in order.items():
                        #stock_item = item.replace("Dish no.", "Dish number")

                        if item not in vendor_stock:
                            print(f"{item} not available in stock")
                            menu2()
                            return

                        if vendor_stock[item] < q:
                            print(f"Not enough stock for {item}")
                            menu2()
                            return


                    for item, q in order.items():
                        #stock_item = item.replace("Dish no.", "Dish number")
                        vendor_stock[item] -= q
                   
                    save_vendor_stock()

                    # Save updated stock

                    print("YaY ! Payment Successful, Order Placed")
                    orders = load_vendor_orders()
                    order_id = str(len(orders) + 101)
                    orders[order_id] = {
                        "items": order.copy(),   # FULL ORDER
                        "total": amt_payble,
                        "time": datetime.now().strftime("%H:%M"),
                        "status": 0
                    }


                    save_vendor_orders(orders)

                    order.clear()  # Clear previous order
                    r = input("Press Any key to Continue")
                    student_dashboard()


                else :
                    print("Payment Failed") 
                    menu2()
                           
            elif r == '0' :
                student_dashboard()
            
            else :
                print("Masti Nhi")
   
    elif r == '0' :
        print("Current Order :",order)
        print("To Remove an Item Select it and Enter its Quantity = 0")
        menu2()
    
    else :
        print("Masti Nhi")
    


# -----------------User Dashboards--------------------

def student_dashboard() :
    
    r = input("Enter 1 to View most Ordered Dishes or Press 2 to Browse Vendor or any other button to Logout\n")
    if r == '1' :
        most_ordered()

    elif r == '2':
        r = input("Press 1 for Vendor no.1 or 2 for Vendor no.2\n")
        if r == '1' :
            menu1()


        elif r == '2' :
            menu2() 

        else :
            print("You Pressed the Wrong Button\n")
            student_dashboard()

    else :
        print("See You Again")
        start()


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
    

        global current_vendor

        if username in vendors_data:
            if vendors_data[username] == password:
                vendor_username_map = {
                    "vendor01": "vendor1",
                    "vendor02": "vendor2"
                }
                current_vendor = vendor_username_map[username]
                vendor_dashboard()
            else:
                print("Incorrect Password")
        else:
            print("Vendor not found")
    
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

# def reset_mock_orders():
#     mock_orders = {
#         "101": {
#             "dish": "Dish number 1",
#             "qty": 2,
#             "time": datetime.now().strftime("%H:%M"),
#             "status": 0
#         },
#         "102": {
#             "dish": "Dish number 2",
#             "qty": 1,
#             "time": datetime.now().strftime("%H:%M"),
#             "status": 0
#         },
#         "103": {
#             "dish": "Dish number 1",
#             "qty": 3,
#             "time": datetime.now().strftime("%H:%M"),
#             "status": 0
#         }
#     }
#     save_vendor_orders(mock_orders)
#     print("Mock orders reset successfully")
#     input("Press any key to continue")
#     vendor_dashboard()


#----------------------Start--------------------------

def start () :
    r = (input("Press 1 to Regiser or 2 to Login or any Else Key to Exit\n"))

    if r == '1' :
        register()
    
    elif r == '2' :
        login()
    
    else :
        print("See You Again")
#-----------------------------------------------------

start()
