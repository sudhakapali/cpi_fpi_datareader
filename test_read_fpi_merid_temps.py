import glob
import os
import numpy as np
import matplotlib.pyplot as plot
from read_fpi_temps import fpi_temps_filereader

def get_merid_temps(temps_file):
    """
    :Synopsis: 

        Function get_merid_temps is an example function that 

        a) reads the FPI thermospheric temperature data products file (*temps.dat), and 
        b) merges the temperature and time values in the North and South directions.
           The output values are sorted in time.

    :Args:
    
        temps_datfile (str): The full pathname of the temperature data products file to be read
 
    :returns: 
    
    * tmid_m : The ut_mid of the meridional measurements,
    * e_time_m :  The error estimate in ut_mid of the meridional measurements,
    * temp_m : The temperature measurement of meridional measurements
    * e_temp_m : The error in temperature of the meridional measurements

    :rtype: 

    * tmid_m : numpy.ndarray
    * e_time_m :  numpy.ndarray
    * temp_m : numpy.ndarray
    * e_temp_m : numpy.ndarray

    """
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
    return (tmid_m, e_time_m, temp_m, e_temp_m)

if __name__ == "__main__":
    # datadir is the directory where the *_temps.dat files are located.
    datadir = "."+os.sep + "data" + os.sep + "*_temps.dat"
    plotdir = "."+ os.sep + "output" + os.sep
    temps_data_files = glob.glob(datadir) 
    for temps_file in temps_data_files:
        tmid_m, e_time_m, temp_m, e_temp_m = \
            get_merid_temps(temps_file)
        print (tmid_m)
        print (temp_m)