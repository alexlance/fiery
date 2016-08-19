#!/usr/bin/env python

import json

# apt install python-termcolor
#from termcolor import colored

def colored(text,colour):
  colours = {}
  colours["red"]    = "#ff0000"
  colours["green"]  = "#067A16"
  colours["yellow"] = "#F19220"
  colours["white"]  = "#000000"
  colours["blue"]   = "#103AD6"
  return "<span style='color:{}'>{}</span>".format(colours[colour],text)


known_ips = {}
known_ips["59.100.26.17/32"]    = "Melb"
known_ips["59.100.13.101/32"]   = "Melb"
known_ips["202.161.105.242/32"] = "Sydney"
known_ips["172.20.0.0/24"]      = colored("Operations","yellow")
known_ips["172.21.0.0/16"]      = colored("Greenzone","green")
known_ips["172.22.0.0/16"]      = colored("Redzone","red")
known_ips["0.0.0.0/0"]          = colored("EVERYONE","blue")
known_ips["10.0.0.0/8"]         = "Vpn"
known_ips["172.0.0.0/8"]        = "Allzones"

known_protocols = {}
known_protocols["22"]           = "ssh"
known_protocols["122"]          = "ssh"
known_protocols["80"]           = "http"
known_protocols["443"]          = "https"
known_protocols["9200"]         = "elastic"

known_vpcs = {}
known_vpcs["vpc-f8f43d9d"] = "green"
known_vpcs["vpc-e96cba8c"] = "red"
known_vpcs["vpc-7eb4851b"] = "yellow"

known_prefix = {}
known_prefix["172.20."] = "yellow"
known_prefix["172.21."] = "green"
known_prefix["172.22."] = "red"
known_prefix["172.32."] = "white"


with open('security') as data_file:    
    data = json.load(data_file)

groups = {}

for k in data["SecurityGroups"]:
  sgid = k["GroupId"]
  summary = ""
  for p in k["IpPermissions"]:

    try:
      fromport = p["FromPort"]
      toport = p["ToPort"]
    except KeyError,e:
      try:
        fromport = p["IpProtocol"]
        toport = p["IpProtocol"]
      except e:
        print "skipping entry: {} {}".format(e, p)
        continue

    if fromport == -1 and toport == -1 and p["IpProtocol"] == "icmp":
        port = "ping"
    elif fromport == toport:
      try:
        port = known_protocols[str(fromport)]
      except KeyError, e:
        port = fromport
    else:
      port = "{}-{}".format(fromport, toport)

    protocol = ""
    ip = ""
    if p["IpProtocol"] != "tcp" and p["IpProtocol"] != "icmp":
      protocol = p["IpProtocol"]+":"

    for l in p["IpRanges"]:
      try:
        ip = known_ips[l["CidrIp"]]
      except KeyError, e:
        try:
          ip = colored(l["CidrIp"],known_prefix[l["CidrIp"][0:7]])
        except KeyError, e:
          ip = l["CidrIp"]

      summary += "</td><td>{}{} {}</td><td> ".format(protocol, port, ip)
          
    groups[sgid] = summary
  
  if sgid not in groups:
    groups[sgid] = ""


with open('instances') as data_file:    
    data = json.load(data_file)

inst = {}

for k in data["Reservations"]:
  for i in k["Instances"]:
    x = i["InstanceId"]
    inst[x] = {}
    inst[x]["id"] = x
    inst[x]["sgids"] = ""

    try:
      inst[x]["zone"] = known_vpcs[i["VpcId"]]
    except KeyError, e:
      inst[x]["zone"] = "white"

    try:
      for n in i["Tags"]:
        if n["Key"] == "Name":
          inst[x]["name"] = n["Value"]
    except KeyError, e:
      inst[x]["name"] = ""

    for s in i["SecurityGroups"]:
      sgid = s["GroupId"]
      try:
        inst[x]["sgids"] += "{}".format(groups[sgid])
      except KeyError, e:
        print "wtf {}".format(e)
    

for colour in ["red","green","yellow","white"]:
  for k,instance in inst.items():
    if instance["zone"] == colour:
      print "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(colored(instance["id"],instance["zone"]), instance["name"], instance["sgids"])


