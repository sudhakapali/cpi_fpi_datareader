import glob
import os
import matplotlib.pyplot as plot
import numpy as np
from read_fpi_temps import fpi_temps_filereader

if __name__ == "__main__":
    datadir = "."+os.sep + "data" + os.sep + "*_temps.dat"
    plotdir = "."+ os.sep + "output" + os.sep
    temps_data_files = glob.glob(datadir) 
    for temps_file in temps_data_files:
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
        # gather the info needed to plot these measurements
        tmid_n = temps_data["ut_mid"][north_pos]
        temp_n = temps_data["temp"][north_pos]
        e_temp_n = temps_data["e_temp"][north_pos]
        e_time_n = temps_data["e_time"][north_pos]
        tmid_s = temps_data["ut_mid"][south_pos]
        temp_s = temps_data["temp"][south_pos]
        e_temp_s = temps_data["e_temp"][south_pos]
        e_time_s = temps_data["e_time"][south_pos]
        tmid_e = temps_data["ut_mid"][east_pos]
        temp_e = temps_data["temp"][east_pos]
        e_temp_e = temps_data["e_temp"][east_pos]
        e_time_e = temps_data["e_time"][east_pos]
        tmid_w = temps_data["ut_mid"][west_pos]
        temp_w = temps_data["temp"][west_pos]
        e_temp_w = temps_data["e_temp"][west_pos]
        e_time_w = temps_data["e_time"][west_pos]
        tmid_z = temps_data["ut_mid"][zenith_pos]
        temp_z = temps_data["temp"][zenith_pos]
        e_temp_z = temps_data["e_temp"][zenith_pos]
        e_time_z = temps_data["e_time"][zenith_pos]
        # get the header variables that we want to display
        obs_date_str = temps_hdr["obs_date"].strftime("%m/%d/%Y")
        expt_name = temps_hdr["expt"] 
        loc_name = str(temps_hdr["location_name"])
        lat_str = str(temps_hdr["latitude"])
        lon_str = str(temps_hdr["longitude"])
        version_str = str(temps_hdr["version_num"])
        #----------------------------------------------------------------
        #plot it
        fig, ax = plot.subplots(1, 2, sharey='row')
        fig.set_size_inches(8, 5)
        plot.subplots_adjust(wspace=0, hspace=0)
        ax[0].errorbar (tmid_n, temp_n, xerr=e_time_n, yerr=e_temp_n, 
            fmt='*r', markerfacecolor='none', label='North')
        ax[0].errorbar (tmid_s, temp_s, xerr=e_time_s, yerr=e_temp_s, 
            fmt='sb', markerfacecolor='none', label='South')
        ax[1].errorbar (tmid_e, temp_e, xerr=e_time_e, yerr=e_temp_e, 
            fmt='*r', markerfacecolor='none', label='East')
        ax[1].errorbar (tmid_w, temp_w, xerr=e_time_w, yerr=e_temp_w, 
            fmt='sb', markerfacecolor='none', label='West')
        ax[1].errorbar (tmid_z, temp_z, xerr=e_time_z, yerr=e_temp_z, 
            fmt='*k', markerfacecolor='none', label='Zenith')
        ax[0].set(xlabel= "time (UT) hrs", ylabel = "Temperature (K)")
        ax[1].set(xlabel= "time (UT) hrs")
        plot.ylim([0,2000])
        titleString =  obs_date_str+ " " + expt_name + " " + loc_name + \
            "  (lat, lon):  (" + lat_str + ", "  + lon_str  + ")"
        fig.suptitle(titleString)
        ax[1].legend()
        ax[0].legend()
        plot.gcf().text(0.9, 0.02, "version " + version_str, fontsize=7)
        png_filebasename = os.path.basename(temps_file).split('.')[0] + ".png"
        pngfile = plotdir + png_filebasename
        fig.savefig(pngfile)
