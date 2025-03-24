#!/bin/sh

STATION_ID="sta01"
CSV_FILE="/tmp/weather-recent.csv"
OUTPUT_FILE_PREFIX="/home/pavel/dev-py/pico_weather_station/server/assets/img/weather_${STATION_ID}_recent_"

# TODO: add to database as a view
SQL_QUERY=$(cat <<EOF
\copy (
  SELECT *
  FROM last_three_days
  WHERE (station_id = '${STATION_ID}') 
) TO STDOUT WITH CSV HEADER
EOF
)

GNUPLOT_SCRIPT=$(cat <<EOF
set term pngcairo size 800,480 font "Monoid,8";
set datafile separator ',';
set xdata time;
set x2data time;
set timefmt '%Y-%m-%d %H:%M:%S';
set grid xtics ytics;
set xtics "2025-01-01 00:00:00", 14400;
set x2tics "2020-01-01 00:00:00",86400;
set mxtics 4;
set format x '%H';
set format x2 '%m-%d';
set output "${OUTPUT_FILE_PREFIX}pressure.png";
set xlabel "Hour";
set x2label "Date";
set ylabel "Pressure (hPa)";
set title 'Recent pressure for station: ${STATION_ID}';
plot "${CSV_FILE}" using 2:(\$5*0.01) with lines title "Pressure at station" lc rgb "#a3be8c",
 "${CSV_FILE}" using 2:(\$7*0.01) with lines title "Pressure at sea level" lc rgb "#5e81ac";
set output "${OUTPUT_FILE_PREFIX}temperature.png";
set ylabel "Temperature (C)";
set title 'Recent temperature for station: ${STATION_ID}';
plot "${CSV_FILE}" using 2:3 with lines title "Temperature" lc rgb "#d08770",
 "${CSV_FILE}" using 2:6 with lines title "Dew point" lc rgb "#b48ead";
set output "${OUTPUT_FILE_PREFIX}humidity.png";
set ylabel "Humidity)";
set yrange [0:100];
set title 'Recent humidity for station: ${STATION_ID}';
plot "${CSV_FILE}" using 2:4 with lines title "Relative[%]" lc rgb "#8fbcbb",
 "${CSV_FILE}" using 2:(\$8*1000) with lines title "Specific[g/kg]" lc rgb "#88c0d0";
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

gnuplot -e "$GNUPLOT_SCRIPT"
#echo "$GNUPLOT_SCRIPT" > .gnuplot

