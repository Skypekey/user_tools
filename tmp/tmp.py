import pathlib
from telnetlib import PRAGMA_HEARTBEAT


s = r'D:\tmp\111\win.1.2'
basepath = pathlib.Path(s)
is_exist = basepath.exists()
is_dir = basepath.is_dir()
is_file = basepath.is_file()
print(is_dir)
# size = basepath.stat().st_size
if [True, False].count(True) == 2:
    print(1111111111)