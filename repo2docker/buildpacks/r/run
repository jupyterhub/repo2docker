#!/usr/bin/env /bin/bash
echo "www-frame-origin=${CSP_HOSTS:-none}" >> /etc/rstudio/rserver.conf
echo  "server-app-armor-enabled=0" >> /etc/rstudio/rserver.conf
echo "session-default-working-dir=/WholeTale/workspace" >> /etc/rstudio/rsession.conf
echo "session-default-new-project-dir=/WholeTale/workspace" >> /etc/rstudio/rsession.conf
exec /usr/lib/rstudio-server/bin/rserver  --server-daemonize 0 --auth-none 1 --auth-validate-users 0
