""" The pinging drone """
import subprocess
from collectclient import Collector
import requests
import settings
import re,os


trl=re.compile("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) .*?  ([0-9]+)/([0-9]+)/([0-9]+)% .*? ([0-9.]+)/([0-9.]+)/([0-9.]+)")
pingc=["fping","-c","10","-A","-q","-i","200"]

class Drone:
  name="ping"
  description="Pings all ip addresses"
  apiurl="FFM-Net_Interface_in_IP4_Network/?verbose"

  def __init__(self):
    r=requests.get("%s/%s"%(settings.nodedb,self.apiurl),verify=False)
    ips=r.json()
    self.ips=[i["attributes"]["ip_address"]["address"] for i in ips["entries"]]

  def run(self):
    try:
      ping=subprocess.check_output(pingc+self.ips,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
      ping=e.output
    c=Collector(test=self.name,resource="address",id=self.ips[0])
    ipm=re.compile("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})")
    pks=re.compile("([0-9]+)/([0-9]+)/([0-9]+)%")
    rtts=re.compile("([0-9.]+)/([0-9.]+)/([0-9.]+)$")
    for l in ping.split("\n"):
      data={}
      m=ipm.search(l)
      if m:
        ip=m.group(1)
      else:
        ip=None
      m=pks.search(l)
      if m:
        (data["packets_transmitted"],
         data["packets_received"],
         data["package_loss"])=[int(i) for i in m.groups()]
      m=rtts.search(l)  
      if m:
        (data["min_rtt"],
         data["avg_rtt"],
         data["max_rtt"])=[float(i) for i in m.groups()]
      if ip:
        c.id=ip
        c.write(data)


    
