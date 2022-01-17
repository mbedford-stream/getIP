# from os import truncate
# ALl the supporting functions are in funcs.py and imported
from funcs import getNetboxIP, getNetboxPrefixes, createIP
# from funcs import readJSON, readHTTP
from datetime import datetime

if __name__ == "__main__":
    # Setup basic netbox connectivity stuff
    netboxURL = "https://172.17.0.16:8443"
    netboxAuth = "b277ccbe97626cb9a5055bcc2fa9cacef95c3a1e"

    allPrefixes, prefixErr = getNetboxPrefixes(netboxURL, netboxAuth)

    if prefixErr != "":
        print("Error connecting to Netbox...")
        quit()

    selectionMade = False
    menuItem = {}
    while selectionMade != True:
        i = 1
        for p in allPrefixes['results']:
            prefixItem = {}
            print("%-5s : %s" % (i, p['prefix']))
            prefixItem['id'] = p['id']
            prefixItem['prefix'] = p['prefix']
            menuItem[i] = prefixItem
            i += 1

        # print(len(allPrefixes['results']))

        try:
            prefixSelect = int(input("Which network? "))
        except Exception as e:
            continue

        if prefixSelect > 1 and prefixSelect <= len(allPrefixes['results']):
            selectionMade = True

    print("getting new IP in network: %s" % menuItem[prefixSelect]['prefix'])

    newIP, freeIPs, getIPErr = getNetboxIP(
        netboxURL, menuItem[prefixSelect]['id'], netboxAuth)

    if getIPErr != "":
        print("Error getting new IP from Netbox...")
        quit()

    newIPDNS = input("DNS name of new IP: ")

    createIPData = {}
    createIPData['ip'] = newIP
    createIPData['name'] = newIPDNS
    createTime = datetime.now()
    formattedTime = createTime.strftime("%d/%m/%Y %H:%M:%S")
    createIPData['desc'] = "Assigned via script %s: %s" % (
        formattedTime, newIPDNS)

    createStatus, retStr = createIP(createIPData, netboxURL, netboxAuth)
    if createStatus != True:
        print("Oopsie")
    else:
        print("\nThe following IP has been assigned and registered...\n%-18s : %s\n" %
              (newIP, newIPDNS))
        if freeIPs == 999:
            print("There are over %s available IPs remaining on this network" %
                  str(freeIPs))
        else:
            print("There are %s available IPs remaining on this network" %
                  str(freeIPs))
