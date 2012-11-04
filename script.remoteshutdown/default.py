# Remote Shutdown

import xbmc
import xbmcaddon

import os
import subprocess

__settings__   = xbmcaddon.Addon(id='script.remoteshutdown')
__cwd__        = __settings__.getAddonInfo('path')
__icon__       = os.path.join(__cwd__,"icon.png")
__scriptname__ = "XBMC Remote Shutdown"

# Get Settings
settings = xbmcaddon.Addon(id = 'script.remoteshutdown')

lang = settings.getLocalizedString

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

def main():
    """ Do the actual execution. """
    if debug:
        msg = "RemoteShutdown: '%s -o \"ConnectTimeout %d\" -y %s@%s \"%s\"'" % (
                sshpath, timeout, remoteuser, hostname, command)
        xbmc.log(msg = msg, level = xbmc.LOGDEBUG)

    notification = 'XBMC.Notification("Sending command to %s", "%s", 5000)' % (
        hostname, sshpath)
    xbmc.executebuiltin(notification)
    retval = subprocess.call(['%s' % sshpath, '-o',
                '"ConnectTimeout %d"' % timeout, '-y',
                '%s@%s' % (remoteuser, hostname),
                '"%s"' % command])

if __name__ == '__main__':
    main()
