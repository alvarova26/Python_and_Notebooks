#!/bin/bash


echo "Current system date : " >/tmp/shortHC_output.txt
#echo "############################################" >>/tmp/shortHC_output.txt

ssh -q  deployment@10.228.101.39 "sudo date" >> /tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt
echo "Ping status" >> /tmp/shortHC_output.txt
sh /home/deployment/Ping.sh >> /tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt
echo "QLoader Service Check" >>/tmp/shortHC_output.txt
##### Qloader status
#echo "############################################" >>/tmp/shortHC_output.txt

ssh deployment@10.228.101.23 "sudo service qloader status" >> /tmp/shortHC_output.txt


echo "############################################" >>/tmp/shortHC_output.txt
echo "Qrouter Service Check" >>/tmp/shortHC_output.txt

ssh deployment@10.228.101.28 "sudo service qrouter status|grep QRouter" >> /tmp/shortHC_output.txt



echo "############################################" >>/tmp/shortHC_output.txt

echo "Qrouter Drop status" >>/tmp/shortHC_output.txt


qrouter_drop=$(ssh deployment@10.228.101.28 "sudo sh /tmp/qrouter.sh")
qrouter_drop=$(echo $qrouter_drop | sed 's/ //g')
if [[ $qrouter_drop == "0" ]]
then
  qr_drop="NO"
else
  qr_drop="YES"
fi
echo -e "QRouter Drops"'\t\t'$qr_drop >>/tmp/shortHC_output.txt


echo "############################################" >>/tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt
echo "Processing  Drop status" >>/tmp/shortHC_output.txt


sleep 2



for i in 10.228.101.58 10.228.103.228 10.228.101.238; do op=$(ssh -q deployment@$i "sudo /omniqdir/scripts/OpenFifo/printPall.bash Action|grep -i Dropped|tail -1"); echo $i "|" $op;done  >>/tmp/shortHC_output.txt

sleep 12

echo "                                                           "  >>/tmp/shortHC_output.txt
echo "Processing  Total Received Full CDRs" >>/tmp/shortHC_output.txt
for i in 10.228.101.58 10.228.103.228 10.228.101.238; do op=$(ssh -q deployment@$i "sudo /omniqdir/scripts/OpenFifo/printPall.bash Action|grep -i 'Total Received Full CDRs'"); echo $i "|" $op;done  >>/tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt
echo "Processing Rate of Cdrs Received " >>/tmp/shortHC_output.txt
for i in 10.228.101.58 10.228.103.228 10.228.101.238; do op=$(ssh -q deployment@$i "sudo /omniqdir/scripts/OpenFifo/printPall.bash Action|grep -i 'Rate of Cdrs Received'"); echo $i "|" $op;done  >>/tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt


#Vertica Checks
echo "############################################" >>/tmp/shortHC_output.txt
echo "Vertica  top 5 nodes with storage_usage ">>/tmp/shortHC_output.txt
ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c " SELECT node_name, storage_usage, (sum(disk_space_used_mb)*100/sum(disk_space_free_mb + disk_space_used_mb))::int storage_usage_percent  FROM disk_storage where storage_usage <> USER GROUP BY 1, 2  having (sum(disk_space_used_mb)*100/sum(disk_space_free_mb + disk_space_used_mb))::int > 5 ORDER BY 3 desc limit 5; " '>> /tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt

echo "Vertica clusterCheck" >>/tmp/shortHC_output.txt

ssh -q  deployment@10.228.101.39"sudo su -l dbadmin -c '/opt/vertica/bin/admintools -t view_cluster'"  >> /tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt

ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select * from nodes;" ' >/tmp/vertica_nodes_status.txt;
cat /tmp/vertica_nodes_status.txt|awk -F"|" '{print $1 $3 $6}'   >> /tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt
####echo "########## Vertica Disk Space >80% Threshold ##############" >>/tmp/shortHC_output.txt



echo "############################################" >>/tmp/shortHC_output.txt



ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select * from mv_execution" '  >> /tmp/shortHC_output.txt

echo "############################################" >>/tmp/shortHC_output.txt
echo "########## Vertica Bad file status (It will display latest file if any)  ##############" >>/tmp/shortHC_output.txt


for i in 10.228.101.39 10.228.103.243 10.228.101.202 10.228.101.16 10.228.103.251 10.228.101.229 10.228.101.59   ; do  op=$(ssh -q deployment@$i "sudo hostname"); count=$(ssh -q deployment@$i "sudo ls -lrth  /radcom/omniq/QLoader |grep -i .bad|wc -l "); echo $i "|" $op "|" $count; done >> /tmp/shortHC_output.txt


echo "############################################" >>/tmp/shortHC_output.txt


echo "                                                           "  >>/tmp/shortHC_output.txt
echo "                                                           "  >>/tmp/shortHC_output.txt


echo "########## BE VMs Disk Space >90% Threshold ##############" >>/tmp/shortHC_output.txt



