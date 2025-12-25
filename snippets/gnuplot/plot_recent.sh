#!/bin/sh

DATE=$(date +%Y%m%d) # Current date in YYYYMMDD format
STATION_ID="sta01"
CSV_FILE="/tmp/weather-recent.csv"
OUTPUT_FILE_TEMPERATURE="/home/pavel/Pictures/weather_${DATE}_${STATION_ID}_temperature_recent.png"
OUTPUT_FILE_PRESSURE="/home/pavel/Pictures/weather_${DATE}_${STATION_ID}_pressure_recent.png"

# Define SQL Query

SQL_QUERY=$(cat <<EOF
\copy (
  SELECT 
    timestamp, 
    temperature, 
    humidity, 
    pressure_at_station*0.01 as pressure_at_station,
    dew_point, 
    pressure_at_sea_level*0.01 as pressure_at_sea_level, 
    specific_humidity
  FROM weather_data
  WHERE (station_id = '${STATION_ID}') 
    AND (timestamp >= NOW() - INTERVAL '72 hours')
) TO STDOUT WITH CSV HEADER
EOF
)

# Define gnuplot script - must end with semi-colon and not contain comments, it's parsed as a single line

GNUPLOT_SCRIPT=$(cat <<EOF
set term pngcairo size 800,480 font "Monoid,8";
set datafile separator ',';
set xdata time;
set timefmt '%Y-%m-%d %H:%M:%S';
set format x '%H:%M';
set grid;
set output "${OUTPUT_FILE_TEMPERATURE}";
set ylabel "Temperature (C)";
set title 'Recent temperature for station: ${STATION_ID}';
plot "${CSV_FILE}" using 1:2 with lines title 'temperature', \
     "${CSV_FILE}" using 1:5 with lines title 'dew point';
set output "${OUTPUT_FILE_PRESSURE}";
set ylabel "Pressure (hPa)";
set title 'Recent pressure for station: ${STATION_ID}';
plot "${CSV_FILE}" using 1:4 with lines title 'station', \
     "${CSV_FILE}" using 1:6 with lines title 'sea level';
EOF
)

# Export data to CSV
psql -h ~/postgre-sockets -d weather_data -c "$SQL_QUERY" > "$CSV_FILE"

# Check if CSV export succeeded
if [ ! -s "$CSV_FILE" ]; then
  echo "Error: CSV file is empty or not created."
  exit 1
fi

gnuplot -e "$GNUPLOT_SCRIPT"

#echo "$GNUPLOT_SCRIPT" > .gnuplot


