#!/bin/sh

STATION_ID="sta01"
CSV_FILE="/tmp/weather-last-month.csv"
YEAR=$(date --date="$(date +'%Y-%m-%d') -1 day" +%Y)
MONTH=$(date --date="$(date +'%Y-%m-%d') -1 day" +%m)
#OUTPUT_FILE="/home/pavel/Pictures/weather_${YEAR}_${MONTH}_${STATION_ID}_temperature.png"
OUTPUT_FILE="/home/pavel/dev-py/pico_weather_station/server/assets/img/weather_${YEAR}_${MONTH}_${STATION_ID}_temperature.png"
LAST_DAY=$(cal $MONTH $YEAR | awk 'NF {DAYS = $NF}; END {print DAYS}')

# TODO: add to database as a view
SQL_QUERY=$(cat <<EOF
\copy (
  SELECT
    EXTRACT(DAY FROM timestamp) AS day,
    AVG(temperature) as avg_temperature,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature
  FROM weather_data
  WHERE (station_id = '${STATION_ID}') 
    AND (EXTRACT(YEAR  FROM TIMESTAMP) = ${YEAR})
    AND (EXTRACT(MONTH FROM TIMESTAMP) = ${MONTH})
  GROUP BY day
  ORDER BY day
) TO STDOUT WITH CSV HEADER
EOF
)

GNUPLOT_SCRIPT=$(cat <<EOF
set term pngcairo size 800,480 font "Monoid,8";
set datafile separator ',';
set grid ;
set xtics 1;
set xrange [0.5:${LAST_DAY}.5];
set output "${OUTPUT_FILE}";
set ylabel "Temperature (°C)";
set title 'Daily temperatures for station: ${STATION_ID}, month ${YEAR}-${MONTH}';
plot "${CSV_FILE}" using 1:((\$2+\$3)/2):(0.4):((\$3-\$2)/2) with boxxyerrorbars title "Temperature Range" lc rgb "#d08770" fs solid 0.5;
EOF
)
# set xrange [1:${LAST_DAY}];

# Export data to CSV
psql -h ~/postgre-sockets -d weather_data -c "$SQL_QUERY" > "$CSV_FILE"

# Check if CSV export succeeded
if [ ! -s "$CSV_FILE" ]; then
  echo "Error: CSV file is empty or not created."
  exit 1
fi
echo "HERE"
gnuplot -e "$GNUPLOT_SCRIPT"
echo "$GNUPLOT_SCRIPT" > .gnuplot
