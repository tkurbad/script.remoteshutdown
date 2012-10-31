# Remote Shutdown

import subprocess
import xbmcaddon

# hostname example 'host.domain.com'

settings = xbmcaddon.Addon(id = 'script.shutdown')
hostname = settings.getSetting('hostname')
sshpath = settings.getSetting('sshpath')
command = settings.getSetting('command')

subprocess.call(['%s' % sshpath, '-y', '-l', 'root',
        '%s' % hostname, '%' % command])
