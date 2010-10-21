#!/usr/bin/env python
#
#   Corey Goldberg - 2010
#   reboot a list of remote windows machines
#   requires Python 2.x and Python for Windows Extensions (pywin32)



import win32api
import win32security
import ntsecuritycon



HOSTS = (
    'server01.example.com',
    'server02.example.com',
    '192.168.12.70', 
)



def main():
    for host in HOSTS:
        print 'rebooting: %s' % host
        reboot_server(host)
    print '\ndone rebooting all machines'


def reboot_server(host, message='server rebooting', timeout=5, force=1, reboot=1):
    adjust_privilege(ntsecuritycon.SE_SHUTDOWN_NAME)
    try:
        win32api.InitiateSystemShutdown(host, message, timeout, force, reboot)
    finally:
        adjust_privilege(ntsecuritycon.SE_SHUTDOWN_NAME, False)


def adjust_privilege(priv, enable=True):
    flags = ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id = win32security.LookupPrivilegeValue(None, priv)
    if enable:
        new_privileges = [(id, ntsecuritycon.SE_PRIVILEGE_ENABLED)]
    else:
        new_privileges = [(id, 0)]
    win32security.AdjustTokenPrivileges(htoken, 0, new_privileges)
    
    
    
if __name__=='__main__':
    main()
    