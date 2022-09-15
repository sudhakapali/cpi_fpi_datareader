import sys
import argparse
import re
import datetime
import numpy as np
def fpi_winds_filereader(winds_datfile):
    """   
    .. function: fpi_winds_filereader

    :synopsis: fpi_winds_filereader is the reader function for the FPI Winds data products files
   
    The winds data file as published by the FPI data analysis program has 4 segments

    * A header section with instrument parameters and summary statistics for the observation night
    * Meridional winds
    * Zonal winds
    * The relative vertical winds

    :Args:
    
        winds_datfile (str): The full pathname of the winds data products file to be read

    :return: A dictionary with the contents of the winds data products file.

    :rtype: dict

    winds_data : dict[str, dict]
    dict of {
        "header" : dict,    # information from the header section of the data products file  \n
        "meridional": dict, # meridional winds data \n
        "zonal": dict,      # zonal winds data \n
        "vertical": dict    # meridional winds data \n
    }
    
        Example 1:  Retrieve meridional winds, meridional winds error estimates and UT time for \n
        each meridional measurement. \n

        .. code-block:: python

            fpi_winds = fpi_winds_filereader(winds_file) 
            winds_hdr = fpi_winds["header"]              
            merid_winds = fpi_winds["meridional"]
            # extract meridional wind velocity
            m_wind = merid_winds["wind"]
            m_wind_err = merid_winds["wind_err"]
            # extract UT time of the meridional wind measurement
            m_ut_time = merid_winds["ut_mid"]
      
        Example 2:  Retrieve zonal winds, zonal winds error estimates and UT time for \n
        each zonal measurement. \n

        .. code-block:: python

            fpi_winds = fpi_winds_filereader(winds_file) 
            zonal_winds = fpi_winds["zonal"]
            # extract zonal wind velocity
            z_wind = zonal_winds["wind"]
            z_wind_err = zonal_winds["wind_err"]
            # extract UT time of the zonal wind measurement
            z_ut_time = zonal_winds["ut_mid"]

        :Type Description for fpi_winds["header"]: 

        winds_hdr: dict[str, Any] \n
            dict of { \n
                "expt" : str, # experiment name \n
                "location_name" : str,          # location name \n
                "obs_date" : datetime.datetime, # observation date \n
                "latitude" : str,               # latitude (positive north, negative south) \n
                "longitude" : str,              # longitude (positive east, negative west) \n
                "version_num : float,           # software version number (major rev.minor rev) \n
                "hdr_lines" : list,             # List of strings with the rest of the header lines from the data products files \n
                "hmax_n" : float,               # Assumed height of HMAX, in kms, in the north direction \n
                "hmax_s" : float,               # Assumed height of HMAX, in kms, in the south direction \n
                "hmax_e" : float,               # Assumed height of HMAX, in kms, in the east direction \n
                "hmax_w" : float,               # Assumed height of HMAX, in kms, in the west direction \n
                "emission_layer_n" : float,     # Assumed height of the emission layer, in kms, in the north direction \n
                "emission_layer_s" : float,     # Assumed height of the emission layer, in kms, in the south direction \n
                "emission_layer_e" : float,     # Assumed height of the emission layer, in kms, in the east direction \n
                "emission_layer_w" : float      # Assumed height of the emission layer, in kms, in the west direction \n
            } \n

        :Type Description for fpi_winds["meridional"]: 

        merid_winds : dict[str, numpy.ndarray] \n
            dict of { \n
                "imgno"  : numpy.ndarray of numpy.int32, # image sequence number \n
                "ut1"    :  numpy.ndarray of numpy.float32, # acquisition start time, in number of hours since start date \n
                "ut2"    :  numpy.ndarray of numpy.float32, # acquisition end time, in number of hours since start date \n
                "ut_mid" :  numpy.ndarray of numpy.float32, # timestamp at the middle of acquisition, in number of hours since start date \n
                "lookdir" :  numpy.ndarray of numpy.str\_, # Look direction. "North" or "South" \n
                "los" :  numpy.ndarray of numpy.float32, # Line of sight wind measurement in m/s \n
                "los_err" :  numpy.ndarray of numpy.float32, # Line of sight wind error estimate in m/s \n
                "ilos" :  numpy.ndarray of numpy.float32, # Interpolated Line of sight wind measurement in the opposite look direction, in m/s \n
                "ilos_err" :  numpy.ndarray of numpy.float32, # Line of sight wind error estimate of the interpolated wind measurement, in m/s \n
                "wind" :  numpy.ndarray of numpy.float32, # meridional wind measurement, in m/s \n
                "wind_err" :  numpy.ndarray of numpy.float32, # Meridional wind error estimate, in m/s \n
                "gradient" :  numpy.ndarray of numpy.float32, # Wind gradient, m/s per 500 kms  \n
                "gradient_err" :  numpy.ndarray of numpy.float32, # Wind gradient error estimate, in m/s per 500 kms \n
                "wind_desc" :  numpy.ndarray of numpy.str\_, # Description of the wind - Empty string, "converging", "diverging"  \n
                "qcode" :  numpy.ndarray of numpy.float32, # Data quality code.  code=0 trustworthy;  code=1 be suspicious;  code=2 be dubious \n
            } \n

        :Type Description for fpi_winds["zonal"]: 

        zonal_winds : dict[str, numpy.ndarray] \n
            dict of { \n
                "imgno"  : numpy.ndarray of numpy.int32, # image sequence number \n
                "ut1"    :  numpy.ndarray of numpy.float32, # acquisition start time, in number of hours since start date \n
                "ut2"    :  numpy.ndarray of numpy.float32, # acquisition end time, in number of hours since start date \n
                "ut_mid" :  numpy.ndarray of numpy.float32, # timestamp at the middle of acquisition, in number of hours since start date \n
                "lookdir" :  numpy.ndarray of numpy.str\_, # Look direction. "East" or "West" \n
                "los" :  numpy.ndarray of numpy.float32, # Line of sight wind measurement in m/s \n
                "los_err" :  numpy.ndarray of numpy.float32, # Line of sight wind error estimate in m/s \n
                "ilos" :  numpy.ndarray of numpy.float32, # Interpolated Line of sight wind measurement in the opposite look direction, in m/s \n
                "ilos_err" :  numpy.ndarray of numpy.float32, # Line of sight wind error estimate of the interpolated wind measurement, in m/s \n
                "wind" :  numpy.ndarray of numpy.float32, # Zonal wind measurement, in m/s \n
                "wind_err" :  numpy.ndarray of numpy.float32, # Zonal wind error estimate, in m/s \n
                "gradient" :  numpy.ndarray of numpy.float32, # Wind gradient, m/s per 500 kms  \n
                "gradient_err" :  numpy.ndarray of numpy.float32, # Wind gradient error estimate, in m/s per 500 kms \n
                "wind_desc" :  numpy.ndarray of numpy.str\_, # Description of the wind - Empty string, "converging", "diverging"  \n
                "qcode" :  numpy.ndarray of numpy.float32, # Data quality code.  code=0 trustworthy;  code=1 be suspicious;  code=2 be dubious \n
            } \n

        :Type Description for fpi_winds["vertical"]: 

        vert_winds : dict[str, numpy.ndarray] \n
            dict of { \n
                "imgno"  : numpy.ndarray of numpy.int32, # image sequence number \n
                "ut1"    :  numpy.ndarray of numpy.float32, # acquisition start time, in number of hours since start date \n
                "ut2"    :  numpy.ndarray of numpy.float32, # acquisition end time, in number of hours since start date \n
                "ut_mid" :  numpy.ndarray of numpy.float32, # timestamp at the middle of acquisition, in number of hours since start date \n
                "vert" :  numpy.ndarray of numpy.float32, # Relative vertical wind measurement, in m/s \n
                "vert_err" :  numpy.ndarray of numpy.float32, # Relative vertical wind error estimate, in m/s \n
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

    def winds_data_iterator():
        with open(winds_datfile, "r") as f:
            lines = f.readlines()
        for line in lines:
            # skip lines with just whitespace
            if line.isspace(): 
                continue
            line_stripped = line.strip()
            yield line_stripped

    def read_winds_header_details():
        """
            collect the header lines, which are the first few lines until the line with 
            the "SS-Analyze" string
        """
        winds_hdr_lines = list()
        for line in winds_datalines :
            winds_hdr_lines.append(line)
            if ('SS-Analyze' in line) :
                break
        
        # Get the name of the experiment (Redline, Greenline)
        expt = ''
        if( "Red".casefold() in (winds_hdr_lines[0]).casefold() ):
            loc_name_end_idx = (winds_hdr_lines[0].casefold()).find("Red".casefold()) - 1
            expt = "RedLine"
        if( "Green".casefold() in (winds_hdr_lines[0]).casefold() ):
            loc_name_end_idx = (winds_hdr_lines[0].casefold()).find("Green".casefold()) - 1
            expt = "GreenLine"

        # Get the location name (which is the entire string in line 0 preceding the experiment label)
        location_name = winds_hdr_lines[0][0:loc_name_end_idx]

        # Get the start date of the observation. Since the year is denoted by two digits, add 2000
        obs_date_yy = int(winds_hdr_lines[2][2:4])
        obs_date_yy += 2000
        obs_date_mon = int(winds_hdr_lines[2][4:6])
        obs_date_day = int(winds_hdr_lines[2][6:8])
        obs_date = datetime.datetime(obs_date_yy, obs_date_mon, obs_date_day)

        # get the version number
        versionNumberStr = re.split(' ', winds_hdr_lines[-1])[1]
        versionNumber = read_float(versionNumberStr[1:])

        latitude = float('NaN')
        longitude = float('NaN')
        for hdr_line in winds_hdr_lines:
            if ("latitude".casefold() in hdr_line.casefold()):
                # split the header line with lat and lon by delimiters, then remove 
                # empty strings, and then read the lat and lon from the list entities
                lat_lon_list = list(filter(None, re.split('[ \,]', hdr_line)))
                latitude = lat_lon_list[2]
                longitude = lat_lon_list[4]
        winds_hdr = {"expt" : expt,
            "location_name" :location_name,
            "obs_date" : obs_date,
            "latitude" : latitude,
            "longitude" : longitude,
            "version_num" : versionNumber,
            "hdr_lines" : winds_hdr_lines}

        return winds_hdr

    def read_winds_cardinal_summary():
        try:
            line = next(winds_datalines)
            # tokenize the line using spaces and the "=" character
            segments = re.split('[ =]+', line)
            n_items = int(segments[0])
            lookdir = segments[1]
            hmax = read_float(segments[5])
            emission_layer = read_float(segments[8])
        except :
            print("Unexpected error:", sys.exc_info()[0])
            return (False, 0, 0, 0)
        else :
            return (True, n_items, lookdir, hmax, emission_layer)

    def read_vert_winds_summary():
        try:
            line = next(winds_datalines)
            # tokenize the line using spaces 
            segments = re.split(' +', line)
            n_items = int(segments[0])
        except :
            return (False, 0)
        else :
            return (True, n_items)
    """
    read_winds_cardinal_detail reads the horizontal (cosine-component) of los winds 
    in each of the 4 cardinal directions, and report meriodional and zonal winds
    """
    def read_winds_cardinal_detail():
        # Read the first line, which is the summary info for the winds in each direction
        # Among other details, it contains the number of wind vectors measured in this 
        # direction.
        # This line also has the assumed hmax and emission layer.
        (status, nvectors, lookdir, hmax, emission_layer) = read_winds_cardinal_summary()
        """
        Skip the next couple of lines. The first line has the column names, and the 
        code will generate column names that correspond to the ones present in the .dat file.
        The second line has the units. skip this because the units are fixed for the columns.
        """
        skip_line = next(winds_datalines)
        skip_line = next(winds_datalines)
        # allocate structured array for each column in the table with winds and errors
        wind_data = np.zeros(
            nvectors,
            dtype={
                'names':
                ['imgno', 'ut1', 'ut2', 'ut_mid', 'lookdir', 'los', 'los_err', 'ilos', 'ilos_err', 'wind', 'wind_err', 'gradient', 'gradient_err', 'wind_desc', 'qcode'],
                'formats':['i4', 'f4', 'f4', 'f4', 'U10', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'U10', 'i4']})
 
        #  assemble wind vector details
        for j in range(0, nvectors) :
            wind_record = next(winds_datalines)
            wind_rec_cols = re.split(' +', wind_record)
            imgNo = read_float(wind_rec_cols[0])
            UT_1 = read_float(wind_rec_cols[1])
            UT_2 = read_float(wind_rec_cols[2])
            UT_mid = read_float(wind_rec_cols[3])
            los = read_float(wind_rec_cols[4])
            i_los = read_float(wind_rec_cols[5])
            wind = read_float(wind_rec_cols[6])
            gradient = read_float(wind_rec_cols[7])
            wind_desc = ' '.join(wind_rec_cols[8:-1])
            qcode = read_float(wind_rec_cols[-1])
            wind_err_record = next(winds_datalines)
            wind_err_cols =re.split(' +', wind_err_record)
            err_los = read_float(wind_err_cols[1])
            err_ilos = read_float(wind_err_cols[2])
            err_wind = read_float(wind_err_cols[3])
            err_gradient = read_float(wind_err_cols[4])
            # now populate the arrays with the values just read
            wind_data["lookdir"] = lookdir
            wind_data[j]['imgno'] = imgNo
            wind_data[j]['ut1'] = UT_1
            wind_data[j]['ut2'] = UT_2
            wind_data[j]['ut_mid'] = UT_mid
            wind_data[j]['los'] = los
            wind_data[j]['los_err'] = err_los
            wind_data[j]['ilos'] = i_los
            wind_data[j]['ilos_err'] = err_ilos
            wind_data[j]['wind'] = wind
            wind_data[j]['wind_err'] = err_wind
            wind_data[j]['gradient'] = gradient
            wind_data[j]['gradient_err'] = err_gradient
            wind_data[j]['wind_desc'] = wind_desc
            wind_data[j]['qcode'] = qcode
        return (hmax, emission_layer, wind_data)
    def read_winds_vertwinds_detail():
        (status, n_vert_winds) = read_vert_winds_summary()
        skip_line = next(winds_datalines)
        skip_line = next(winds_datalines)
        skip_line = next(winds_datalines)
        vert_wind_data = np.zeros(n_vert_winds, dtype={'names':('imgno', 'ut1', 'ut2', 'ut_mid', 'vert', 'vert_err', 'qcode'),
                'formats':('i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'i4')})
        for j in range(0, n_vert_winds) :
            wind_record = next(winds_datalines)
            # if it contains the string "order" skip it because we are 
            # ingesting only the derived relative vertical winds from all orders,
            # and not ingesting vertical wind information for each order (fringe)
            while( "order" in wind_record): 
                wind_record = next(winds_datalines)
            wind_rec_cols = re.split(' +', wind_record)
            imgNo = read_float(wind_rec_cols[0])
            UT_1 = read_float(wind_rec_cols[1])
            UT_2 = read_float(wind_rec_cols[2])
            UT_mid = read_float(wind_rec_cols[3])
            bin = read_float(wind_rec_cols[4])
            ebin = read_float(wind_rec_cols[5])
            vert = read_float(wind_rec_cols[6])
            e_vert = read_float(wind_rec_cols[7])
            qcode = read_float(wind_rec_cols[-1])

            # now populate the arrays with the values just read
            vert_wind_data[j]['imgno'] = imgNo
            vert_wind_data[j]['ut1'] = UT_1
            vert_wind_data[j]['ut2'] = UT_2
            vert_wind_data[j]['imgno'] = imgNo
            vert_wind_data[j]['ut_mid'] = UT_mid
            vert_wind_data[j]['vert'] = vert
            vert_wind_data[j]['vert_err'] = e_vert
            vert_wind_data[j]['qcode'] = qcode
        return (vert_wind_data)
                       
    winds_datalines = winds_data_iterator()
    winds_hdr = read_winds_header_details()
    (hmax_n, e_layer_n, wind_data_n) = read_winds_cardinal_detail()
    (hmax_s, e_layer_s, wind_data_s) = read_winds_cardinal_detail()
    (hmax_e, e_layer_e, wind_data_e) = read_winds_cardinal_detail()
    (hmax_w, e_layer_w, wind_data_w) = read_winds_cardinal_detail()
    wind_data_v = read_winds_vertwinds_detail()

    winds_hdr["hmax_n"] = hmax_n
    winds_hdr["emission_layer_n"] = e_layer_n
    winds_hdr["hmax_s"] = hmax_s
    winds_hdr["emission_layer_s"] = e_layer_s
    winds_hdr["hmax_e"] = hmax_e
    winds_hdr["emission_layer_e"] = e_layer_e
    winds_hdr["hmax_w"] = hmax_w
    winds_hdr["emission_layer_w"] = e_layer_w

    """
    Merge the north and south winds data to return meridional wind info
    """  
    merid_winds = np.concatenate((wind_data_n, wind_data_s), axis=None)
    merid_winds_sorted = np.sort(merid_winds, order="ut_mid")
    # convert the meridional winds np array  to a dictionary
    merid_winds_dict = dict()
    for col_name in merid_winds_sorted.dtype.names:
        merid_winds_dict[col_name] = merid_winds_sorted[col_name]
    """"
    Merge the east and west winds data to return zonal wind info
    """  
    zonal_winds = np.concatenate( (wind_data_e, wind_data_w), axis=None)
    zonal_winds_sorted = np.sort(zonal_winds, order="ut_mid")
    # convert the zonal winds np array  to a dictionary
    zonal_winds_dict = dict()
    for col_name in zonal_winds_sorted.dtype.names:
        zonal_winds_dict[col_name] = zonal_winds_sorted[col_name]

    # convert the vertical winds np array  to a dictionary
    vert_winds_dict = dict()
    for col_name in wind_data_v.dtype.names:
        vert_winds_dict[col_name] = wind_data_v[col_name]

    winds_data = {
        "header" : winds_hdr,
        "meridional" : merid_winds_dict,
        "zonal" : zonal_winds_dict,
        "vertical" : vert_winds_dict}

    return (winds_data)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "winds_datfile",type=str, help="The full path of the *winds.dat file to be parsed."
    )
    args = argument_parser.parse_args()

    fpi_winds = fpi_winds_filereader( args.winds_datfile)

    print ("Winds header data:")
    print (fpi_winds["header"])
    print ("meridional winds:")
    print (fpi_winds["meridional"])
    print ("Zonal winds:")
    print (fpi_winds["zonal"])
    print ("Relative vertical winds:")
    print (fpi_winds["vertical"])
