import argparse
import re
import datetime
import numpy as np
"""
    fpi_temps_filereader is the reader function for the FPI Temperature data products files.
     The temperature data file as published by the FPI data analysis program has 2 segments:
    -- A header section with instrument parameters and summary statistics for the observation night
    -- The temperature data products derived from each image in the observation night
"""
def fpi_temps_filereader(temps_datfile):
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
        if( "Redline".casefold() in (temps_hdr_lines[0]).casefold() ):
            expt = "Redline"
        if( "GreenLine".casefold() in (temps_hdr_lines[0]).casefold() ):
            expt = "GreenLine"

        # Get the location name (which is the entire string in line 0 preceding the experiment label)
        loc_name_end_idx = (temps_hdr_lines[0].casefold()).find(expt.casefold()) - 1
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
        # allocate structured array for each column in the table with winds and errors
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
   # convert the vertical winds np array  to a dictionary
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
