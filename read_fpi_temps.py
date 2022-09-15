import argparse
import re
import datetime
import numpy as np
def fpi_temps_filereader(temps_datfile):
    """
    .. function: fpi_temps_filereader

    :synopsis: fpi_temps_filereader is the reader function for the FPI temperature data products files.

        The temperature data file as published by the FPI data analysis program has 2 segments \:

        * A header section with instrument parameters and summary statistics for the observation night
        * The temperature data products derived from each image in the observation night

    :Args:
    
        temps_datfile (str): The full pathname of the temperature data products file to be read
 
    :Returns: 
    
        temps_data (dict): A dictionary with the contents of the temperature data products file

    :rtype: 
    
    temps_data : dict[str, dict]
    dict of {
        "header" : dict,    # information from the header section of the temperature data products file  \n
        "data": dict        # temperature data \n
    }
    
    Example 1: Retrieve tempeture, termperature error estimates and time of measurement for zenith measurements \n
    
    .. code-block:: python

        # read in the temperature data products
        fpi_temps = fpi_temps_filereader(temps_file)
        temps_hdr = fpi_temps["header"]
        temps_data = fpi_temps["data"]
        # Get the indices corresponding to the zenith and 4 directions
        zenith_pos = np.where(temps_data["zn"] == 0)
        north_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 0))
        south_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 180))
        east_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 90))
        west_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 270))
        # gather the temperature measurements in the zenith direction
        tmid_z = temps_data["ut_mid"][zenith_pos]
        temp_z = temps_data["temp"][zenith_pos]
        e_temp_z = temps_data["e_temp"][zenith_pos]
        e_time_z = temps_data["e_time"][zenith_pos]

    Example 2: Retrieve tempeture, termperature error estimates and time of measurement for north and south measurements 
        and merge them as "meridional" measurements \n

    .. code-block:: python

        # read in the temperature data products
        fpi_temps = fpi_temps_filereader(temps_file)
        temps_data = fpi_temps["data"]
        # Get the indices corresponding to the north and south measurements
        north_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 0))
        south_pos = np.where( (temps_data["zn"] == 45) & (temps_data["az"] == 180))
        merid_pos = np.concatenate( (north_pos, south_pos), axis=None )
        # Gather the temperature and time measurements in the meridional direction
        tmid_m = temps_data["ut_mid"][merid_pos]
        temp_m = temps_data["temp"][merid_pos]    # temperature in Kelvin
        e_temp_m = temps_data["e_temp"][merid_pos]  # +/- error in temperature
        e_time_m = temps_data["e_time"][merid_pos]  # +/- error in time
        # sort them in ascending order of acquisition time
        merid_pos_sorted = np.argsort(tmid_m)
        tmid_m = tmid_m[merid_pos_sorted]
        temp_m = temp_m[merid_pos_sorted]    # temperature in Kelvin
        e_temp_m = e_temp_m[merid_pos_sorted]  # +/- error in temperature
        e_time_m = e_time_m[merid_pos_sorted]  # +/- error in time

    Following is the desciption of value of fpi_temps["header"] \n

    temps_hdr: dict[str, Any] \n
        dict of { \n
            "expt" : str, # experiment name \n
            "location_name" : str,          # location name \n
            "obs_date" : datetime.datetime, # observation date \n
            "latitude" : str,               # latitude (positive north, negative south) \n
            "longitude" : str,              # longitude (positive east, negative west) \n
            "version_num : float,           # software version number (major rev.minor rev) \n
            "hdr_lines" : list              # List of strings with the rest of the header lines from the data products files \n
        } \n

    Following is the desciption of value of fpi_temps["data"] \n
    temps_data : dict[str, numpy.ndarray] \n
            dict of { \n
                "imgno"  : numpy.ndarray of numpy.int32, # image sequence number \n
                "ut1"    :  numpy.ndarray of numpy.float32, # acquisition start time, in number of hours since start date \n
                "ut2"    :  numpy.ndarray of numpy.float32, # acquisition end time, in number of hours since start date \n
                "ut_mid" :  numpy.ndarray of numpy.float32, # timestamp at the middle of acquisition, in number of hours since start date \n
                "az" :  numpy.ndarray of numpy.float32, # Azimuth angle of look direction, in degrees \n
                "zn" :  numpy.ndarray of numpy.float32, # Zenith angle of look direction, in degrees \n
                "signal" :  numpy.ndarray of numpy.float32, # Relative signal strength, in A.D.U / pixel \n
                "e_signal" :  numpy.ndarray of numpy.float32, # Relative signal strength error estimate, in A.D.U / pixel \n
                "bkgnd" :  numpy.ndarray of numpy.float32, # Relative background , in A.D.U / pixel \n
                "e_bkgnd" :  numpy.ndarray of numpy.float32, # Relative background strength error estimate, in A.D.U / pixel \n
                "temp" :  numpy.ndarray of numpy.float32, # Temperature, in degrees K \n
                "e_temp" :  numpy.ndarray of numpy.float32, # Temperature error estimate, in degrees K \n
                "moon"   : numpy.ndarray of numpy.float32, # Percentage of the moon's synodic cycle \n
                "qcode" :  numpy.ndarray of numpy.float32, # Data quality code.  code=0 trustworthy;  code=1 be suspicious;  code=2 be dubious \n
            } \n
    """
    def read_float(string_lit):
        flt_val = float('NaN')
        try:
           flt_val = float(string_lit) 
        except:
            flt_val = float('NaN')
        return flt_val
        
    def temps_data_iterator():
        with open(temps_datfile, "r") as f:
            lines = f.readlines()
        for line in lines:
            # skip lines with just whitespace
            if line.isspace(): 
                continue
            line_stripped = line.strip()
            yield line_stripped

    def read_temp_header_details():
        """
            collect the header lines, which are the first few lines until the line with 
            the "SS-Analyze" string
        """
        temps_hdr_lines = list()
        for line in temps_datalines :
            temps_hdr_lines.append(line)
            if ('SS-Analyze' in line) :
                break
        # Get the name of the experiment (Redline, Greenline)
        expt = ''
        if( "Red".casefold() in (temps_hdr_lines[0]).casefold() ):
            loc_name_end_idx = (temps_hdr_lines[0].casefold()).find("Red".casefold()) - 1
            expt = "RedLine"
        if( "Green".casefold() in (temps_hdr_lines[0]).casefold() ):
            loc_name_end_idx = (temps_hdr_lines[0].casefold()).find("Green".casefold()) - 1
            expt = "GreenLine"

        # Get the location name (which is the entire string in line 0 preceding the experiment label)
        location_name = temps_hdr_lines[0][0:loc_name_end_idx]

        # Get the start date of the observation. Since the year is denoted by two digits, add 2000
        obs_date_yy = int(temps_hdr_lines[2][2:4])
        obs_date_yy += 2000
        obs_date_mon = int(temps_hdr_lines[2][4:6])
        obs_date_day = int(temps_hdr_lines[2][6:8])
        obs_date = datetime.datetime(obs_date_yy, obs_date_mon, obs_date_day)

        # get the version number
        versionNumberStr = re.split(' ', temps_hdr_lines[-1])[1]
        versionNumber = read_float(versionNumberStr[1:])

        latitude = float('NaN')
        longitude = float('NaN')
        for hdr_line in temps_hdr_lines:
            if ("latitude".casefold() in hdr_line.casefold()):
                # split the header line with lat and lon by delimiters, then remove 
                # empty strings, and then read the lat and lon from the list entities
                lat_lon_list = list(filter(None, re.split('[ \,]', hdr_line)))
                latitude = lat_lon_list[2]
                longitude = lat_lon_list[4]

        temps_hdr = {"expt" : expt,
            "location_name" :location_name,
            "obs_date" : obs_date,
            "latitude" : latitude,
            "longitude" : longitude,
            "version_num" : versionNumber,
            "hdr_lines" : temps_hdr_lines}

        return temps_hdr

    """
    read_temps_detail reads the temperature data products in each 
    the 5 look directions, and returns a named numpy structed array with the data product details
    """
    def read_temps_detail():
        """
        Skip the first couple of lines. The first line has the column names, and the 
        code will generate column names that correspond to the ones present in the .dat file.
        The second line has the units. skip this because the units are fixed for the columns.
        """
        skip_line = next(temps_datalines)
        skip_line = next(temps_datalines)
        # allocate structured array for each column in the table with temperature and errors
        temps_data = np.zeros(
            0,
            dtype={
                'names':
                # image tmid Etime   AZ    ZN   signal Esignal   bkgnd  Ebkgnd   temp    Etemp  moon code
                ('imgno', 'ut_mid', 'e_time', 'az', 'zn', 'signal', 'e_signal', 'bkgnd', 'e_bkgnd', 'temp', 'e_temp', 'moon', 'qcode'),
                'formats':('i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'i4')})
        #  assemble temperature details
        temps_record = next(temps_datalines)
        while( not('Raw data' in temps_record)): 
            temps_rec_cols = re.split(' +', temps_record)
            imgno = read_float(temps_rec_cols[0])
            ut_mid = read_float(temps_rec_cols[1])
            e_time = read_float(temps_rec_cols[2])
            az = read_float(temps_rec_cols[3])
            zn = read_float(temps_rec_cols[4])
            signal = read_float(temps_rec_cols[5])
            e_signal = read_float(temps_rec_cols[6])
            bkgnd = read_float(temps_rec_cols[7])
            e_bkgnd = read_float(temps_rec_cols[8])
            temp = read_float(temps_rec_cols[9])
            e_temp = read_float(temps_rec_cols[10])
            moon = read_float(temps_rec_cols[11])
            qcode = read_float(temps_rec_cols[12])
            # now populate the array with the values just read
            temps_data = np.append(temps_data,
                np.array([(imgno, ut_mid, e_time, az, zn, signal, e_signal, bkgnd, e_bkgnd, temp, e_temp, moon, qcode)],
                    dtype=temps_data.dtype))
            temps_record = next(temps_datalines)

        return temps_data
                       
    temps_datalines = temps_data_iterator()
    temps_hdr = read_temp_header_details()
    temps_data = read_temps_detail()
   # convert the temperature data products file contents to a dictionary
    temps_data_dict = dict()
    for col_name in temps_data.dtype.names:
        temps_data_dict[col_name] = temps_data[col_name]

    fpi_temps = {
        "header" : temps_hdr,
        "data" : temps_data_dict }
    return (fpi_temps)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "temps_datfile",type=str, help="The full path of the *temps.dat file to be parsed."
    )
    args = argument_parser.parse_args()

    fpi_temps = fpi_temps_filereader( args.temps_datfile)
    print ("temps header data:")
    print (fpi_temps["header"])
    print ("Temperature data products:")
    print (fpi_temps["data"])
