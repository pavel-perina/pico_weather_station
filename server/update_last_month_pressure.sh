#!/bin/sh

STATION_ID="sta01"
CSV_FILE="/tmp/weather-last-month.csv"
YEAR=$(date --date="$(date +'%Y-%m-%d') -1 day" +%Y)
MONTH=$(date --date="$(date +'%Y-%m-%d') -1 day" +%m)
NEXT_MONTH=$(date --date="$(date +'%Y-%m-%d') -1 day +1 month" +%m)
OUTPUT_FILE="/home/pavel/dev-py/pico_weather_station/server/weather_${YEAR}_${MONTH}_${STATION_ID}_pressure.png"
LAST_DAY=$(cal $MONTH $YEAR | awk 'NF {DAYS = $NF}; END {print DAYS}')

# TODO: add to database as a view
SQL_QUERY=$(cat <<EOF
\copy (
  SELECT
    DATE_TRUNC('hour', timestamp) AS date_time,
    AVG(pressure_at_station)*.01   as pressure_at_station,
    AVG(pressure_at_sea_level)*.01 as pressure_at_sea_level
  FROM weather_data
  WHERE (station_id = '${STATION_ID}') 
    AND (EXTRACT(YEAR  FROM TIMESTAMP) = ${YEAR})
    AND (EXTRACT(MONTH FROM TIMESTAMP) = ${MONTH})
  GROUP BY date_time
  ORDER BY date_time
) TO STDOUT WITH CSV HEADER
EOF
)

GNUPLOT_SCRIPT=$(cat <<EOF
set term pngcairo size 800,480 font "Monoid,8";
set datafile separator ',';
set xdata time;
set timefmt '%Y-%m-%d %H:%M:%S';
set format x '%d';
set grid;
set output "${OUTPUT_FILE}";
set ylabel "Pressure (hPa)";
set xrange [ "${YEAR}-${MONTH}-01 00:00:00" : "${YEAR}-${MONTH}-${LAST_DAY} 23:59:59" ];
set xtics "${YEAR}-${MONTH}-01 00:00:00", 86400;
set title 'Daily temperatures for station: ${STATION_ID}, month ${YEAR}-${MONTH}';
plot "${CSV_FILE}" using 1:2 with lines title "Pressure at station" lc rgb "#a3be8c",
 "${CSV_FILE}" using 1:3 with lines title "Pressure at sea level" lc rgb "#5e81ac";
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

