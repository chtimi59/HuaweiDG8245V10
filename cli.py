import argparse
import json
import re
import interfaces

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", default="192.168.1.1", type=str, help="router address")
    parser.add_argument("-u", "--user", default="user", type=str, help="user name")
    parser.add_argument("-p", "--pw", default="admin",  type=str, help="password")
    parser.add_argument("-f", "--forward", type=str, help="ip forward idx.enable, ex: -f 0.1") 
    args = parser.parse_args()
    interfaces.setConf(
        ip=args.ip,
        user=args.user,
        pw=args.pw
    )
    cookie = interfaces.getCookie()
    (onttoken, WanIPPortMappingPortList, WanIPPortMapping) = interfaces.portMappingNew(cookie)
    if args.forward is None:
        for idx in range(0, len(WanIPPortMapping)):
            print(f"{idx}:", json.dumps(WanIPPortMapping[idx], indent=4))
    else:
        m = re.search(r'^(\d+).(1|0)$', args.forward)
        if m is None:
            raise Exception('invalid forward expected: idx.enable\nexample: -f 0.1')
        else:
            idx = int(m.group(1))
            mode = m.group(2)
            WanIPPortMapping[idx]["ProtMapEnabled"] = mode
            interfaces.setPortMapping(cookie, onttoken, WanIPPortMapping[idx])
            (onttoken, WanIPPortMappingPortList, WanIPPortMapping) = interfaces.portMappingNew(cookie)
            print(json.dumps(WanIPPortMapping[idx], indent=4))

if __name__ == "__main__":
   main()
