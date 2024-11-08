"""
"""


import os
import pickle
import json
import base64
from app.crypto.asymmetric import AKE
from app.crypto.symmetric import SKE
from app.util import display
from dateutil import parser

from config import (
    PRIV_KEY_FILE, PUB_KEY_FILE, EVENTS_FILE, DATETIME_FORMAT, EXCHANGE_LIMIT
)



def app_credits() -> None:
    """
    Application credits and information display.
    """
    
    print("BITicket Server")
    print("© Maximus Milazzo\n")
    print("Create and release digital cryptographically secure tickets that users can exchange and redeem.")
    print('See the "README.txt" file for more information and to learn how it works.  Enjoy!')
    
    input()
    
    

def key_setup() -> None:
    """
    Application asymmetric cryptosystem initialization.
    """
    
    try:
        cipher = AKE()
        
        with open(PRIV_KEY_FILE, "wb") as f:
            f.write(cipher.private_key)
            
        with open(PUB_KEY_FILE, "wb") as f:
            f.write(cipher.public_key)
            
        display.clear()
        print("SUCCESS: System keys generated")
        
    except Exception as e:
        display.clear()
        print(f"ERROR: Key setup failed --\n{e}")
        
    input()
    
    

def db_setup() -> None:
    """
    """
    ### TODO



def main() -> None:
    """
    Program entry point.
    """
    
    display.clear()
    # clear initial display
    
    while True:
        print("Ticket Configration Menu\n")
        print("1 - Credits and information")
        print("2 - Database setup")
        print("3 - Key setup")
        print("x - Exit\n")
        # program options
        
        option = input("> ")
        display.clear()
        
        match option.lower():
            case "1":
                app_credits()
                # show credits and infromation

            case "2":
                db_setup()
                # set up server database
            
            case "3":
                key_setup()
                # setup global keys

            case "x":
                return
                # exit application
            
            case _:
                print("Error: Invalid input")
                input()
                # bad input

        display.clear()



if __name__ == "__main__":
    main()