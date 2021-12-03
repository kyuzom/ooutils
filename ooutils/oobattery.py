#!/usr/bin/env python
'''
Onion Omega LiPo battery support.
'''
import subprocess
import re

BATTERY_CLI_EXE = "power-dock2"
BATTERY_RGX_PAT = "(\d+\.\d+ V)|(\d+ V)"

def battery_level_raw():
	'''
	Return with battery level in raw format (str)
	'''
	ps = subprocess.Popen(BATTERY_CLI_EXE, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = ps.communicate()
	if ps.returncode != 0:
		raise RuntimeError("OO battery_level, error: ", err)
	match = re.search(BATTERY_RGX_PAT, out.strip())
	if match is None:
		raise RuntimeError("OO battery_level, Could not retrieve information.")
	return match.group()

def battery_level():
	'''
	Return with battery level in [V] (float)
	'''
	return float(battery_level_raw()[:-2])

def battery_percentage(vmax=4.2, vmin=3.5):
	'''
	Return with battery level percentage in [%] (float)
	'''
	vactual = battery_level()
	return float(((vactual-vmin)/(vmax-vmin))*100)
