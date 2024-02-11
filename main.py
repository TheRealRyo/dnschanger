import tkinter as tk
import customtkinter as ctk
import os
import re
import configparser
from CTkMessagebox import CTkMessagebox

global startupp
startupp = 0

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


app=ctk.CTk()

app.geometry("400x400")
app.title("version 0.1")


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
    return last_dns
    
def on_save():
    dns1 = dnsptxt.get()
    dns2 = dnsstxt.get()

    if (len(dns1) >= 8) and (len(dns2) == '' or len(dns2) >= 8):
         

            config = configparser.ConfigParser()
            config.read('FILE.INI')
            dns_to_save = dnsptxt.get() + " " + dnsstxt.get()
            dns_list = config.get('DNS_LIST', 'list')
            for machine, query in zip(dns_list.split(','), config['DNS']):
                if dns_to_save == config.get('DNS', query):
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
        CTkMessagebox(message="your input is invalid.",
                  icon="warning", option_1="ok")
        
        




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

def on_set():
    dns1 = dnsptxt.get()
    dns2 = dnsstxt.get()
    if (len(dns1) >= 8) and (len(dns2) == '' or len(dns2) >= 8):
       
        os.system('netsh interface ipv4 show interfaces')
        os.system('netsh interface ip set dns name="Ethernet 2" static ' + dns1)    
        os.system('netsh interface ip add dns name="Ethernet 2"  '+ dns2 +' index=2')
    else:
        CTkMessagebox(message="your input is invalid.",
                  icon="warning", option_1="ok")

        
    
def on_select(*args):
    dns_list = combobox.get().split()
    if not (combobox.get()== "Select a dns" or combobox.get()=="theres no saved"):
        

        
        if  dns_list:
            dnsptxt.set(dns_list[0])
            dnsstxt.set(dns_list[1])
    
    

    

def Only_Integer(S):
    
    if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','.']:
        
        return True                                                       
    return False

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
combobox = ctk.CTkComboBox(app,values=vals,state="readonly",variable=comboselect)
combobox.pack(padx=10 , pady=10)
delb = ctk.CTkButton(app, text="delete", command=on_delete , fg_color="#b0092a" , hover_color="#400c16" ) 
delb.pack( padx = 10 , pady=10)

read_ini()

app.mainloop()