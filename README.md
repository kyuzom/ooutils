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
import ooutils
# LiPo battery data
battery = ooutils.Battery()
print(battery.level_raw())
print(battery.level())
print(battery.percentage(vmax=4.12, timeout=3.0))
```

## License

ooutils is MIT licensed. See the included [LICENSE](LICENSE) file.
