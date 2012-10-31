# Remote Shutdown

import subprocess
import xbmcaddon

# hostname example 'host.domain.com'

settings = xbmcaddon.Addon(id = 'script.shutdown')
hostname = settings.getSetting('hostname')

subprocess.call(['/usr/bin/ssh', '-y', '-l', 'root',
        '%s' % hostname, 'shutdown -hP now'])

