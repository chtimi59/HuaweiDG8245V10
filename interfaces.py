
#https://docs.python-requests.org/en/latest/user/quickstart/#raw-response-content
import base64
import re
import sys
import requests

conf_ip = None # "192.168.1.1"
conf_user = None # "user"
conf_pw = None # "admin"

def setConf(ip, user, pw):
    global conf_ip, conf_user, conf_pw
    conf_ip = ip
    conf_user = user
    conf_pw = pw

def hex_to_char(input):
    output = ""
    start = 0
    for m in re.finditer(r'\\x([0-9a-f]{2})', input):        
        value = int(m.group(1), 16)        
        output += input[start:m.start()] + chr(value)
        start = m.end()
    output += input[start:]
    return output

#print(hex_to_char("-\\x31-"))
#print(hex_to_char("\\x31"))
#print(hex_to_char("31"))
#print(hex_to_char(""))
#print(hex_to_char("\\x31\\x31"))
#print(hex_to_char("onze=\\x311,vingt-deux=\\x322"))

def formater(s):
    tmp = s.strip()
    # remove simple and ouble quote
    m = re.search(r'^[\"\'](.*)[\"\']', tmp)
    if not m is None:
        tmp = m.group(1).strip()
    return hex_to_char(tmp)

def getCookie():
    if conf_ip is None: raise Exception('invalid ip')
    if conf_user is None: raise Exception('invalid user')
    if conf_pw is None: raise Exception('invalid password')

    base64encode = lambda v : base64.b64encode(v.encode("ascii")).decode("ascii")
    
    r = requests.post(f"http://{conf_ip}/asp/GetRandCount.asp")
    r.encoding = 'utf-8'
    cnt = r.text.encode("ascii","ignore").decode()

    r = requests.post(f"http://{conf_ip}/login.cgi", data={
        "UserName": conf_user,
        "PassWord": base64encode(conf_pw),
        "Language": "english",
        "x.X_HW_Token": cnt
    })

    if r.status_code != 200:
        print(f"invalid HTTP {r.status_code }")
        sys.exit(1) 

    cookie = r.headers.get("Set-cookie")
    if cookie is None:
        print(f"Invalid token")
        sys.exit(1)

    return cookie

# useless
def getLanUserDevInfo(cookie):
    if conf_ip is None: raise Exception('invalid ip')

    r = requests.get(f"http://{conf_ip}/html/bbsp/common/GetLanUserDevInfo.asp", headers={
        'Cookie': cookie
    })
    r.encoding = 'utf-8'
    js = r.text.encode("ascii","ignore").decode()
    return js

def portMappingNew(cookie):
    r = requests.get(f"http://{conf_ip}/html/bbsp/portmapping/portmappingnew.asp", headers={
        'Cookie': cookie
    })
    r.encoding = 'utf-8'
    html = r.text.encode("ascii","ignore").decode()    
    
    m = re.search(r'<input type="hidden" name="onttoken" id="hwonttoken" value="([0-9a-f]+)">', html)
    if m is None:
        print(f"no onttoken")
        sys.exit(1)
    onttoken = m.group(1)

    WanIPPortMappingPortList = []    
    listOfMatchs = re.findall(r'new stPortMappingPortList\(([^\(\)]+)\)', html)
    for m in listOfMatchs:
        t = tuple(map(formater,  m.split(",")))
        if not 5 == len(t):
             continue # use to reset var (useless for use)                
        (domain,Protocol,InternalPort,ExternalPort,ExternalSrcPort) = t
        if domain == "thisDomain": 
            continue # use by appTempSelect() a function to give template (useless for use)
        if domain == "": 
            continue # use to reset var (useless for use)        
        WanIPPortMappingPortList.append({
            "domain": domain,
            "Protocol": Protocol,
            "InternalPort": InternalPort,
            "ExternalPort": ExternalPort,
            "ExternalSrcPort": ExternalSrcPort
        })

    WanIPPortMapping = []
    listOfMatchs = re.findall(r'new stPortMap\(([^\(\)]+)\)', html)
    for m in listOfMatchs:
        t = tuple(map(formater,  m.split(",")))
        if not 8 == len(t):
             continue # use to reset var (useless for use)        
        (domain,ProtMapEnabled,RemoteHost,RemoteHostRange,OperateRule,InClient,Description,ExternalIP) = t
        WanIPPortMapping.append({
            "domain": domain,
            "ProtMapEnabled": ProtMapEnabled,
            "RemoteHost": RemoteHost,
            "RemoteHostRange": RemoteHostRange,
            "OperateRule": OperateRule,
            "InClient": InClient,
            "Description": Description,
            "ExternalIP": ExternalIP
        })
    
    return (onttoken, WanIPPortMappingPortList, WanIPPortMapping)


def setPortMapping(cookie, onttoken, portMapping):
    url=f"http://{conf_ip}/html/bbsp/portmapping/complexajax.cgi?x={portMapping['domain']}&RequestFile=html/bbsp/portmapping/portmappingnew.asp"
    data={
        'x.PortMappingEnabled': portMapping["ProtMapEnabled"],
        'x.PortMappingDescription': portMapping["Description"], 
        'x.InternalClient': portMapping["InClient"], 
        'x.RemoteHost': portMapping["RemoteHost"], 
        'x.X_HW_RemoteHostRange': portMapping["RemoteHostRange"], 
        'x.X_HW_Token': onttoken,
    }   
    r = requests.post(url, data=data , headers={'Cookie': cookie})
    #print(r.status_code, formater(r.text))
