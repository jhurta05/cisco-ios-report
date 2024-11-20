from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from netmiko.exceptions import AuthenticationException
from socket import error as socket_error
import errno
import re
import logging


#List of cisco switches ip addresses, add as many as you want in the same format.
ip_list = [
'192.168.0.1',  '192.168.0.2'
]

#Enable Netmiko logging level DEBUG
logging.basicConfig(filename=r'C:\Users\YOUR_PATH\netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#List where informations will be stored
devices = []

#Clearing the old data from the CSV file and writing the headers
f = open(r"C:\Users\YOUR_PATH\IOS-Report.csv", "w+")
f.write("IP Address, Hostname, Uptime, Current_Version, Current_Image, Serial_Number, Device_Model, Device_Memory")
f.write("\n")
f.close()

#Clearing the old data from the CSV file and writing the headers
f = open(r"C:\Users\YOUR_PATH\Login_issues.csv", "w+")
f.write("IP Address, Status")
f.write("\n")
f.close()



#loop all ip addresses in ip_list
for ip in ip_list:
    cisco = {
    'device_type':'cisco_ios',
    'ip':ip,
    'username':'YOUR_USERNAME',     #SSH username
    'password':'YOUR_PASSWORD',  #SSH password
    'secret': 'YOUR_PASSWORD',   #SSH_enable_password
    'ssh_strict':False,  
    'fast_cli':False,
    }
    
    #handling exceptions errors
    
    try:
        net_connect = ConnectHandler(**cisco)
    except NetMikoTimeoutException:
        f = open(r"C:\Users\YOUR_PATH\login_issues.csv", "a")
        f.write(ip + "," + "Device Unreachable/SSH not enabled")
        f.write("\n")
        f.close()
        continue
    except AuthenticationException:
        f = open(r"C:\Users\YOUR_PATH\login_issues.csv", "a")
        f.write(ip + "," + "Authentication Failure")
        f.write("\n")
        f.close()
        continue
    except SSHException:
        f = open(r"C:\Users\YOUR_PATH\login_issues.csv", "a")
        f.write(ip + "," + "SSH not enabled")
        f.write("\n")
        f.close()
        continue
    except socket_error as socket_err:
        f = open(r"C:\Users\YOUR_PATH\login_issues.csv", "a")
        f.write(ip + "," + "Connection Refused")
        f.write("\n")
        f.close()
        continue
    try:
        net_connect.enable()

    #handling exceptions errors        
    except ValueError:
        f = open(r"C:\Users\YOUR_PATH\login_issues.csv", "a")
        f.write(ip + "," + "Could be SSH Enable Password issue")
        f.write("\n")
        f.close()
        continue
    

    # execute show version on router and save output to output object    
    sh_ver_output = net_connect.send_command('show version', expect_string=r"#", read_timeout=8000)   

    #finding hostname in output using regular expressions
    regex_hostname = re.compile(r'(\S+)\suptime')
    hostname = regex_hostname.findall(sh_ver_output)

    #finding uptime in output using regular expressions
    regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
    uptime = regex_uptime.findall(sh_ver_output)
    uptime = str(uptime).replace(',' ,'').replace("'" ,"")
    uptime = str(uptime)[1:-1] 
    
    
    #finding version in output using regular expressions
    regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
    version = regex_version.findall(sh_ver_output)

    #finding serial in output using regular expressions
    regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
    serial = regex_serial.findall(sh_ver_output)

    #finding ios image in output using regular expressions
    regex_ios = re.compile(r'System\simage\sfile\sis\s"([^ "]+)')
    ios = regex_ios.findall(sh_ver_output)

    #finding model in output using regular expressions
    regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
    model = regex_model.findall(sh_ver_output)
    

    #finding the router's memory using regular expressions
    regex_memory = re.search(r'with (.*?) bytes of memory', sh_ver_output)#.group(1)
    memory = regex_memory
    
    
    
    #append results to table [hostname,uptime,version,serial,ios,model]
    devices.append([ip, hostname,uptime,version,ios,serial,model,memory])
    


#print all results (for all switches) on screen    
for i in devices:
    i = ", ".join(map(str,i))     
    f = open(r"C:\Users\YOUR_PATH\IOS-Report.csv", "a")
    f.write(i)
    f.write("\n")
    f.close()
