import re
from ip_collector import *
from loggy_collector import *

help = """
COMMANDS EXAMPLE
log showall                            show all loggy in loggy database
log search date <date>                 search loggy by date (ex: 16/May/2000)
log search datedur <dd-dd/mmm/yyyy>  search loggy by date during (ex: 16-17/May/2000)
log search ip <ip>                     search loggy by ip (ex:0.0.0.0)
log addlog <filepath>                  add new log file read and store in database
ip showall                             show all ip in ip database
ip show <ip>                           show specific ip in database    
"""

while True:
    cmd = re.split(' ', input('cmd : '))
    if cmd[0] == 'ip':
        try:
            if cmd[1] == "showall": ip_show_info_all()
            elif cmd[1] == "show": 
                try: ip_show_info(cmd[2]) 
                except: pass
        except: pass
    elif cmd[0] == 'log':
        try:
            if cmd[1] == "showall": loggy_show_info_all()
            elif cmd[1] == "addlog": 
                try: 
                    loggy_database_append(loggy_read_log_file(cmd[2]))
                except: pass
            elif cmd[1] == "search": 
                try:
                    if cmd[2] == "date": 
                        try: loggy_show_loggy(loggy_search_date(cmd[3]))
                        except: pass
                    elif cmd[2] == "datedur": 
                        try: loggy_show_loggy(loggy_search_datedur(cmd[3]))
                        except: pass
                    elif cmd[2] == "ip": 
                        try: loggy_show_loggy(loggy_search_ip(cmd[3]))
                        except: pass
                except: pass
        except: pass
    elif cmd[0] == "exit": break
    elif cmd[0] == "help": 
        print(help)