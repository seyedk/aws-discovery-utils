import os
import sys
import argparse
import shutil
import time
import csv
import datetime
import boto3



filename='application_names.csv'
if __name__ == '__main__':
    apps = []
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        print (header_row)
        for index, column_header in enumerate(header_row):
            print(index, column_header)
        client = boto3.client('discovery')
        for row in reader:

            try:
                print ("Adding %s application to ADS ..." % row[0])
                client.create_application(name=row[0], description=row[1])
                print ("Application %s has been added to ADS successfully!" % row[0])
            except Exception:
                pass





