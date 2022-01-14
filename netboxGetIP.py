# from os import truncate
# ALl the supporting functions are in funcs.py and imported
from xmlrpc.client import _datetime
from funcs import getNetboxIP, getNetboxPrefixes, createIP, readJSON, readHTTP
from datetime import datetime

if __name__ == "__main__":
    # Setup basic netbox connectivity stuff
    netboxURL = "https://172.17.0.16:8443"
    netboxAuth = "b277ccbe97626cb9a5055bcc2fa9cacef95c3a1e"

    allPrefixes = getNetboxPrefixes(netboxURL, netboxAuth)

    i = 1
    selectionMade = False
    menuItem = {}
    while selectionMade != True:
        for p in allPrefixes['results']:
            prefixItem = {}
            print("%-5s : %s" % (i, p['prefix']))
            prefixItem['id'] = p['id']
            prefixItem['prefix'] = p['prefix']
            menuItem[i] = prefixItem
            i += 1

        try:
            prefixSelect = int(input("Which network? "))
        except Exception as e:
            quit()

        if prefixSelect > 1 and prefixSelect <= len(p):
            selectionMade = True

    print("getting new IP in network: %s" % menuItem[prefixSelect]['prefix'])

    newIP, freeIPs = getNetboxIP(
        netboxURL, menuItem[prefixSelect]['id'], netboxAuth)

    newIPDNS = input("DNS name of new IP: ")

    createIPData = {}
    createIPData['ip'] = newIP
    createIPData['name'] = newIPDNS
    createTime = datetime.now()
    formattedTime = createTime.strftime("%d/%m/%Y %H:%M:%S")
    createIPData['desc'] = "Assigned via script %s: %s" % (
        formattedTime, newIPDNS)

    # print(createIPData)

    # quit()

    createStatus, retStr = createIP(createIPData, netboxURL, netboxAuth)
    if createStatus != True:
        print("Oopsie")
    else:
        print("I think we reserved an IP.... ")
