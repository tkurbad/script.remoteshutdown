#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Remote Shutdown XBMC Addon

import os
import os.path
import shlex
import subprocess

import xbmc
import xbmcaddon

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

# ssh connect timeout (seconds) (e.g. 30)
timeout = int(float(settings.getSetting('timeout')))

# use shell
shell = (settings.getSetting('shell') == 'true')

# ssh extra commandline options (e.g. '-i /path/to/key')
sshextraopts = shlex.split(settings.getSetting('sshextraopts'))
#  try to filter some 'dangerous' options
if 'ssh' in sshpath:
    oldextraopts = sshextraopts[:]
    for extraopt in ['-q', '-y']:
        if extraopt in sshextraopts:
            sshextraopts.remove(extraopt)
    if oldextraopts != sshextraopts:
        settings.setSetting('sshextraopts', ' '.join(sshextraopts))

# enable log output (false)
debug = (settings.getSetting('debug') == 'true')

# Shortcut to getLocalizedString
lang = settings.getLocalizedString

# Notification Icons
iconsdir = os.path.join(__cwd__, 'resources', 'icons')
icon_ssh = os.path.join(iconsdir, 'ssh.png')
icon_success = os.path.join(iconsdir, 'ssh_success.png')
icon_error = os.path.join(iconsdir, 'ssh_error.png')

# Standard Notifications
notify_ssh = lang(41000)
notify_success = lang(41001)
notify_error = lang(41002)


# Methods
def notify(header = '', msg = '', timeout = 5000, icon = None):
    """ Send XBMC Notifcation """

    # Build notification string
    notification = u'XBMC.Notification("'
    notification += u'%s' % header
    notification += u'", "'
    notification += u'%s' % msg
    notification += u'", '
    notification += u'%d' % timeout
    if icon is not None:
        notification += u', "'
	notification += u'%s' % icon
	notification += u'"'
    notification += u')'

    # Notify
    xbmc.executebuiltin(notification.encode('utf-8'))


def _error(msg = '', exitcode = None):
    """ Notify about an error """
    if debug:
        logmsg = 'RemoteShutdown: Error!'
        if exitcode is not None:
            logmsg = '%s Exit code %d' % (logmsg, exitcode)
        xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

    header = notify_error
    notify(header = header, msg = msg, icon = icon_error)


def main():
    """ Do the actual execution. """

    # Build commandline
    cmdline = []

    cmdline_cmd = [r'%s' % sshpath]
    cmdline_args = []
    if 'ssh' in sshpath:
        cmdline_args.extend([r'-t', r'-y'])
        cmdline_args.extend([r'-o', r'ConnectTimeout %d' % timeout])
    cmdline_args.extend(sshextraopts)
    cmdline_rhost = [r'%s@%s' % (remoteuser, hostname)]
    cmdline_rcmd = [r'%s' % command]

    for part in (cmdline_cmd, cmdline_args, cmdline_rhost, cmdline_rcmd):
        cmdline.extend(part)

    # Execution via shell enabled?
    if shell:
        cmdline = ' '.join(cmdline)

    # Send initial notification
    header = notify_ssh
    msg = '%s %s %s\n%s' % (
        ' '.join(cmdline_cmd),
        ' '.join(cmdline_args),
        ' '.join(cmdline_rhost),
        ' '.join(cmdline_rcmd))
    notify(header = header, msg = msg, icon = icon_ssh)

    # Write cmdline to the log, if debugging is enabled
    if debug:
        logmsg = "RemoteShutdown: '%s'" % ' '.join(cmdline)
        xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

    # Execute the cmdline
    try:
        process = subprocess.Popen(
            cmdline,
            shell = shell,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    except OSError, e:
        # E.g., command not found
        _error(e.strerror)
        return

    # XBMC messes with the returncode of child processes by setting
    # the signal handler for SIGCHLD to SIG_IGN.
    # Thus, whenever a returncode should be retrieved, the child
    # process is already dead.
    # To circumvent this, we have to trust the command to fill stderr
    # with some text, if an error occurs.
    stdout_value, stderr_value = process.communicate()

    # Split the strings up for easier handling
    stdout_list = stdout_value.split('\n')
    stderr_list = stderr_value.split('\n')

    # Success, i.e. stderr_value is empty
    if not stderr_value:
        if debug:
            logmsg = 'RemoteShutdown: Success!'
            xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

        header = notify_success
        notify(header = header, msg = msg, icon = icon_success)
        # TODO: Show command output, i.e. stdout_value, in a popup window
        return

    # Error, otherwise
    if debug:
        logmsg = 'RemoteShutdown: Error!\n'
        logmsg += 'RemoteShutdown: STDERR: %s' % stderr_value
        xbmc.log(msg = logmsg, level = xbmc.LOGDEBUG)

    # Show notification about the error, including the first two lines
    # of the stderr output.
    max_index = 1
    if len(stdout_list) > 1:
            max_index = 2
    _error('%s' % '\n'.join(stderr_list[0:max_index]))


if __name__ == '__main__':
    main()
