#!/bin/bash 

#Usage: printPall.bash [thread name]

PID=`pgrep -l omniqu | awk '{print $1}'`

if [ -z $PID ]; then
	echo "omniqunifier not running"
	exit 0
fi

OMNIQCMDLN=/omniqdir/arch/x86_64/release/bin/omniqcmdln

FILTER=$1
INSTANCE=$2

function print_all_instances_fast_queue_stats
{
	cmd="ls /omniqdir/sysfiles/ | grep infifo | grep $1"
	if [ ! -z $FILTER ]; then 
		cmd=$cmd" | grep $FILTER"
	fi
	for infifo in `eval $cmd`; do
		process=`echo $infifo | awk -F_ '{print $2}'`
		thread_name=`echo $infifo | awk -F_ '{print $3}'`
		instance=`echo $infifo | awk -F_ '{print $4}'`
                if [ ! -z $INSTANCE ]; then
                        if [ $instance -ne $INSTANCE ]; then
                                continue;
                        fi
                fi
		echo "******   "$thread_name" "$instance"    ******"
		${OMNIQCMDLN} $process $thread_name $instance pall
		echo
	done
		
}

print_all_instances_fast_queue_stats OrderedCdrRouter
print_all_instances_fast_queue_stats IsupMerge
print_all_instances_fast_queue_stats TcapMerge
print_all_instances_fast_queue_stats OpenCalls
print_all_instances_fast_queue_stats Correlation
print_all_instances_fast_queue_stats RecordManager
print_all_instances_fast_queue_stats DBAgent
print_all_instances_fast_queue_stats Maintenance
print_all_instances_fast_queue_stats Actions
print_all_instances_fast_queue_stats ActionExe
print_all_instances_fast_queue_stats AggRouter
print_all_instances_fast_queue_stats AggBasicUnit
print_all_instances_fast_queue_stats AggSecondTier
print_all_instances_fast_queue_stats AggFinalizer
