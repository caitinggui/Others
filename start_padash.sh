#! /bin/env bash 
                         
function help() {
    echo "parameters:"   
    echo "-h or --help   | 查看说明"
    echo "-l path, --log path   log files to make available for psdash. Patterns (e.g."
    echo "              /var/log/**/*.log) are supported. This option can be"
    echo "              used multiple times."                                                                                                                                                                    
    echo "--register-to host:port"
    echo "              The psdash node running in web mode to register this"
    echo "              agent to on start up. e.g 10.0.1.22:5000."
    echo "              Default is 192.168.10.219:11119"
    echo "-m mode --mode mode"
    echo "              The mode of psdash.It can be 'master' or 'agent', default is 'master'"

}

index=0
mode="master"
port=11119
while true ; do                
    case "$1" in               
        -h|--help)                
            help
            exit 1;;                  
        -l|--log)
            path[$index]=$2           
            let index+=1
            shift 2 ;;
        -m|--mode)
            mode=$2
            shift 2 ;;
        --register-to)
            host=$2
            shift 2 ;;
        --)
            shift ; break ;;          
        *)
            break;;
    esac
done
echo ${path[*]}

if [ $mode = 'master' ]
then
    echo "start psdash master"
    psdash -a
elif [ $mode = 'agent' ]
then
    echo "start psdash rpc"
    psdash -a --register-to http://192.168.10.219:11119
fi 
