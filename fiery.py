import json

def label(text,colour):
  colours = {}
  colours["red"]    = "#ff0000"
  colours["green"]  = "#067A16"
  colours["yellow"] = "#F19220"
  colours["white"]  = "#000000"
  colours["blue"]   = "#103AD6"
  return "<span style='color:{}'>{}</span>".format(colours[colour],text)


known_ips                       = {}
known_ips["59.100.26.17/32"]    = "Melb"
known_ips["59.100.13.101/32"]   = "Melb"
known_ips["202.161.105.242/32"] = "Sydney"
known_ips["172.20.0.0/24"]      = label("REMOVEOperations","yellow")
known_ips["172.19.0.0/16"]      = label("Operations","yellow")
known_ips["172.21.0.0/16"]      = label("Greenzone","green")
known_ips["172.22.0.0/16"]      = label("Redzone","red")
known_ips["0.0.0.0/0"]          = label("EVERYONE","blue")
known_ips["10.0.0.0/8"]         = "VpnZone"
known_ips["172.0.0.0/8"]        = "AllZones"
known_ips["192.30.252.0/22"]    = "Github"
known_ips["172.21.51.0/24"]     = label("DashboardA","green")
known_ips["172.21.52.0/24"]     = label("DashboardB","green")
known_ips["172.21.13.0/24"]     = label("DashboardC","green")

known_protocols                 = {}
known_protocols["22"]           = "ssh"
known_protocols["122"]          = "ssh"
known_protocols["80"]           = "http"
known_protocols["443"]          = "https"
known_protocols["9200"]         = "elastic"
known_protocols["5672"]         = "rabbitmq"
known_protocols["5044"]         = "filebeats"

known_vpcs                      = {}
known_vpcs["vpc-f8f43d9d"]      = "green"
known_vpcs["vpc-e96cba8c"]      = "red"
known_vpcs["vpc-7eb4851b"]      = "yellow"
known_vpcs["vpc-ece51b88"]      = "yellow"

known_prefix                    = {}
known_prefix["172.19."]         = "yellow"
known_prefix["172.20."]         = "yellow"
known_prefix["172.21."]         = "green"
known_prefix["172.22."]         = "red"
known_prefix["172.32."]         = "white"

costs                 = {}
costs["t1.micro"]     =  0.008
costs["t2.nano"]      =  0.008
costs["t2.micro"]     =  0.016
costs["t2.small"]     =  0.032
costs["t2.medium"]    =  0.064
costs["t2.large"]     =  0.128
costs["t2.xlarge"]    =  0.256
costs["t2.2xlarge"]   =  0.512
costs["m4.large"]     =  0.134
costs["m4.xlarge"]    =  0.269
costs["m4.2xlarge"]   =  0.538
costs["m4.4xlarge"]   =  1.076
costs["m4.10xlarge"]  =  2.69
costs["m4.16xlarge"]  =  4.305
costs["m3.medium"]    =  0.093
costs["m3.large"]     =  0.186
costs["m3.xlarge"]    =  0.372
costs["m3.2xlarge"]   =  0.745
costs["c4.large"]     =  0.13
costs["c4.xlarge"]    =  0.261
costs["c4.2xlarge"]   =  0.522
costs["c4.4xlarge"]   =  1.042
costs["c4.8xlarge"]   =  2.085
costs["c3.large"]     =  0.132
costs["c3.xlarge"]    =  0.265
costs["c3.2xlarge"]   =  0.529
costs["c3.4xlarge"]   =  1.058
costs["c3.8xlarge"]   =  2.117
costs["g2.2xlarge"]   =  0.898
costs["g2.8xlarge"]   =  3.592
costs["x1.16xlarge"]  =  9.671
costs["x1.32xlarge"]  =  19.341
costs["r3.large"]     =  0.2
costs["r3.xlarge"]    =  0.399
costs["r3.2xlarge"]   =  0.798
costs["r3.4xlarge"]   =  1.596
costs["r3.8xlarge"]   =  3.192
costs["r4.large"]     =  0.16
costs["r4.xlarge"]    =  0.319
costs["r4.2xlarge"]   =  0.638
costs["r4.4xlarge"]   =  1.277
costs["r4.8xlarge"]   =  2.554
costs["r4.16xlarge"]  =  5.107
costs["i2.xlarge"]    =  1.018
costs["i2.2xlarge"]   =  2.035
costs["i2.4xlarge"]   =  4.07
costs["i2.8xlarge"]   =  8.14
costs["d2.xlarge"]    =  0.87
costs["d2.2xlarge"]   =  1.74
costs["d2.4xlarge"]   =  3.48
costs["d2.8xlarge"]   =  6.96



with open('security') as data_file:    
    data = json.load(data_file)

groups = {}

for k in data["SecurityGroups"]:
  sgid = k["GroupId"]
  summary = ""
  groups[sgid] = ""
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

    if fromport == -1 and toport == -1 and p["IpProtocol"] == "icmp":
        port = "ping"
    elif fromport == toport:
      try:
        port = known_protocols[str(fromport)]
      except KeyError, e:
        port = fromport
    else:
      port = "{}-{}".format(fromport, toport)

    if port in ["-1:-1","1-32000","-1"]:
      port = "ALL_PORTS"


    protocol = ""
    ip = ""
    if p["IpProtocol"] != "tcp" and p["IpProtocol"] != "icmp" and p["IpProtocol"] != "-1":
      protocol = p["IpProtocol"]+":"

    for l in p["IpRanges"]:
      try:
        ip = known_ips[l["CidrIp"]]
      except KeyError, e:
        try:
          ip = label(l["CidrIp"],known_prefix[l["CidrIp"][0:7]])
        except KeyError, e:
          ip = l["CidrIp"]

      summary += "</td><td>{} can access {} {}</td><td> ".format(ip, protocol, port)
    groups[sgid] = summary
  


with open('instances') as data_file:    
    data = json.load(data_file)

inst = {}

for k in data["Reservations"]:
  for i in k["Instances"]:
    x = i["InstanceId"]
    inst[x] = {}
    inst[x]["id"] = x
    inst[x]["sgids"] = ""
    inst[x]["ip1"] = i["PublicIpAddress"]
    inst[x]["ip2"] = i["PrivateIpAddress"]
    inst[x]["type"] = i["InstanceType"]
    inst[x]["cost"] = costs[i["InstanceType"]] * 24 * 365 / 12

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
      #print "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(instance["zone"],label(instance["id"],instance["zone"]), instance["ip1"], instance["ip2"], instance["name"], instance["sgids"])
      print "{}, {}, {}, {}, {}, {}, {}".format(instance["zone"], instance["id"], instance["ip1"], instance["ip2"], instance["name"], instance["type"], instance["cost"])


