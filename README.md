install 1.11 works on Ubuntu 20.04 ... not 1.12

https://projectaweek.com/2016/11/29/network-caller-id-ncid-install-on-raspberry-pi/
http://ncid.sourceforge.net/index.html
https://sourceforge.net/p/ncid/wiki/Home/
https://sourceforge.net/projects/ncid/files/ncid/1.12/#debian-based-os-packages
http://ncid.sourceforge.net/doc/NCID-UserManual.html#faq_top
http://ncid.sourceforge.net/doc/NCID-UserManual.html#instl_deb_top
https://sourceforge.net/p/ncid/wiki/Steps%20to%20install%20and%20configure%20minicom%20on%20a%20Raspberry%20Pi/

Welcome to minicom 2.7.1

OPTIONS: I18n
Compiled on Dec 23 2019, 02:06:26.
Port /dev/ttyUSB0, 16:32:28

Press CTRL-A Z for help on special keys

at
OK

RING

sudo ncidd -C /etc/ncid/ncid.conf -D

sudo vim /etc/ncid/ncidd.conf
set ttyclocal = 1
set ttyport = /dev/ttyUSB0
set lockfile = /var/lock/LCK..ttyUSB0

sudo systemctl status 

tones@manager1:/etc/ncid$ sudo apt list | grep -i ncid

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libkf5incidenceeditor-bin/focal 19.12.3-0ubuntu1 amd64
libkf5incidenceeditor-data/focal 19.12.3-0ubuntu1 all
libkf5incidenceeditor-dev/focal 19.12.3-0ubuntu1 amd64
libkf5incidenceeditor5abi2/focal 19.12.3-0ubuntu1 amd64
ncid/now 1.11-1 amd64 [installed,local]
r-cran-seroincidence/focal 2.0.0-1 all
rancid-cgi/focal 3.11-1 all
rancid/focal 3.11-1 amd64

tones@manager1:/etc/ncid$ sudo systemctl status ncidd.service
● ncidd.service - Network Caller ID server
     Loaded: loaded (/lib/systemd/system/ncidd.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-09-15 17:20:04 EDT; 3min 34s ago
       Docs: man:ncidd(8)
    Process: 5852 ExecStart=/usr/sbin/ncidd --pidfile /run/ncidd.pid (code=exited, status=0/SUCCESS)
   Main PID: 5870 (ncidd)
      Tasks: 1 (limit: 4468)
     Memory: 388.0K
     CGroup: /system.slice/ncidd.service
             └─5870 /usr/sbin/ncidd --pidfile /run/ncidd.pid

Sep 15 17:20:02 manager1 systemd[1]: Starting Network Caller ID server...
Sep 15 17:20:04 manager1 systemd[1]: Started Network Caller ID server.

https://rcwd.dev/long-lived-python-scripts-with-supervisor.html
https://jayden-chua.medium.com/use-supervisor-to-run-your-python-tests-13e91171d6d3
supervisord -c supervisord.conf

[program:test_process]
command=python -u supervisord_test.py
directory=/home/tones/code/log-to-mqtt-send-to-ha
stdout_logfile=/home/tones/code/log-to-mqtt-send-to-ha/test_process_output.txt
redirect_stderr=true