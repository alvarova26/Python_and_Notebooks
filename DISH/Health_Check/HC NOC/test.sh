count_15_min=0
for i in `cat /tmp/all_probe.txt`; do value=$(cat /tmp/SIP_probe_count.txt | grep -i $i); if [[ $value == '' ]]; then continue; else count_15_min=$((count_15_min + 1)); fi; echo $count_15_min ; done
