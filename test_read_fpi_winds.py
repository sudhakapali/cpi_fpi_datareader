import glob
import os
import numpy as np
import matplotlib.pyplot as plot
from read_fpi_winds import fpi_winds_filereader

"""
    Test program to read the FPI Thermospheric Winds data products file (*winds.dat)
    This program reads the winds data products files in the "data" sub-folder,
    produces a line-of-sight plot for each file that is read, and save the plot
    "output" folder of the project to a file with the same basename as the input file
    and a "_LosVsUT.png" extension.
    For example, the output plot created for "mh220301_winds.dat" is "mh220301_winds_losVsUT.png"
"""
if __name__ == "__main__":
    # datadir is the directory where the *_winds.dat files are located.
    datadir = "."+os.sep + "data" + os.sep + "*_winds.dat"
    plotdir = "."+ os.sep + "output" + os.sep
    winds_data_files = glob.glob(datadir) 

    for winds_file in winds_data_files:
        # read in the winds data products
        fpi_winds = fpi_winds_filereader(winds_file)
        winds_hdr = fpi_winds["header"]
        merid_winds = fpi_winds["meridional"]
        zonal_winds = fpi_winds["zonal"]
        vert_winds = fpi_winds["vertical"]

        # Get the indices corresponding to the zenith and 4 directions
        north_idx = np.where ( 'North'.lower() == np.char.lower(merid_winds["lookdir"]) )
        south_idx = np.where( 'South'.lower() == np.char.lower(merid_winds["lookdir"]) )
        east_idx = np.where ( 'East'.lower() == np.char.lower(zonal_winds["lookdir"]) )
        west_idx = np.where( 'West'.lower() == np.char.lower(zonal_winds["lookdir"]) )

        tmid_n = merid_winds["ut_mid"][north_idx]
        tmid_s = merid_winds["ut_mid"][south_idx]
        tmid_e = zonal_winds["ut_mid"][east_idx]
        tmid_w = zonal_winds["ut_mid"][west_idx]

        los_n = merid_winds["los"][north_idx]
        los_s = merid_winds["los"][south_idx]
        los_e = zonal_winds["los"][east_idx]
        los_w = zonal_winds["los"][west_idx]

        e_time_n = (merid_winds["ut2"][north_idx] - merid_winds["ut1"][north_idx])/2.0
        e_time_s = (merid_winds["ut2"][south_idx] - merid_winds["ut1"][south_idx])/2.0
        e_time_e = (zonal_winds["ut2"][east_idx] - zonal_winds["ut1"][east_idx])/2.0
        e_time_w = (zonal_winds["ut2"][west_idx] - zonal_winds["ut1"][west_idx])/2.0

        e_los_n = merid_winds["los_err"][north_idx]
        e_los_s = merid_winds["los_err"][south_idx]
        e_los_e = zonal_winds["los_err"][east_idx]
        e_los_w = zonal_winds["los_err"][west_idx]
        
        # get the header variables that we want to display
        obs_date_str = winds_hdr["obs_date"].strftime("%m/%d/%Y")
        expt_name = winds_hdr["expt"] 
        loc_name = str(winds_hdr["location_name"])
        lat_str = str(winds_hdr["latitude"])
        lon_str = str(winds_hdr["longitude"])
        version_str = str(winds_hdr["version_num"])
        #----------------------------------------------------------------
        #plot it
        fig, ax = plot.subplots(1, 2, sharey='row')
        fig.set_size_inches(8, 5)
        plot.subplots_adjust(wspace=0, hspace=0)
        ax[0].errorbar (tmid_n, los_n, xerr=e_time_n, yerr=e_los_n, 
            fmt='*r', markerfacecolor='none', label='North')
        ax[0].errorbar (tmid_s, los_s, xerr=e_time_s, yerr=e_los_s, 
            fmt='sb', markerfacecolor='none', label='South')
        ax[1].errorbar (tmid_e, los_e, xerr=e_time_e, yerr=e_los_e, 
            fmt='*r', markerfacecolor='none', label='East')
        ax[1].errorbar (tmid_w, los_w, xerr=e_time_w, yerr=e_los_w, 
            fmt='sb', markerfacecolor='none', label='West')
        ax[0].set(xlabel= "time (UT) hrs", ylabel = "Line of Sight Velocity (m/s)")
        ax[1].set(xlabel= "time (UT) hrs")

        # set the range for y-axis
        plot.ylim([-300, 300])
        xlim_min, xlim_max = ax[0].get_xlim()
        # plot a horizontal black line of at 0 m/s for reference
        ax[0].plot((xlim_min, xlim_max), (0, 0), 'k:')
        ax[1].plot((xlim_min, xlim_max), (0, 0), 'k:')

        titleString =  loc_name +   "  (lat, lon):  (" + lat_str + ", "  + lon_str  + ")" + \
             "\n" + obs_date_str + " " + expt_name 
           
        fig.suptitle(titleString)
        ax[1].legend()
        ax[0].legend()
        plot.gcf().text(0.9, 0.02, "version " + version_str, fontsize=7)
        png_filebasename = os.path.basename(winds_file).split('.')[0] + "_losVsUT.png"
        pngfile = plotdir + png_filebasename
        fig.savefig(pngfile)
