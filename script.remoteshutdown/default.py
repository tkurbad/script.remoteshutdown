# Remote Shutdown

import subprocess
import xbmcaddon

# hostname example 'host.domain.com'
# sshpath example '/usr/bin/ssh'
# command example 'shutdown -hP now'

settings = xbmcaddon.Addon(id = 'script.remoteshutdown')
hostname = settings.getSetting('hostname')
sshpath = settings.getSetting('sshpath')
command = settings.getSetting('command')

subprocess.call(['%s' % sshpath, '-y', '-l', 'root',
        '%s' % hostname, '%' % command])
