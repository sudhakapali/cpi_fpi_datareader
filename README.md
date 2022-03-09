# CPI_FPI_dataproduct_reader

Python file readers for the FPI winds and temperature data product files, which are produced by the FPI data analysis software.
<li> docs : Documentation of the data format of the FPI winds data product files (*winds.dat) and temperature data product files (*temps.dat)
<li>read_fpi_temps.py : Python program to read CPI FPI temperature data product files
<li>read_fpi_winds.py : Python program to read CPI FPI winds data product files
<li>data : Subfolder with sample winds and temperature data products which are used as input to the following test programs.
<li>test_read_fpi_temps.py : Example and test program demonstrating usage of the temperature data reader. This program plots temperature vs. UT for each observation direction.
<li>test_read_fpi_winds.py : Example and test program demonstrating usage of the winds data reader. This program plots Line of Sight Wind Velocity vs. UT for each observation direction.
<li> output : subfolder with example plots produced by test_read_fpi_temps.py and test_read_fpi_winds.py
