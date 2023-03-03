import PySimpleGUI as sg
import subprocess
import sys, os

sg.theme('SystemDefaultForReal')

#Constants
DEFAULT_SERVER = 'SERVER' #These 4 should be replaced with export/import with JSON files (except password, since plaintext password is bad.)
DEFAULT_USERNAME = 'USERNAME'
DEFAULT_PASSWORD = 'PASSWORD'
DEFAULT_DOMAIN = 'DOMAIN'
MENU_BAR = [['File', ['Reset Login Info', 'Exit']], ['Help', ['About', 'What is this?', 'NetEx Version']]]

program_files = os.environ['PROGRAMFILES(X86)']
necli = "C:/Program Files (x86)/SonicWall/SSL-VPN/NetExtender/NECLI.exe"
os.chdir('C:/Program Files (x86)/SonicWall/SSL-VPN/NetExtender/')
#necli = '{program_files}/SonicWall/SSL-VPN/NetExtender/NECLI.exe'
nestatus = subprocess.run([necli, 'showstatus'], capture_output=True).stdout.decode('utf-8').strip()

layout = [
    [sg.Menu(MENU_BAR, tearoff=False)],
    [sg.Text("Please input NetExtender Login Information")],
    [sg.Text("Sever Address:"), sg.Push(), sg.Input(f"{DEFAULT_SERVER}", k='-SERVER-')],
    [sg.Text("Username:"), sg.Push(), sg.Input(f"{DEFAULT_USERNAME}", k='-USERNAME-')],
    [sg.Text("Password:"), sg.Push(), sg.Input(f"{DEFAULT_PASSWORD}", k='-PASSWORD-')],
    [sg.Text("Domain:"), sg.Push(), sg.Input(f"{DEFAULT_DOMAIN}", k='-DOMAIN-')],
    [sg.StatusBar(nestatus, k='-STATUS-'), sg.Btn("Connect", k='-CONNECT-'), sg.Button("Disconnect", k='-DISCONNECT-')]
]

window = sg.Window("NetExtender", layout)


while True:
    event, values = window.read(timeout=500)
    if event in ['Exit', sg.WIN_CLOSED]:
        break
    if event == 'About':
        sg.Popup("TSM NetExtender GUI Replacement V0.1", title="About")
    if event == 'What is this?':
        sg.Popup("Hi, I'm Justin from TSM\nI got sick of NetExtender forgetting info so I\nmade this replacement UI for it.")
    if event == '-CONNECT-':
        #nestatus = 'Connecting...'
        #window.refresh()
        server = values['-SERVER-']
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        domain = values['-DOMAIN-']
        connect_arguments = f"connect -s {server} -u {username} -p {password} -d {domain}"
        print(connect_arguments)
        #connect = subprocess.call(['powershell', '-c', f"Start-Process '{necli}' -ArgumentList 'connect -s {server} -u {username} -p {password} -d {domain}'"], stdout=sys.stdout)#.stdout.decode('utf-8').strip()
        print(necli + " " + connect_arguments)
        print(os.getcwd())
        connect = subprocess.run([f'./NECLI.exe', f'connect -s {server} -u {username} -p {password} -d {domain}'],
                                  stdout=sys.stdout)  # .stdout.decode('utf-8').strip()
        window.refresh()
    if event == '-DISCONNECT-':
        subprocess.run([necli, 'disconnect'])
    if event == 'NetEx Version':
        sg.Popup("This will take a moment to pull info from windows\nThe program may be unresponsive during this time\nPress OK to continue.")
        version = subprocess.run(['powershell.exe', "(Get-WMIObject Win32_Product | Where-Object{$_.Name -eq 'Sonicwall NetExtender'}).Version"], capture_output=True)
        version = version.stdout.decode('utf-8').strip()
        sg.Popup(f"NetExtender version: {version}")
