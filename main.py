import awsinstance as awsins

def run_menu():
    flagsmenu = True
    while flagsmenu:
        
        opc = int(input(
            
            """
            1 - Run the instance
            2 - List
            3 - Start
            4 - Stop
            5 - Terminate
            """
            ))
        if opc == 1:
            flagsmenu == False
        elif opc == 2:
            flagsmenu == False
        elif opc == 3:
            flagsmenu == False

run_menu()