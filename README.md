This is a Python script that will get a report on the current IOS version, updatime, boot image, IP, hostname, and model of Cisco equipment.

This script will save this information in a CSV file, so you must make sure that the CSV file exists in the desired location. 

For location, please edit YOUR_PATH within each section to your desired file location.

CREDENTIALS:

You have to edit YOUR_USERNAME and YOUR_PASSWORD for the one you use to SSH into the equipment.

QUANTITY and PROCESSING time:

You can add as many IP addresses as you want inside the ip_list section using the format '000.000.000.000'. The processing time will depend on how fast your network is and how many devices you're scanning.
I've used this script with 370+ Cisco switches/routers and I was able to complete it in about 12 minutes. 

EXCEPTIONS:

Almost every exception is already added to the script, however, there might be a new one that will cause the script to stop, if this happens to you, please take a screenshot of the error, 
and let me know so I can help you add that exception to the script. All exceptions (loggin_issues) will be stored on the file you specify under each exception.
