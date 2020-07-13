#--  This program makes use of Bash commands to activate the night light. During the day time, when we want to avoid falling asleep, we need less red pixels and more of the blue ones. During the night, it is the opposite as we need less blue pixels so as to not get our eyes strained. This program gives the user five options.


import os
import subprocess
import time

def input_backlight_value():
    os.system('dconf write /org/gnome/settings-daemon/plugins/color/night-light-enabled true')

    b_light = int(input("\n\n1. High Red\n2. Normal Night\n3. Off\n4. Cooler\n5. High Blue\n"))

    dc_nlight = {
        1 : 1000,
        2 : 4000,
        3 : 6500,
        4 : 8000,
        5 : 10000
    }

    time.sleep (0.8)
    command = "gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature " + str (dc_nlight [b_light])

    os.system(command)
    #print (command)

#--

def master():
    stat = int(input("1. On\n2. Off\n"))
    if (stat == 2):
        light_off()
    elif (stat == 1):
        input_backlight_value()
#--

def light_off():
    os.system('gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature 6500')
    time.sleep (0.8)
    os.system('dconf write /org/gnome/settings-daemon/plugins/color/night-light-enabled false')

#--

def hibernate_system():
    mins = int(input("Minutes: "))
    sec  = int(input("Seconds: "))

    total_time = (mins * 60) + sec
    time.sleep(total_time)

    os.system ('systemctl suspend')

#--

import os
import getpass as gp
import base64
def encrypt():
    pwd = gp.getpass (": ")
    pwd_b = str.encode (pwd)
    enc = base64.b64encode (pwd_b)
    pwd = None
    pwd_b = None
    print ("Encrypted --> {}".format (enc))
    dec = base64.b64decode (enc)
    print ("Decrypted --> {}".format (dec))

#--

if __name__ == '__main__':
    master()


