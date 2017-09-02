import os
import sys
import argparse
import shutil
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import time
import csv
import datetime
import boto3


# described_export_task = client.describe_export_tasks(nextToken=u'05e37a6aeba0fba68')
# exported_agents = [export for export in described_export_task['exportsInfo'] if export['exportStatus'] != 'SUCCEEDED']
# print(len(exported_agents))
# print (exported_agents)
# selectedAgents = [a['agentId'] for a in agents_queue[500:500]]




def getNexPage():
    export_response = client.describe_export_tasks()
    exports_info = None

    while exports_info == None:
        for response in export_response['exportsInfo']:
            # if response['exportId'] == exporting_agents[agent_id][2]:
            exports_info = response
            if response['exportStatus'] == 'IN_PROGRESS':
                print ("\n%s" % response)
                # if exports_info == None:
        if export_response['nextToken'] != "":
            print ("there's more with token %s" % export_response['nextToken'])
            export_response = client.describe_export_tasks(nextToken=export_response['nextToken'])
            exports_info = None
            # print export_response
        else:
            exports_info = "Finished"
            print exports_info

            #


            # Search for matching response in while loop for paginated export responses
            # getNexPage()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--reg-time",
                        help="The agent registered timestamp as for a new agent. Format: YYYY-MM-DDTHH:MM",
                        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M'))

    return parser.parse_args()


def CreateFilterForNewAgentsByRegisterationTime(date):
    """ Get teh list of agents that have been registered at a specific date/time """
    new_agents = [(agent['agentId'], agent['registeredTime']) for agent in agents_queue if
                  agent['registeredTime'] >= date]

    filter = "--filter "
    for a in new_agents:
        filter += a[0] + " "

    print filter
    print ("Total Number Agents: %s" % len(agents_queue))
    print ("Number of New Agents: %s" % len(new_agents))


if __name__ == '__main__':
    args = parse_args()

    start_input = args.reg_time
    date_string = start_input.strftime('%Y-%m-%dT%H:%M')
    client = boto3.client('discovery')
    global exports_info, export_response
    agents_queue = [agent for agent in client.describe_agents()['agentsInfo'] if
                    "connector" not in agent['agentType'].lower()]
    CreateFilterForNewAgentsByRegisterationTime(date_string)
