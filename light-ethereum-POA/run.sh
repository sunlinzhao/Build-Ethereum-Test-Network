#!/bin/bash
# /root/light-ethereum/run.sh

bash initial.sh
sleep 1
bash create.sh
sleep 1
bash buildLink.sh
sleep 1
bash send_enode.sh
sleep 1
bash across_build.sh
sleep 1
bash unlockAccount.sh
sleep 1
bash monitor.sh
sleep 1
# bash start_mining.sh
