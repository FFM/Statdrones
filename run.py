import settings
import importlib
import sys

drones=[importlib.import_module(i).Drone for i in settings.drones]
tests=[i.name for i in drones]

if __name__=="__main__":
  try:
    cmd=sys.argv[1]
  except IndexError:
    cmd=""
  if cmd in tests:  
    drones[tests.index(cmd)]().run()
  else: 
    print """Usage run.py <command>"""
    print """known commands: """
    for i in drones:
      print "%s: %s"%(i.name,i.description)