for i in `cat /home/deployment/iplist_tocheck_ssh.txt` ; do op=$(ssh -q deployment@$i "sudo hostname";ssh -q deployment@$i "sudo df -khP" | grep -v Filesystem| sed 's/%//g' |awk '($5>=90)'|grep -v boot); echo $i "|" $op; done >> /tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt
echo "                                                           "  >>/tmp/shortHC_output.txt

echo "########## CRM STATUS For all VMs  ##############" >>/tmp/shortHC_output.txt


echo "############################################" >>/tmp/shortHC_output.txt

>/tmp/crm_status_output.txt
for i in 10.228.101.18 10.228.101.36 10.228.101.21 10.228.101.23 ; do ssh -q deployment@$i "sudo crm status"; done>>/tmp/crm_status_output.txt;
crm_stat=`cat /tmp/crm_status_output.txt|egrep -i "FaILED|STOP|ERROR|NOK"|wc -l`
if [ $crm_stat -eq 0 ] ; then    echo "CRM STATUS             : OK" | tee -a /tmp/crm_status_output.txt; else    echo "CRM STATUS             : NOK,please check output file /tmp/crm_status_output.txt for details  " | tee -a /tmp/crm_status_output.txt; fi >>/tmp/shortHC_output.txt


echo "                                                           "  >>/tmp/shortHC_output.txt
echo "                                                           "  >>/tmp/shortHC_output.txt


echo "################# MGU Critical Alarms Top 20 (for complete list check /tmp/MGUALARMS.txt) ###########################" >>/tmp/shortHC_output.txt
echo "############################################" >>/tmp/shortHC_output.txt


ssh deployment@10.228.103.215  "sudo sh /tmp/MGU_alarm_critical_checks_shd.sh" >/tmp/MGUALARMS.txt ;

 head -20 /tmp/MGUALARMS.txt >>/tmp/shortHC_output.txt





echo "                                                           "  >>/tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt




echo "############# Data  validation in  DB  ############# ">/tmp/DataDelay_status.txt

echo "Delay_Diameter:">>/tmp/DataDelay_status.txt
ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select (sysdate - max(start_time))Delay_Diameter from omniq.cdr_hpa_diameter;" ' >>/tmp/DataDelay_status.txt
echo "Delay_SIP:">>/tmp/DataDelay_status.txt
ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select (sysdate - max(start_time))Delay_Diameter from omniq.cdr_hpa_sip;" ' >>/tmp/DataDelay_status.txt
echo "Probe count last 15 min in SIP:">>/tmp/DataDelay_status.txt
ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select measuring_probe_name,count(*) from omniq.cdr_hpa_sip where start_time > sysdate -15/1440 group by 1 order by 1;" ' >>/tmp/DataDelay_status.txt
echo "Probe count last 15 min in Diameter:">>/tmp/DataDelay_status.txt
ssh -q  deployment@10.228.101.39 '/opt/vertica/bin/vsql -U omniq -w radcom -t -c "select measuring_probe_name,count(*) from omniq.cdr_hpa_diameter where start_time > sysdate -15/1440 group by 1 order by 1;" ' >>/tmp/DataDelay_status.txt


echo "                                                           "  >>/tmp/shortHC_output.txt

echo "                                                           "  >>/tmp/shortHC_output.txt


echo "#############Total number of FE machines ############" >>/tmp/shortHC_output.txt
cond=127.0.0.1 types="vprobe|vLB|vLBAgent"; curl -sg http://$cond:8084/MaveriQConductor/machines | awk '/Clusters:/{exit};$0~/type=('$types')/{l_print=1};l_print==1&&/site=/{l_print=0;match($0,/=/);print substr($0,RSTART+1)}' | sort -u | while read site; do echo $'\n\n'\#$site; curl -sg http://$cond:8084/MaveriQConductor/machines | awk -v "OFS=\t" '/Clusters:/{exit};/name=/{match($0,/=([^.]+)/);name=substr($0,RSTART+1,RLENGTH-1);l_print=0};$0~/type=('$types')/{l_print=1};/attributes=/{match($0,/_oam_direct_net_1:([^;]+)/);ip_direct=substr($0,RSTART+18,RLENGTH-18)};l_print==1&&/site='$site'$/{print ip_direct,name}' | sort -k2; done >>/tmp/shortHC_output.txt 

sh /tmp/Probe_DataValidationChecks.sh > /tmp/DISH_Probe_status.txt

cat /tmp/shortHC_output.txt >/tmp/DISH_system_hc_status_new.txt


cat /tmp/DataDelay_status.txt >> /tmp/DISH_system_hc_status_new.txt

cat /tmp/DISH_Probe_status.txt >> /tmp/DISH_system_hc_status_new.txt

chmod 777 /tmp/DISH_system_hc_status_new.txt



cat /tmp/DISH_system_hc_status_new.txt

