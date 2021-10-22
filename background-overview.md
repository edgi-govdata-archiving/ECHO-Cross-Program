## Environmental Data Governance Initiative (EDGI)
## Environmental Enforcement Watch (EEW) - a project of EDGI

### What is this about?

We start with EPA data on permits, inspections, violations, enforcement actions.  This data is collected and made public in an EPA system called the Enforcement Compliance History Online (ECHO).  In the Data Services tab of this site the National Data Sets contain numerous CSV files of data, dating back to the 1980s in many cases.  Each data set has its own set of fields, whose meanings are defined in separate pages.

Working with database experts at Stony Brook University in New York, EEW defined database schema to allow us to load the CSV files into a PostgreSQL database to facilitate searching and analyzing the data.  An automated process for this was developed for many of the key data sets within ECHO.  The database is read-only.

With this data available, EEW was able to begin writing Jupyter Notebooks to analyze and visualize the ECHO data and begin reporting our findings.  We have used these notebooks in several online events with local and national environmental groups to look into questions about specific regions and EPA programs.  We are still relatively early in this process.

Python Jupyter notebooks are flexible and transparent.  They allow us to quickly ask new questions about the data, and they let anyone see how the results have been derived. 

### Code Organization

We have been trying to balance the transparency of having code in the cells of a Jupyter notebook for transparency with keeping the notebook easy for non-coders to read and run.  As we’ve been developing new notebooks we also find that there is much code that can be re-used.  We have moved much of the common code into a separate Github repository called ECHO_modules.  

### ECHO_modules

This repository of Python code is imported into most of our Jupyter notebooks. The primary files of interest in this repository are:

**get_data.py** - This contains a get_echo_data() function that is the primary way to query the PostgreSQL database.

**DataSet.py** - This is a Python class that represents an EPA ECHO data set--a specific EPA program such as the Clean Water Act (CWA), Clean Air Act (CAA), Resource Conservation and Recovery Act (RCRA - hazardous waste), etc., a specific type of data on the program such as violations, inspections, enforcements, and other fields.  It contains methods for working retrieving the data from the database, storing the data, and returning it on demand, using the DataSetResult class.
**DataSetResult.py** - This class gets and stores data for a specific query of the DataSet.

**utilities.py** - A number of functions in this file are used in the notebooks to perform common functions and keep the notebook code cells less bulky.

**make_data_sets.py** - The make_data_sets() function can be used to create a number of DataSet objects based on a standard definition of fields.

**data_set_presets.py** - This contains the standard definition of the most commonly used DataSets, such as CWA_violations, CAA_inspections, etc.

**geographies.py** - Region types (states, zip codes, congressional districts, etc.) and state abbreviations used in notebook dropdowns.
