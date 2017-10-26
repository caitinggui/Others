#!/usr/bin/expect
puts "IP is 219, 23, 24, 50.46"
set ip1 192.168.10.219
# notice the space and format
if {$argc<1} {
    puts "Use default hostname 192.168.10.219"
    set serverip $ip1
} else {
    set hostname [lindex $argv 0]
    if {$hostname=="50.46"} {
        set serverip 192.168.
    } else {
        set serverip 192.168.10.
    }
# 拼接字符串
    append serverip $hostname
}
set timeout 60
set name caitinggui
spawn ssh $name@$serverip
expect "*password:"
    send "mypassword\r"
interact
