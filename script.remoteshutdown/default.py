# Remote Shutdown

from xbmc import executebuiltin, log, LOGDEBUG
from xbmcaddon import Addon

import subprocess

def main():
    # Init Addon
    settings = Addon(id = 'script.remoteshutdown')
    lang = settings.getLocalizedString

    # Get Settings
# command example 'shutdown -hP now'

    # remote hostname (e.g. 'host.domain.com')
    hostname = settings.getSetting('hostname')
    # path to ssh executable (e.g. '/usr/bin/ssh')
    sshpath = settings.getSetting('sshpath')
    # username on remote machine (e.g. 'root')
    remoteuser = settings.getSetting('remoteuser')
    # command to execute remotely (e.g. 'shutdown -hP now')
    command = settings.getSetting('command')
    # ssh connect timeout (e.g. 20)
    timeout = (int(settings.getSetting('timeout')) * 5) + 5
    # enable log output (false)
    debug = settings.getSetting('debug')

    if debug:
        msg = "RemoteShutdown: '%s -o \"ConnectTimeout %d\" -y -l %s %s \"%s\"'" % (
                  sshpath, timeout, remoteuser, hostname, command)
        log(msg = msg, level=LOGDEBUG)

    executebuiltin('XBMC.Notification("Sending command", "/usr/bin/ssh", 5000)')
    retval = subprocess.call(['%s' % sshpath, '-o', '"ConnectTimeout %d"' % timeout, '-y',
                  '-l', '%s' % remoteuser, '%s' % hostname, '"%s"' % command])

if __name__ == '__main__':
    main()
