#!/usr/bin/env python
'''
Onion Omega LiPo battery support.
'''
import subprocess
import threading
import re
try:
	from Queue import Queue
except (ImportError, ModuleNotFoundError):
	from queue import Queue

class Battery(object):
	'''
	LiPo battery object
	'''
	BATTERY_CLI_EXE = "power-dock2"
	BATTERY_RGX_PAT = "(\d+\.\d+ V)|(\d+ V)"

	def __init__(self):
		self._ps = None

	def level_raw(self, timeout=1.0):
		'''
		Get battery level in raw format (str)
		@param timeout: [float] Timeout for battery level reading
		@return [str] Battery level in format '%d V'
		'''
		def access_battery_level(msgq):
			self._ps = subprocess.Popen([Battery.BATTERY_CLI_EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = self._ps.communicate()
			msgq.put((self._ps.returncode, out, err), block=True, timeout=0.1)
		msgq = Queue(maxsize=1)
		psthr = threading.Thread(target=access_battery_level, args=(msgq,))
		psthr.start()
		psthr.join(timeout=timeout)
		if self._ps is None:
			raise RuntimeError("OO Battery level, Timed out.")
		elif (self._ps.poll() is None) or psthr.is_alive():
			self._ps.terminate()
			psthr.join()
			self._ps = None
			raise RuntimeError("OO Battery level, Timed out.")
		self._ps = None
		rc, out, err = msgq.get(block=True, timeout=0.1)
		msgq.task_done()
		msgq.join()
		if rc != 0:
			raise RuntimeError("OO Battery level, rc: {0}, error: {1}".format(rc, err))
		match = re.search(Battery.BATTERY_RGX_PAT, out.strip())
		if match is None:
			raise RuntimeError("OO Battery level, Unknown str format: {0}".format(out))
		return match.group()

	def level(self, timeout=1.0):
		'''
		Get battery level in [V] (float)
		@param timeout: [float] Timeout for battery level reading
		@return [float] Battery level in [V]
		'''
		return float(self.level_raw(timeout=timeout)[:-2])

	def percentage(self, vmax=4.2, vmin=3.5, timeout=1.0):
		'''
		Get battery level percentage in [%] (float)
		@param vmax: [float] Battery maximum level in [V]
		@param vmin: [float] Battery minimum level in [V]
		@param timeout: [float] Timeout for battery level reading
		@return [float] Battery level in [%]
		'''
		vactual = self.level(timeout=timeout)
		return float(((vactual-vmin)/(vmax-vmin))*100)

if __name__ == '__main__':
	import sys
	battery = Battery()
	if sys.version_info[0] == 2:
		print battery.level_raw()
	else:
		print(battery.level_raw())
