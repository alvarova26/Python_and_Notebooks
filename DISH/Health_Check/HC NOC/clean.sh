#!/bin/bash

rm -rf /var/lib/cloud/instance*
rm -rf /var/log/cloud-init*
yum clean all
rm -rf /etc/yum.repos.d/*
rm -rf /tmp/*
rm -rf /var/tmp/*
rm -rf /var/tmp/*tmp*
rm -f /var/lib/dhclient/dhclient*
rm -rf /etc/udev/rules.d/70-persistent-net.rules
history -c






