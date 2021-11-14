# Huawei DG8245V10 CLI

This wifi-router has an HTTP user interface, but as far I known no REST api.

The motivation here is to provide a basic CLI to enable/disable a preconfigured IP forwarding configuration.

Install the script:
```bash
./install prod
./run -h # show cli help
```

List router's current "IP-forwarding" configurations:
```bash
./run --pw=<password>

# I've only one:
0: {
    "domain": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANIPConnection.1.PortMapping.1",
    "ProtMapEnabled": "0",
    "RemoteHost": "",
    "RemoteHostRange": "",
    "OperateRule": "",
    "InClient": "192.168.0.145",
    "Description": "My box",
    "ExternalIP": ""
}
```

Enable configuration "0":
```
./run --pw=<password> -f 0:1
```
