# Remote Shutdown

import xbmc
import xbmcaddon

import os
import shlex
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

# ssh extra commandline options (e.g. '-y')
sshextraopts = shlex.split(settings.getSetting('sshextraopts'))

# enable log output (false)
debug = settings.getSetting('debug')

def main():
    """ Do the actual execution. """
    notification = 'XBMC.Notification("Sending command to %s@%s", "%s %s %s", 5000)' % (
        remoteuser, hostname, sshpath, '-o "ConnectTimeout %d" %s' % (
            timeout, ' '.join(sshextraopts)), command)
    xbmc.executebuiltin(notification)
    cmdline = ['%s' % sshpath, '-o', 'ConnectTimeout %d' % timeout]
    cmdline.extend(sshextraopts)
    cmdline.extend(['%s@%s' % (remoteuser, hostname), '%s' % command])

    if debug:
        msg = "RemoteShutdown: '%s'" % ' '.join(cmdline)
        xbmc.log(msg = msg, level = xbmc.LOGDEBUG)

    subprocess.call(cmdline)

if __name__ == '__main__':
    main()
