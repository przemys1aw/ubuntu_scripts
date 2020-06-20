#!/usr/bin/python3

# genSecDbPerRel.py || GENerate SECurity DataBase PER RELease
#
# A script to create the Ubuntu security database json only
# for one target release to improve queries for USNs, CVEs
# and deb packages.
# For more info check: https://usn.ubuntu.com
#
# Author: przemys1aw
# Project page: https://github.com/przemys1aw/ubuntu_scripts
# License MIT
# Date: 06/20/2020
#
# Sample usage:
# ./genSecDbPerRel.py focal

import json, os, urllib.request, sys

releases = ["artful", "bionic", "cosmic", "disco", "eoan", "focal",
            "hardy", "lucid", "natty", "oneiric", "precise", "quantal",
            "raring", "saucy", "trusty", "utopic", "vivid", "wily",
            "xenial", "yakkety", "zesty"
]

# Testing the input value
if len(sys.argv) != 2:
  print(
    "Provide the valid Ubuntu target release code name." +
    "Example:\n\n\t {} focal\n".format(sys.argv[0])
  )
  sys.exit()
else:
  target = sys.argv[1]

for t in releases:
  if t == target:
    found = True
    break

try:
  if found:
    print("The target Ubuntu release to create the security database is: {}.".format(target))
except:
  print("The target Ubuntu release {} not recognized.".format(target))
  print("The valid code names are:\n")
  for t in releases:
    print(t, end=' ')
  print()
  sys.exit()

# functions
def getSecDb():
  url = 'https://usn.ubuntu.com/usn-db/database.json'
  secDbFile =  "./database.json"

  if os.path.exists(secDbFile):
    print("The local full monty database file {} is available.".format(secDbFile))
  else:
    print("The local full monty database file {} not found. Downloading it.".format(secDbFile))
    urllib.request.urlretrieve(url, secDbFile)
    print("Download completed.")

  with open('./database.json', 'r') as secDbFile:
    dbObj = json.load(secDbFile)
    secDbFile.close()
  return dbObj

def freshDbFile(ubuntuRelease):
  dbFile =  "./" + ubuntuRelease + "Database.json"
  if os.path.exists(dbFile):
    os.remove(dbFile)
    print(
      "The previous instance of the {} database was removed." +
      "\nCreating a fresh version of {} file.".format(ubuntuRelease, dbFile)
    )
  else:
    print("Creating a new {} file.".format(dbFile))
  return dbFile

def genRelSecDb(ubuntuRelease, inputDatabaseObj):
  releaseDb = {}
  for row in inputDatabaseObj:
    for release in inputDatabaseObj[row]["releases"].keys():
      if release == ubuntuRelease:
        releaseInfo = { ubuntuRelease: inputDatabaseObj[row]["releases"][ubuntuRelease] }
        fullDatabaseObj[row]["releases"] = releaseInfo
        releaseDb[row] = inputDatabaseObj[row]
  return json.dumps(releaseDb)

# main
print("Attempting to create the security database for the {} release.".format(target))

fullDatabaseObj = getSecDb()

f  = open(freshDbFile(target) , 'w+')
f.write(genRelSecDb(target, fullDatabaseObj))
print("The file was created.")
f.close()
