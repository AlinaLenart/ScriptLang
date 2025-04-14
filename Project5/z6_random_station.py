import csv
import random
from pathlib import Path
import statistics
from z6_logger import logger


# finds a random station that measures a given compound within a given time range
def find_random_station(compound: str, frequency: str, start: str, end: str, 
                        measurements_dir: Path = Path("measurements"),
                        stations_file: Path = Path("stacje.csv")) -> tuple:
    
    try:
        measurement_file = find_measurement_file(compound, frequency, measurements_dir)

        if not measurement_file:
            logger.critical(f"CRITICAL ERROR: No measurement file found for {compound} {frequency}")
            return None, None

        station_codes = get_stations_in_time_range(measurement_file, start, end)

        if not station_codes:
            logger.warning("No stations found with data in the specified time range")
            return None, None

        random_station_code = random.choice(station_codes)
        logger.debug(f"Randomly selected station: {random_station_code}")
        
        name, address = get_station_metadata(random_station_code, stations_file)
        if not name or not address:
            logger.error(f"Failed to get metadata for station {random_station_code}")
        return name, address

    except Exception as e:
        logger.critical(f"CRITICAL ERROR in find_random_station: {str(e)}")
        return None, None

# finds a csv file with measurements for a specific compound and frequency
def find_measurement_file(compound: str, frequency: str, measurements_dir: Path) -> Path:

    try:
        for file in measurements_dir.glob(f"*_{compound}_{frequency}.csv"):
            logger.info(f"Found measurement file: {file}")
            return file
        return None
    except Exception as e:
        logger.critical(f"CRITICAL ERROR searching for measurement file: {str(e)}")
        return None

# returns a list of station codes that have data in the specified date range, expects dates in format MM/DD/YY HH:MM
def get_stations_in_time_range(measurement_file: Path, start_date: str, end_date: str) -> list:
    
    # set to avoid duplicates
    valid_stations = set()
    try:
        logger.info(f"Opening measurement file: {measurement_file}")
        with open(measurement_file, 'r', encoding='utf-8') as f:

            reader = csv.reader(f)
            # skip header
            next(reader)  
            # read station codes
            station_codes_row = next(reader)  
            station_codes = station_codes_row[1:] 

            # skip next 3 lines: wskaźnik, czas uśredniania, Jednostka
            for _ in range(3):
                next(reader)

            # iterate through measurement data
            for row in reader:
                # skip empoty lines
                if not row: 
                    continue
                try:
                    # get DATE MM/DD/YYYY HH:mm from first column and check if in range
                    date_str = row[0].strip()
                    if start_date <= date_str <= end_date:
                        # for each station column (skipping first) checking value if not empty (5,,5)
                        for i, value in enumerate(row[1:]):
                            if value.strip():
                                # taking station code value and adding it to set
                                valid_stations.add(station_codes[i])
                    logger.debug(f"Processed row ({len(str(row))} bytes)")
                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    # continue
    except FileNotFoundError:
        logger.critical(f"CRITICAL ERROR: Measurement file not found: {measurement_file}")
        return []
    except Exception as e:
        logger.critical(f"CRITICAL ERROR processing measurement file: {str(e)}")
        return []
    
    logger.info(f"Closing file: {measurement_file}")
    return list(valid_stations)

# returns station name and address based on station code.
def get_station_metadata(station_code: str, stations_file: Path) -> tuple:
    try:
        logger.info(f"Opening stations file: {stations_file}")
        with open(stations_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row['Kod stacji'] == station_code:
                    name = row.get('Nazwa stacji', '').strip()
                    address = row.get('Adres', '').strip()
                    logger.info(f"Found metadata for station: {station_code}")
                    
                    return name, address

        logger.warning(f"No data found for this station code: {station_code}")
        return None, None

    except FileNotFoundError:
        logger.critical(f"CRITICAL ERROR: Stations file not found: {stations_file}")
        return None, None
    except Exception as e:
        logger.critical(f"CRITICAL ERROR reading stations file: {str(e)}")
        return None, None

# returns a list of float measurements for a specific station in the given time range
def get_station_measurements(measurement_file: Path, station_code: str, 
                              start_date: str, end_date: str) -> list[float]:

    measurements = []
    station_index = None

    try:
        logger.info(f"Opening measurement file: {measurement_file}")
        with open(measurement_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # skip headers
            next(reader) 
            for _ in range(4):
                next(reader)

            # read station_codes
            station_codes_row = next(reader)
            # finding column index with given station code
            for i, code in enumerate(station_codes_row[1:]):
                # because thats how station code looks in measurements: DsGlogWiStwo-PM10-24g (match by prefix)
                if code.startswith(f"{station_code}-"):
                    station_index = i + 1
                    break
            
            # station not found return empty list
            if station_index is None:
                logger.warning(f"Station {station_code} not found in file {measurement_file}")
                return []

            # iterate over measurement rows
            for row in reader:
                if not row:
                    # skip empty
                    continue
                try:
                    # read and check date
                    date_str = row[0].strip()
                    if start_date <= date_str <= end_date:
                        # taking value from calculated column
                        value = row[station_index].strip()
                        if value:
                            # convert to float (no need in this case, but given in task intro)
                            measurements.append(float(value.replace(",", ".")))
                    logger.debug(f"Processed row ({len(str(row))} bytes)")
                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    # continue

    except FileNotFoundError:
        logger.critical(f"CRITICAL ERROR: Measurement file not found: {measurement_file}")
        return []
    except Exception as e:
        logger.critical(f"CRITICAL ERROR reading measurements: {str(e)}")
        return []

    logger.info(f"Closing file: {measurement_file}")
    return measurements


# calculates mean and standard deviation for measurements of a given station
def calculate_stats(stationcode: str, compound: str, frequency: str, start: str, end: str, 
                    measurements_dir: Path = Path("measurements")) -> tuple:
    
    try:
        measurement_file = find_measurement_file(compound, frequency, measurements_dir)
        if not measurement_file:
            logger.error(f"No file found for {compound} {frequency}")
            return None, None

        measurements = get_station_measurements(measurement_file, stationcode, start, end)
        if not measurements:
            logger.warning(f"No data for station {stationcode} in the specified time range")
            return None, None

        avg = statistics.mean(measurements)
        stdev = statistics.stdev(measurements) if len(measurements) > 1 else 0.0
        logger.info(f"Calculated stats for {stationcode}: avg={avg:.2f}, std={stdev:.2f}")
        return avg, stdev
    except Exception as e:
        logger.critical(f"CRITICAL ERROR in calculate_stats: {str(e)}")
        return None, None
