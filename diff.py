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

""" 

creates a list of agents have not been exported.
usese the directory path with the assumption that 

"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory",
                        help="Path to directory containing agentExports folder. Default set to current directory.",
                        type=str, default=os.getcwd())

    return parser.parse_args()


def get_subdirs(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


# /code/Client/PDS/discovery-export


if __name__ == '__main__':
    print("hello there!")
    args = parse_args()
    # this gets all the agents we have exported so far!
    dir_path = os.path.join(args.directory, "agentExports")
    agent_dirs = get_subdirs(dir_path)
    # we can print them if needed :)
    for dir in agent_dirs:
        print ("%s\n" % dir)

    # now we need to get the total number of agents we have in ADS database:
    # but first we need to instantiate boto "discovery" client

    client = boto3.client('discovery')

    # then we read the agents info from the database: but really? we need just the agent ID
    agents_queue = [agent['agentId'] for agent in client.describe_agents()['agentsInfo'] if
                    "connector" not in agent['agentType'].lower()]

    # let's log it to make sure we have the agentId only:
    print ("All agents in the DB:")
    for a in agents_queue:
        print ("%s\n" % a)

    # now we need to get the diff of the captured agents:
        # with slight change in the above loop
    if(agents_queue.count>0):
        print("Printing the agents not in the agentExport directory")
        filter = "--filter "
        for agent in agents_queue:
            if agent not in agent_dirs:
                print (agent)
                filter += " %s"%agent
        print filter



