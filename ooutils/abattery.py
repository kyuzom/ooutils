#!/usr/bin/env python
'''
Onion Omega LiPo battery asynchronous support.

NOTE! This is not the async python lib, just enables asynchronous battery level access.
'''
from __future__ import print_function
import uuid
import threading
try:
	from .battery import Battery
except ValueError:
	from battery import Battery

class ABattery(object):
	'''
	LiPo battery asynchronous object
	'''
	OP_NOTHING = 0
	OP_ONGOING = 1
	OP_SUCCESS = 2
	OP_FAILURE = 3

	def __init__(self):
		self._results = dict()

	def get(self, id):
		'''
		Get result identified by parameter id
		@param id: [str] Operation unique identifier
		@return [tuple] Result of the requested operation (operation code, result value)
		'''
		if id in self._results:
			return (self._results[id]['opcode'], self._results[id]['result'])
		else:
			return (ABattery.OP_NOTHING, None)

	def wait(self, id, timeout=1.0):
		'''
		Wait for operation to finish identified by parameter id
		@param id: [str] Operation unique identifier
        @param timeout: [float] Timeout for waiting
		@return [tuple] Result of the requested operation (operation code, result value)
		'''
		if id in self._results:
			self._results[id]['worker'].join(timeout=timeout)
			return (self._results[id]['opcode'], self._results[id]['result'])
		else:
			return (ABattery.OP_NOTHING, None)

	def terminate(self, id):
		'''
		Terminate operation identified by parameter id
		@param id: [str] Operation unique identifier
		@return [tuple] Result of the requested operation (operation code, result value)
		'''
		if id in self._results:
			battery = self._results[id]['object']
			opcode = self._results[id]['opcode']
			result = self._results[id]['result']
			if battery._ps is not None:
				battery._ps.terminate()
			self._results[id]['worker'].join()
			del self._results[id]
			return (opcode, result)
		else:
			return (ABattery.OP_NOTHING, None)

	def _battery_async(self, id, *args):
		'''
		Measure battery level in the background
		@param id: [str] Operation unique identifier
		'''
		battery = self._results[id]['object']
		try:
			value = getattr(battery, self._results[id]['method'])(*args)
		except Exception as e:
			self._results[id]['result'] = str(e)
			self._results[id]['opcode'] = ABattery.OP_FAILURE
		else:
			self._results[id]['result'] = value
			self._results[id]['opcode'] = ABattery.OP_SUCCESS

	def level_raw(self, timeout=1.0):
		'''
		Get battery level in raw format in the background (str)
		@param timeout: [float] Timeout for battery level reading
		@return [str] Operation identifier
		'''
		id = str(uuid.uuid4())
		thr = threading.Thread(target=self._battery_async, args=(id, timeout))
		self._results[id] = {
			'opcode': ABattery.OP_ONGOING,
			'object': Battery(),
			'method': 'level_raw',
			'worker': thr,
			'result': None
		}
		thr.start()
		return id

	def level(self, timeout=1.0):
		'''
		Get battery level in [V] in the background (float)
		@param timeout: [float] Timeout for battery level reading
		@return [str] Operation identifier
		'''
		id = str(uuid.uuid4())
		thr = threading.Thread(target=self._battery_async, args=(id, timeout))
		self._results[id] = {
			'opcode': ABattery.OP_ONGOING,
			'object': Battery(),
			'method': 'level',
			'worker': thr,
			'result': None
		}
		thr.start()
		return id

	def percentage(self, vmax=4.2, vmin=3.5, timeout=1.0):
		'''
		Get battery level percentage in [%] in the background (float)
		@param vmax: [float] Battery maximum level in [V]
		@param vmin: [float] Battery minimum level in [V]
		@param timeout: [float] Timeout for battery level reading
		@return [str] Operation identifier
		'''
		id = str(uuid.uuid4())
		thr = threading.Thread(target=self._battery_async, args=(id, vmax, vmin, timeout))
		self._results[id] = {
			'opcode': ABattery.OP_ONGOING,
			'object': Battery(),
			'method': 'percentage',
			'worker': thr,
			'result': None
		}
		thr.start()
		return id

if __name__ == '__main__':
	#from __future__ import print_function
	import time
	battery = ABattery()
	id0 = battery.level_raw()
	id1 = battery.level()
	id2 = battery.percentage(vmax=4.12, timeout=0.8)
	print(battery.wait(id0, timeout=0.1))
	print(battery.wait(id2))
	time.sleep(3)
	print(battery.get(id0))
	print(battery.get(id1))
	print(battery.terminate(id2))
	print(battery.get(id2))
