import json
import requests
import urllib3
import random
import ipaddress

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getNetboxIP(netboxURL, prefixID, netboxAuth):
    # Request a list of available IPs on the VIP network from Netbox and return some stuff
    authHeaders = {
        "content-type": "application/json",
        'Connection': "close",
        "User-Agent": "Mark's API thing (python Requests)",
        "Authorization": "TOKEN " + netboxAuth
    }

    # Netbox has about 4 IPs on this network so I'm not worried about stressing anything
    # but thhis call could be adjusted to be a bit easier on Netbox
    netQueryURL = netboxURL + "/api/ipam/prefixes/%s/available-ips/?limit=1000" % prefixID

    # Send the request
    try:
        authResp = requests.get(
            netQueryURL, headers=authHeaders, verify=False)
    except Exception as e:
        return "", 0,  e

    # Handle cases where response is not 200 so we don't try to json an error message
    if authResp.status_code != 200:
        print(authResp.status_code, authResp.text)
        return "", 0, str(authResp.status_code)+"\n"+authResp.text
    else:
        jsonResp = json.loads(authResp.text)

    # Return the a random IP address from the list of available values
    # just because we can.
    # We also return the total number of available IPs on the subnet.... because we can
    return jsonResp[random.randrange(0, len(jsonResp))]["address"], len(jsonResp)-1


def getNetboxPrefixes(netboxURL, netboxAuth):
    authHeaders = {
        "content-type": "application/json",
        'Connection': "close",
        "User-Agent": "Mark's API thing (python Requests)",
        "Authorization": "TOKEN " + netboxAuth
    }
    # Netbox has about 4 IPs on this network so I'm not worried about stressing anything
    # but thhis call could be adjusted to be a bit easier on Netbox
    netQueryURL = netboxURL + "/api/ipam/prefixes/"

    # Send the request
    try:
        authResp = requests.get(
            netQueryURL, headers=authHeaders, verify=False)
    except Exception as e:
        return "", 0,  e

    # Handle cases where response is not 200 so we don't try to json an error message
    if authResp.status_code != 200:
        print(authResp.status_code, authResp.text)
        return "", 0, str(authResp.status_code)+"\n"+authResp.text
    else:
        jsonResp = json.loads(authResp.text)

    # Return the a random IP address from the list of available values
    # just because we can.
    # We also return the total number of available IPs on the subnet.... because we can

    return jsonResp

    # return jsonResp[random.randrange(0, len(jsonResp))]["address"], len(jsonResp)-1,  ""


def createIP(newEntry, netboxURL, netboxAuth):
    # Create new IP object on Netbox with bare minimum information stuff
    authHeaders = {
        "content-type": "application/json",
        'Connection': "close",
        "User-Agent": "Mark's API thing (python Requests)",
        "Authorization": "TOKEN " + netboxAuth
    }

    netQueryURL = netboxURL + "/api/ipam/ip-addresses/"
    # Here we define the bare minimum informational stuff to attach to the IP
    # Easily updatable since we're passing a dict and just applying those values to the correct field
    createBody = json.dumps({
        "address": newEntry["ip"],
        "description": newEntry["desc"],
        "dns_name": newEntry["name"]
    })

    # Send the request
    try:
        httpResp = requests.post(
            netQueryURL, headers=authHeaders, data=createBody, verify=False)
    except Exception as e:
        return False, e

    # Handle cases where response is not 200 so we don't try to json an error message
    # If everyone is happy, just return True and assume all went well.
    if httpResp.status_code != 201:
        print(httpResp.status_code, httpResp.text)
        return False, str(httpResp.status_code)+"\n"+httpResp.text
    else:
        return True, ""


def readJSON(jsonFile):
    # Probably doesn't even need to be a function but we read the JSON file and return the contents
    returnDict = {}

    try:
        f = open(jsonFile)
    except Exception as e:
        return returnDict, e

    jsonContent = json.loads(f.read())

    f.close()

    return jsonContent, ""


def validIP(ipAddress):
    # Is the IP passed a valid IPv4 address?
    # Not that anyone would try to enter a weird string of numbers and pass it off as an IP
    try:
        ipaddress.ip_address(ipAddress)
        return True
    except ValueError:
        return False


def readHTTP(checkURL):
    # SUPER simple test to see if the service is now responding to requests
    # Load the URL we just created and if it returns a 200 status code we're all good
    authHeaders = {
        'Connection': "close",
        "User-Agent": "Mark's API thing (python Requests)",
    }

    # Send the request
    try:
        httpResp = requests.get(
            checkURL, headers=authHeaders, verify=False)
    except Exception as e:
        return "", e

    if httpResp.status_code != 200:
        return "", str(httpResp.status_code)+"\n"+httpResp.text
    else:
        return httpResp.text, ""


if __name__ == "__main__":
    print("funcs.py cannot be run directly")
    quit()
