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

# Shortcut to getLocalizedString
lang = settings.getLocalizedString

# Notification Icons
iconsdir = os.path.join(__cwd__, 'resources', 'icons')
icon_ssh = os.path.join(iconsdir, 'ssh.png')
icon_success = os.path.join(iconsdir, 'ssh_success.png')
icon_error = os.path.join(iconsdir, 'ssh_error.png')

# Methods
def notify(header = '', msg = '', timeout = 5000, icon = None):
    """ Send XBMC Notifcation """

    # Build notification string
    notification = 'XBMC.Notification("'
    notification += header
    notification += '", "'
    notification += msg
    notification += '", '
    notification += '%d' % timeout
    if icon is not None:
        notification += ', "'
	notification += icon
	notification += '"'
    notification += ')'

    # Notify
    xbmc.executebuiltin(notification)


def main():
    """ Do the actual execution. """

    # Send initial notification
    header = lang(41000).replace('%remoteuser%', remoteuser).replace('%hostname%', hostname)
    msg = '%s %s %s' % (
        sshpath, '-o "ConnectTimeout %d" %s' % (
            timeout, ' '.join(sshextraopts)
        ), command)
    notify(header = header, msg = msg, icon = icon_ssh)

    # Build commandline
    cmdline = ['%s' % sshpath, '-o', 'ConnectTimeout %d' % timeout]
    cmdline.extend(sshextraopts)
    cmdline.extend(['%s@%s' % (remoteuser, hostname), '%s' % command])

    if debug:
        logmsg = "RemoteShutdown: '%s'" % ' '.join(cmdline)
        xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

    retval = subprocess.call(cmdline)

    # Success
    if retval == 0:
        if debug:
            logmsg = 'RemoteShutdown: Success!'
            xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

        header = lang(41001)
        notify(header = header, msg = msg, icon = icon_success)
        return

    # Error
    if debug:
        logmsg = 'RemoteShutdown: Error!'
        xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

    header = lang(41002)
    notify(header = header, msg = msg, icon = icon_error)


if __name__ == '__main__':
    main()
