#!/bin/bash
function join_array { 
    local IFS="$1"; shift; echo "$*"; 
}
function create_genre_array {
    genres=$1
    IFS="|" read -a genre_array <<< $genres
    genres_json=$(join_array ',' ${genre_array[@]})
    genres_json=$(echo $genres_json| sed 's/,/","/g')
    echo "[\"${genres_json}\"]"
}


exec < movies.csv
elasticsearch_host=$(echo "http://${1}:9200/${2}/_doc")
echo $elasticsearch_host
read header
while IFS="," read -r movieId title genres 
do 
  title=$(echo ${title}|tr '"' " ")
  echo $title
  length=${#title}
  if [ $length -gt 7 ]
  then
    year=$(echo $title| cut -c"$((length-7))-$((length-1))"| tr -dc "0-9")
    title=$(echo $title| cut -c"1-$((length-7))")
    
    genres_json=$(create_genre_array $genres)
    echo "$movieId $title $year $genres_json"

    echo "$(curl -XPUT "$elasticsearch_host/$movieId" -H 'Content-Type: application/json' -d"{\"title\": \"$title\", \"year\": \"$year\", \"genres\":$genres_json }"))"
  fi
done