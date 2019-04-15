source ./config.ini

command=$3

filename=$1
task_id=$2

file_name=$(basename $filename)

if [ ! -n "$task_id" ];then
	echo "Please give a task id"
	exit
fi

shard_max=100

if [ $shard_value -gt $shard_max ];then
	echo "shard value too large"
	exit
fi



splite(){
	mkdir -p ${file_name}-splite
        if [ ! -f "$filename" ];then
            echo "Current file doesn't exist"
            rm -rf ${file_name}-splite
            exit
        fi
    	split -C ${shard_value}M  $filename ${file_name}-splite/${file_name}_
        
}


if [ ! -n "$command" ];then
	splite
	python src/get_task_id.py $server $task_id $user_id | python src/upload.py $server $file_name $user_id | python src/merge.py $server $file_name $user_id
	rm -rf ${file_name}-splite
else
	echo "Error Argument"
fi

