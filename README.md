# ooutils

OO utils - Collection of Onion Omega python scripts.

## Installation

### libs

Install extra libraries that this package depends on:
``` sh
opkg install python-light power-dock2
```

### setup.py

Install this package manually via **setup.py** file:
``` sh
git clone https://github.com/kyuzom/ooutils
cd ooutils
python setup.py install
```

## Usage

### python lib

Use as an external library:
``` python
from __future__ import print_function
import time
import ooutils

# LiPo battery data
battery = ooutils.Battery()
print(battery.level_raw())
print(battery.level())
print(battery.percentage(vmax=4.12, timeout=0.8))

# LiPo battery asynchronous data
battery = ooutils.ABattery()
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
```

## License

ooutils is MIT licensed. See the included [LICENSE](LICENSE) file.
