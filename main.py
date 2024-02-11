
import tkinter as tk
import customtkinter as ctk
import os
import re
import configparser
from CTkMessagebox import CTkMessagebox
import psutil
import wmi




global startupp

global BBB
BBB = 0

startupp = 0

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


app=ctk.CTk()

app.geometry("400x400")
app.title("version 1.1.0")
app.maxsize(width=400 , height=400)
app.eval('tk::PlaceWindow . center')
app.resizable(0,0)
app.iconbitmap("AppICO.ico")


def use_regex(input_text):
    pattern = r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b"
    return re.search(pattern, input_text)


def set_ini(index1, val1 ):
    config = configparser.ConfigParser()
    config.read('FILE.INI')
    config['DNS']['d' + str(index1)] = val1
    with open('FILE.INI', 'w') as configfile:    # save
        config.write(configfile)
    L = []
    for x in range(0,index1):
 
        L.append( "d" + str(x+1) + ",")

    List_string = ''.join(L)
    config.set ('DNS_LIST', 'list',   List_string )
    
    with open('FILE.INI', 'w') as configfile:    # save
            config.write(configfile)  
    read_ini()
    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)




def read_ini():
    try:
        s = 0
        config = configparser.ConfigParser()
        config.read('FILE.INI')
        dns_list = config['DNS_LIST']['List']
        saved_d = []
        global saved_dns
        saved_dns = []
        dd=""
        for machine, query in zip(dns_list.split(','), config['DNS']):
            saved_d.append(query)
            saved_dns.append(config.get('DNS', query))
           
        
        last_dns = []
        if dns_list:
            last_dns = saved_dns[-1]
            combobox['values'] = saved_dns
            combobox.configure(values=saved_dns)
            if s == 0:
                combobox.set("Select a dns")
        else:
            combobox.configure(values=saved_dns)
            combobox.set("theres no saved")
    except FileNotFoundError:
        print("File 'data.txt' not found")
    except Exception as e:
        print("Error:", e)
    s = startupp  + 1
    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)

    return last_dns
    
def on_save():
    dns1 = dnsptxt.get()
    dns2 = dnsstxt.get()



    if_match1 = use_regex(dns1)
    if_match2 = use_regex(dns2)



    

    if if_match1:
        if dns2 == "" or if_match2:

            
                

            config = configparser.ConfigParser()
            config.read('FILE.INI')
            if not dns2 == '':
                dns_to_save = dns1 + " " + dns2
                dns_list = config.get('DNS_LIST', 'list')
            else:
                dns_to_save = dns1
                dns_list = config.get('DNS_LIST', 'list')
            for machine, query in zip(dns_list.split(','), config['DNS']):
                if_save = config.get('DNS', query)
                if dns_to_save == if_save:
                    dnsp.configure(validate="key", validatecommand=vcmd)

                    # Re-register validation for dnss Entry widget
                    dnss.configure(validate="key", validatecommand=vcmd)
                    CTkMessagebox(title="Warning!" ,message="your input is duplicate.",
                        icon="warning", option_1="ok")  
                    
                    return



            if not (dnsstxt.get() == "" and dnsptxt.get() == ""):
                set_ini(len(saved_dns)+1 , dnsptxt.get() + " " + dnsstxt.get() )
                dd = read_ini()
                config = configparser.ConfigParser()
                config.read('FILE.INI')
                dns_list = config.get('DNS_LIST', 'list')
            
                for machine, query in zip(dns_list.split(','), config['DNS']):
                    if dd == config.get('DNS', query):
                        combobox.set(config.get('DNS', query))
            
                
    else:  
        CTkMessagebox(title="Warning!", message="your input is invalid.",
                        icon="warning", option_1="ok")          
        
    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)
    




def on_delete():
    config = configparser.ConfigParser()
    config.read('FILE.INI')
    dns_list = config['DNS_LIST']['List']
    dns_to_del = combobox.get()
    
    for machine, query in zip(dns_list.split(','), config['DNS']):
        if dns_to_del == config.get('DNS', query):
        
            config.remove_option('DNS', query)
            with open('FILE.INI', 'w') as configfile:    # save
                config.write(configfile)  
            for  x in (dns_list.split(',')):
                if query == x:                    
                    new_dns_list =dns_list.replace(query + ",","")
                    config.set ('DNS_LIST', 'list',   new_dns_list )
                    combobox.set("Select a dns")
                    with open('FILE.INI', 'w') as configfile:    # save
                        config.write(configfile)  
    
    read_ini()
    dnsptxt.set("")
    dnsstxt.set("")
    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)

