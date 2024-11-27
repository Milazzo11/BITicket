import sqlite3
import pickle
from config import DB_FILE

from typing import List


def register(event_id: str, ticket_number: int) -> None:
    """
    Store ticket issue data.
    """
    ### literally just increment the "issued tickets" data by 1
    #### ALSO if "returned list" in data contains the ticket number, remove it

    # Connect to the database
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    # Step 1: Increment the issued count
    cursor.execute("""
        UPDATE events
        SET issued = issued + 1
        WHERE id = ?
    """, (event_id,))
    
    # Step 2: Fetch the current returned list
    cursor.execute("""
        SELECT returned FROM event_data WHERE event_id = ?
    """, (event_id,))
    row = cursor.fetchone()

    # Step 3: Deserialize the returned list from the database
    returned_list: List = pickle.loads(row[0])

    # Step 4: Remove the ticket_number from the returned list if it exists
    if ticket_number in returned_list:
        returned_list.remove(ticket_number)

        # Step 5: Serialize the updated returned list and update the database
        cursor.execute("""
            UPDATE event_data
            SET returned = ?
            WHERE event_id = ?
        """, (pickle.dumps(returned_list), event_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()






def cancel(event_id: str, ticket_number: int) -> bool:
    """
    Cancel a ticket.
    """
    ### alter the cancel bitstring to reflect that the ticket has been returned N+1 times

    ## the cancel bytestring rught now looks like:


    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch the redemption bitstring for the event
    cursor.execute("""
        SELECT cancel_bitstring FROM event_data
        WHERE event_id = ?
    """, (event_id,))
    row = cursor.fetchone()

    cancel_bitstring = bytearray(row[0])
    ### TODO -- TEMP BYTE, NOT BIT ARRAY

    if cancel_bitstring[ticket_number] == 255: ### TODO - FIX THIS -- TEMP MAX USING BYTE ARRAY
        conn.close()
        return False

    cancel_bitstring[ticket_number] += 1

    # Update the database with the new cancel bitstring
    cursor.execute("""
        UPDATE event_data
        SET cancel_bitstring = ?
        WHERE event_id = ?
    """, (bytes(cancel_bitstring), event_id))

    conn.commit()
    conn.close()
    return True



def reissue(event_id: str, ticket_number: int) -> None:
    """
    """
    ### add this ticket number to the "returned tickets" list for re-registration

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch the current returned list from the database
    cursor.execute("""
        SELECT returned
        FROM event_data
        WHERE event_id = ?
    """, (event_id,))
    row = cursor.fetchone()

    # Unpickle the returned list
    returned_list: List = pickle.loads(row[0])
    returned_list.append(ticket_number)

    # Update the database with the new returned list
    cursor.execute("""
        UPDATE event_data
        SET returned = ?
        WHERE event_id = ?
    """, (pickle.dumps(returned_list), event_id))

    conn.commit()
    conn.close()




def redeem(event_id: str, ticket_number: int) -> bool:
    """
    Alter the redemption bitstring for the associated ticket number bit to reflect a redemption.
    """

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch the redemption bitstring for the event
    cursor.execute("""
        SELECT redeemed_bitstring FROM event_data
        WHERE event_id = ?
    """, (event_id,))
    row = cursor.fetchone()


    redeemed_bitstring = bytearray(row[0])
    ### TODO -- TEMP BYTE, NOT BIT ARRAY

    if redeemed_bitstring[ticket_number] == 1:
        conn.close()
        return False

    # Mark the ticket as redeemed (set the bit at the ticket number index to 1)
    redeemed_bitstring[ticket_number] = 1

    # Update the database with the new redeemed bitstring
    cursor.execute("""
        UPDATE event_data
        SET redeemed_bitstring = ?
        WHERE event_id = ?
    """, (bytes(redeemed_bitstring), event_id))

    conn.commit()
    conn.close()
    return True


def verify(event_id: str, ticket_number: int) -> bool:
    """
    Verify that the associated ticket number bit in the redemption bitstring is a 1-bit.
    """

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch the redemption bitstring for the event
    cursor.execute("""
        SELECT redeemed_bitstring FROM event_data
        WHERE event_id = ?
    """, (event_id,))
    row = cursor.fetchone()

    redeemed_bitstring = bytearray(row[0])

    # Check if the ticket has been redeemed (i.e., bit at ticket_number index is 1)
    if redeemed_bitstring[ticket_number] == 1:
        conn.close()
        return True

    conn.close()
    return False