import re
from ip_collector import *
from loggy_collector import *

help = """
COMMANDS EXAMPLE
log showall                 show all loggy in loggy database
log search date <date>      search loggy by date (ex:16/May/2000)
log search ip <ip>          search loggy by ip (ex:0.0.0.0)
ip showall                  show all ip in ip database
ip show <ip>                show specific ip in database    
"""

while True:
    cmd = re.split(' ', input('cmd : '))
    if cmd[0] == 'ip':
        try:
            if cmd[1] == "showall": ip_show_info_all()
            elif cmd[1] == "show": ip_show_info(cmd[2])
        except: pass
    elif cmd[0] == 'log':
        try:
            if cmd[1] == "showall": loggy_show_info_all()
            elif cmd[1] == "search":
                try:
                    if cmd[2] == "date": loggy_search_date(cmd[3])
                    elif cmd[2] == "ip": loggy_search_ip(cmd[3])
                    elif cmd[2] == "timedu": loggy_search_timedu(cmd[3], cmd[4])
                except: pass
        except: pass
    elif cmd[0] == "exit": break
    elif cmd[0] == "help": 
        print(help)