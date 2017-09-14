import csv
import os
import shutil
import boto3
import logging

Hosts = {'app1':"dc1qsiapi01t01", 'app2':'dc1zxabojv01t01', 'app3':'dc1yhbfiyd01t01'}

server_filename = "servers.csv"
app_server_file_name="app_server.csv"
serverMap = {}
app_server_list=[]

def load_serverMap():

    with open(server_filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            key = str(row[4]).lower().strip()
            serverMap[key]= str(row[0]).lower().strip()
            #serverMap['HostName']=row[1]

            #servers.append(serverMap)

def get_server_id(hostName):
    print ("finding the server Id for the host name %s " %hostName)
    for key, value in serverMap.items():
        #print(key, "-->", value)
        if(hostName in value):
            return key
    return ""


def get_app_id_from_ads(key):
    retval=''
    configurations = client.list_configurations(configurationType='APPLICATION')
    print(configurations)
    appMap = {app['application.name']: app['application.configurationId'] for app in configurations['configurations'] }
    theCount = len(appMap.keys())
    print ("there are %d applications" % theCount)
    if appMap.has_key(key):
        retval = appMap[key]
    else:
        response = client.create_application(name=key,description='')
        print ("Reseponse is %s"%response)
        retval = response['configurationId']
    return retval

#
# def get_ap_id(appName):
#
#     appId = get_app_id_from_ads(appName)
#     return appId


# def load_app_server_map():
#     with open(app_server_file_name) as f:
#         reader = csv.reader(f)
#         header_row = next(reader)
#         for row in reader:
#             app_server_map[row[0]] = row[1]


def load_app_server():
    app_server_lines = open(app_server_file_name,'r').readlines()
    return app_server_lines


def get_hosts(app):
    retVal = []
    return retVal


def get_server_ids(hosts):
    #print hosts
    server_ids=[]
    for h in hosts:

        if serverMap.has_key(h):
            id = serverMap[h]
            server_ids.append(id)
            print ("\tKey %s has been added"%id)
        else:
            print ("\tKey %s Not Found"%h)



    return server_ids


def get_app_server_map(app_server_list):
    retVal = {}
    for line in app_server_list:
        print ("--->%s"%line)
        splitted = line.split(',')
        key = str(splitted[0]).strip()

        value = str(splitted[1]).lower()
        if(retVal.has_key(key)):
            retVal[key] += ',' + value.strip() + ".pdsi.corp"
        else:
            retVal[key] = str(splitted[1]).strip().lower() + ".pdsi.corp"
    return retVal




if __name__ == '__main__':
    log_file="association.log"
    if log_file:
        print(str.format("Debug log file {} configured; this will be the last message to the console.", log_file))
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s: %(message)s')
    client = boto3.client('discovery')

    load_serverMap()
    app_server_list = load_app_server()
    app_server_map = get_app_server_map(app_server_list)

    print (app_server_map)

    for key in app_server_map:
        print ("* work started for app %s"%key)
        hostsString = app_server_map[key]


        # first we need to get all the host names associated with the app in the manaul inventory
        hosts = str(hostsString).split(',')


        serverIds = get_server_ids(hosts)
        msg = "* the list of servers to be associaetd with App %s -->%s"%(key,serverIds)
        print (msg)
        logging.info(msg)

        appId = get_app_id_from_ads(key)

        msg = "**Now associating  App Id: %s with Servers  %s " % (appId, serverIds)
        print (msg)
        logging.info(msg)
        try:
            client.associate_configuration_items_to_application(applicationConfigurationId=appId,configurationIds=serverIds)
            msg = "The app %s has been associated with Servers %s" % (appId, serverIds)
            print (msg)
            logging.info(msg)
        except Exception as ve:
            error = str.format("Error happened!", ve)
            print(error)
            logging.error(error)