def on_set():
    try:
        dns1 = dnsptxt.get()
        dns2 = dnsstxt.get()

        if_match1 = use_regex(dns1)
        if_match2 = use_regex(dns2)

        
        if if_match1:
            if dns2 == "" or if_match2:
                
                    

                adapter= comboselect2.get()
                c = wmi.WMI()
                # Define the specific adapter description or caption you want to target
                adapter_description = adapter  # Example: "Local Area Connection"
                # Define the DNS server search order
                if not dns2 == "":
                    dns_servers = [dns1, dns2]  # Example: Google DNS servers
                else:
                    dns_servers = [dns1]
                # Iterate over network adapters to find the one with the specified description
                for adapter in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                    if adapter.Description == adapter_description:
                        # Set the DNS server search order for the specific adapter
                        adapter.SetDNSServerSearchOrder(dns_servers)
                        dnsp.configure(validate="key", validatecommand=vcmd)
                        dnss.configure(validate="key", validatecommand=vcmd)
                        CTkMessagebox(title="Success", message="DNS settings changed for adapter:" + adapter_description ,
                        icon="check", option_1="ok")
                        break
                    else:
                        dnsp.configure(validate="key", validatecommand=vcmd)
                        dnss.configure(validate="key", validatecommand=vcmd)
                        CTkMessagebox(title="Adapter not found",message="Adapter '{adapter_description}' not found or not enabled.",
                        icon="warning", option_1="ok")
                                
                # os.system('netsh interface ipv4 show interfaces')
                # os.system('netsh interface ip set dns name="'+adapter+'" static '+dns1+'')    
                # os.system('netsh interface ip add dns name="'+adapter+'"  '+dns2+' index=2')
            else:

                dnsp.configure(validate="key", validatecommand=vcmd)
                dnss.configure(validate="key", validatecommand=vcmd)
                CTkMessagebox(title="Warning!",message="your input is invalid.",
                        icon="warning", option_1="ok")
                

                
        else:
            dnsp.configure(validate="key", validatecommand=vcmd)

            dnss.configure(validate="key", validatecommand=vcmd)
            CTkMessagebox(title="Warning!", message="your input is invalid.",
                icon="warning", option_1="ok")
            
                

    except Exception as e:
        CTkMessagebox(title="Warning!",message=e,
                    icon="warning", option_1="ok")
    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)
    
    
def on_select(*args):
    dns_list = combobox.get().split()
    if not (combobox.get()== "Select a dns" or combobox.get()=="theres no saved"):
        

        
        if  len(dns_list) == 2:
            dnsptxt.set(dns_list[0])
            dnsstxt.set(dns_list[1])
        elif len(dns_list) == 1:
            dnsptxt.set(dns_list[0])
        else:
            return

    # Re-register validation for dnsp Entry widget
    dnsp.configure(validate="key", validatecommand=vcmd)

    # Re-register validation for dnss Entry widget
    dnss.configure(validate="key", validatecommand=vcmd)

    

    

def Only_Integer(S):
    global BBB
    if S == combobox.get():
        return True
    if S.isdigit() or (S == '.' ) or BBB == 1:
        BBB = 0
        return True
        
    return False
    

def click(key):
    global BBB
    
    BBB = 1
    
    
    
vcmd = (app.register(Only_Integer), '%S')

frame1= ctk.CTkFrame(app, bg_color="#242424",fg_color="#242424")  

frame1.rowconfigure((0,1), weight=1)
frame1.columnconfigure((0,1), weight=1)
frame1.pack()
dnsptxt=ctk.StringVar()
dnsp = ctk.CTkEntry(frame1, textvariable=dnsptxt,validate="key",validatecommand=vcmd)
dnsp.grid(row=0,column=0, padx = 10 , pady=10)
dnsstxt=ctk.StringVar()
dnss = ctk.CTkEntry(frame1, textvariable=dnsstxt,validate="key",validatecommand=vcmd)
dnss.grid(row=1,column=0, padx = 10 , pady=10)
save =ctk.CTkButton(frame1, text="save", command=on_save) 
save.grid(row=0,column=1,rowspan=2, padx = 10 , pady=10)
setb =ctk.CTkButton(app, text="set", command=on_set) 
setb.pack( padx = 10 , pady=10)



vals = []
comboselect = ctk.StringVar()
comboselect.trace_add('write', on_select)
combobox = ctk.CTkComboBox(app,values=vals,state="readonly",variable=comboselect , width=200)
combobox.pack(padx=10 , pady=10)
delb = ctk.CTkButton(app, text="delete", command=on_delete , fg_color="#b0092a" , hover_color="#400c16" ) 
delb.pack( padx = 10 , pady=10)
addrs = psutil.net_if_addrs()
adapter_list = list(addrs.keys())
adapter_Description= []
comboselect2 = ctk.StringVar()
c = wmi.WMI()
for adapter in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
    adapter_Description.append(adapter.Description)
combobox2 = ctk.CTkComboBox(app,values=adapter_Description,state="readonly",variable=comboselect2 , width=300)
combobox2.set(adapter_Description[0])
combobox2.pack(padx=10 , pady=10)

dnsp.bind("<BackSpace>", click)
read_ini()

app.mainloop()