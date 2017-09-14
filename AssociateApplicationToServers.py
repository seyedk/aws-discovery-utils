import csv
import os
import shutil


Hosts = ["dc1qsiapi01t01", "dc1zxabojv01t01", "dc1yhbfiyd01t01"]

server_filename = "servers.csv"
serverMap = {}
def load_serverMap():

    with open(server_filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:

            serverMap[row[0]]= row[4]
            #serverMap['HostName']=row[1]

            #servers.append(serverMap)

def get_server_id(hostName):
    print ("finding the server Id for the host name %s " %hostName)
    for key, value in serverMap.items():
        #print(key, "-->", value)
        if(hostName in value):
            return key
    return ""

if __name__ == '__main__':
    load_serverMap()
    for host in Hosts:
        Id = get_server_id(host)
        print "Found Id ", Id



