#!/bin/bash
T=$(echo $1 | bc)
TP=$(echo $2 | bc)
X=$(echo $3 | bc)
Y=$(echo $4 | bc)

alerts="./alerts.csv"
logs="./logs.csv"

for ((count=0;count<TP;count=count+T)); do
  #echo $(date +'%d/%m/%Y %H:%M:%S:%3N'), $(uptime | awk '{print $10,$11,$12}')
  upt=$(uptime)
  #echo $upt
  date=$(echo $upt | awk '{gsub(/[,;]/, ""); OFS=","; print $1}')
  one_min=$(echo $upt | awk '{gsub(/[,;]/, ""); OFS=","; print $10}' | bc)
  five_min=$(echo $upt | awk '{gsub(/[,;]/, ""); OFS=","; print $11}' | bc)
  fifteen_min=$(echo $upt | awk '{gsub(/[,;]/, ""); OFS=","; print $12}' | bc)
  #echo $one_min
  #echo $X
  if (( $(echo "$one_min > $X" | bc -l) ))
    then
      echo $date,"HIGH CPU USAGE",$one_min,$five_min,$fifteen_min >> $alerts
  fi
  #echo $(echo "$five_min > $Y" | bc -l)
  if [ $(echo "$five_min > $Y" | bc -l) == 1 ] && [ $(echo "$one_min > $X" | bc -l) == 1 ]
    then
      echo $date,"Very HIGH CPU usage",$one_min,$five_min,$fifteen_min >> $alerts
  fi
  echo $date,$one_min,$five_min,$fifteen_min >> $logs
  sleep 1
done

exit 0

