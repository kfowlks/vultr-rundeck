#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Vultr Rundeck Resource Dump 

Author: Kevin Fowlks
Date:   08/22/2016

This program reads servers from vultr and converts output to a rundeck compatible resources.xml file format.  

rundeck resource xml format http://rundeck.org/1.5.2/manpages/man5/resource-v13.html

Requires

Under CYGWIN run to install pip
  python -m ensurepip

# This code relies on the following lib: https://github.com/spry-group/python-vultr

pip install vultr

Usage:
    The program can be run as shown below:

        $ python dump-rundeck-resources.py -k [Vultr-API-Key]

        or 

        export VULTR_KEY=APIKEY
        
        $ python dump-rundeck-resources.py

    The xml is generated to stdio 

    python dump-rundeck-resources.py > /var/rundeck/projects/rundeck-production/etc/resources.xml

"""

import sys
import argparse
import json

from json import dumps
from os import environ
from vultr import Vultr, VultrError
from xml.dom.minidom import Document

def main():
  pass

def exportNode(dictofdicts):

    node = xmldoc.createElement("node")

    # Define our required attributes
    node.setAttribute("name", str(dictofdicts['label']))
    node.setAttribute("type", str("Node"))
    node.setAttribute("hostname", str(dictofdicts['main_ip']))
    node.setAttribute("username", "deploy")
    node.setAttribute("description", "vultr instance {0} os: {1}, ".format(str(dictofdicts['label']), str(dictofdicts['os'])) )
    node.setAttribute("tags", "{0},{1},{2},{3},{4}".format(str(dictofdicts['os']), str(dictofdicts['location']), str(dictofdicts['label']), str(dictofdicts['SUBID']), str(dictofdicts['tag'])) )

    # This will exclude the below keys from being added to the xml attributes
    exclude_set = ['name','type','hostname','username', 'description','SUBID','tag','label']
    
    # Add remaining k,v pairs as custom attributes to the xml document.
    for k,v in dictofdicts.items():
      if k not in exclude_set:
        node.setAttribute( k, str(v))

    return node

parser = argparse.ArgumentParser(description='Vultr Rundeck Resource')

parser.add_argument('-k', '--api-key', metavar='N',dest='api_key', help='Vultr API-Key')
parser.add_argument('-v', '--verbose', help='verbosity',dest='enable_trace', action='store_true')

try:    
  args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

API_KEY = environ.get('VULTR_KEY')

#print 'API-KEY: ', args.api_key
if API_KEY is None:
  if args.api_key is None:
      print "A mandatory option api-key is missing\n"
      parser.print_help()
      exit(-1)
  else:
      api_key = args.api_key
else:
  api_key = API_KEY

vultr = Vultr(api_key)

# Write out xml rundeck format http://rundeck.org/1.5.2/manpages/man5/resource-v13.html
xmldoc = Document()

try:
      # curl -H 'API-Key: APIKEY' "https://api.vultr.com/v1/server/list"
      server_list_json = vultr.server_list()

      project = xmldoc.createElement("project")

      xmldoc.appendChild(project)

      for k in server_list_json:
          node = exportNode(server_list_json[k])

          project.appendChild(node)
          node_attribute_values = {}

      sys.stdout.write(xmldoc.toprettyxml(indent="	"))

except VultrError as ex:
        logging.error('VultrError: %s', ex)

if __name__ == '__main__':
  main()