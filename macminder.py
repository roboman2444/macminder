#!/usr/bin/env python3
from traceback import print_exc
from pprint import pprint

import sys
import csv
import argparse

parser = argparse.ArgumentParser(
                    prog='macminder',
                    description='Minds your macs',
                    epilog='Bottom text')
parser.add_argument('-e', '--essid', type=str, help="filter mac to this essid")
parser.add_argument("filename", nargs='+', help="any csv files you want to process")

args = parser.parse_args()
filteressid = None

if args.essid:
	filteressid = args.essid.strip()

Stations = []
APs = []


for fname in args.filename:
	try:
		print(fname)
		with open(fname, newline='') as csvfile:
			#reader = csv.DictReader(csvfile)
			reader = csv.reader(csvfile)
			#there's gotta be a better way to do this... maybe a different output form
			#look for ap section
			#look for station section
			curput = None
			for row in reader:
				if not any(row): continue
		#		pprint(row[0])
				if "BSSID" in row[0]:
					curput = APs
					continue
				if "Station" in row[0]:
					curput = Stations
					continue
				#if curput misses empty lists
				if curput != None:
					curput.append(row)

	except:
		print_exc()

if filteressid:
	print("filtering to " + filteressid)

APsdict ={}
for ap in APs:
	try:
		mac = ap[0].strip()
		firstseen = ap[1].strip()
		lastseen = ap[2].strip()
		essid = ap[13].strip()
#		print(f"{mac} - {essid}")
		if filteressid and essid.strip() != filteressid:
			continue
		APsdict[mac] = (essid, firstseen, lastseen)
	except:
		print_exc()

lookforprobes = set([ v[0] for k,v in APsdict.items() ])

Stationsdict = {}
StaWithAssoc = {}
StaWithProbe = {}
for sta in Stations:
	try:
		mac = sta[0].strip()
		firstseen = sta[1].strip()
		lastseen = sta[2].strip()
		bssid = sta[5].strip()
		probes = sta[6].strip()
		if "(not associated)" in bssid:
			bssid = None
		Stationsdict[mac] = (bssid, firstseen, lastseen, probes)

		assoc = APsdict.get(bssid)
		if assoc:
			StaWithAssoc[mac] = (bssid, assoc[0], firstseen, lastseen, probes)
		if probes and probes in lookforprobes:
			StaWithProbe[mac] = (bssid, firstseen, lastseen, probes)
	except:
		print_exc()
#pprint(Stationsdict)



#todo re-do this once i figure out what multiple probes look like
#StaWithAssoc = { k,v for k,v in Stationsdict.items() if v[0] and v[0] in Apsdict )

print("looking for associations to...")

assocprint = [ (k, v[0]) for k,v in APsdict.items() ]
pprint(assocprint)

print("Assoc to ...")
pprint(StaWithAssoc)

print("looking for probes to...")
pprint(lookforprobes)
print("Probe to ...")
pprint(StaWithProbe)


#print("All")
#pprint(Stationsdict)
