#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:05:40 2020

@author: ericnost

This script collates pre-recorded data pulled from EEW's AllPrograms Jupyter Notebook
"""
# Import code libraries
import os
import csv
import numpy as np

# Initial variable definitions

inf = {2002: 1.421,
 2003: 1.389,
 2004: 1.353,
 2005: 1.309,
 2006: 1.268,
 2007: 1.233,
 2008: 1.187,
 2009: 1.192,
 2010: 1.172,
 2011: 1.137,
 2012: 1.114,
 2013: 1.097,
 2014: 1.08,
 2015: 1.079,
 2016: 1.065,
 2017: 1.043,
 2018: 1.018,
 2019: 1.0,
 2001: 1.444} # Inflation adjusters for 2019, from the US BLS

# Final stores the results as we go through each congressional district and state's data
final = {"header": ["District", "CWA_CHG", "ENF_CHG", "PEN_CHG", "CAA_PCT", "CWA_PCT", "RCRA_PCT", "CWA_IN_CHG", "CAA_IN_CHG", "RCRA_IN_CHG", "INSP_CHG", "CWA_TOTAL", "CWA_FAC"]} #Dictionary to de-duplicate values

# Go through each folder and pull out files
directory = '' # Set to your own copy of the data files from https://github.com/edgi-govdata-archiving/CD-report/tree/master/CD_Dirs
district = ""

for folder, dirs, files in os.walk(directory):
    print(folder[48:]) # this is directory-dependent! Be sure to change for your own. It strips the folder path in order to pull out the state/district name
    thisDistrict = folder[48:]
    if len(thisDistrict) == 2:
        district = thisDistrict[:2]
    elif len(thisDistrict) == 3:
        district = thisDistrict[:2]+"0"+thisDistrict[-1]
    elif (len(thisDistrict) == 4):
        district = thisDistrict
    
    pre_cwa = [] # 01-16 count of CWA violations
    trump_cwa = [] # 17-19 count of CWA violations
    cwa_pct_chg="x" # percent change in average number of CWA violations 01-16 vs 17-19

    caa_pct = "x" # percent of CWA facilities that are "recurring violations" = 3+ quarters out of the past 12/13 in non-compliance
    cwa_pct = "x" # percent of CAA facilities that are "recurring violations" = 3+ quarters out of the past 12/13 in non-compliance
    rcra_pct = "x" # percent of RCRA facilities that are "recurring violations" = 3+ quarters out of the past 12/13 in non-compliance
    
    pre_enf = [] # 01-16 count of enforcement actions
    trump_enf = [] # 17-19 count of enforcement actions 
    pre_pen=[] # 01-16 sum of penalties
    trump_pen=[] # 01-16 count of enforcement actions
    pen_pct_chg="x" # percent change in average penalties 01-16 vs 17-19
    enf_pct_chg = "x" # percent change in average enforcement actions 01-16 vs 17-19
    

    pre_insp_caa = [] # 01-16 count of CAA inspections
    trump_insp_caa = [] # 17-19 count of CAA inspections
    pre_insp_cwa = [] # 01-16 count of CWA inspections
    trump_insp_cwa = [] # 17-19 count of CWA inspections
    pre_insp_rcra = [] # 01-16 count of RCRA inspections
    trump_insp_rcra = [] # 17-19 count of RCRA inspections
    pre_insp=[] # 01-16 count of all inspections
    trump_insp=[] # 17-19 count of all inspections
    
    insp_pct_chg="x" # percent change in average inspections all programs 01-16 vs 17-19
    caa_insp_pct_chg="x" # percent change in average CAA inspections 01-16 vs 17-19
    cwa_insp_pct_chg="x" # percent change in average CWA inspections 01-16 vs 17-19
    rcra_insp_pct_chg="x" # percent change in average RCRA inspections 01-16 vs 17-19
    
    fac="x" # count of CWA facilities
    cwa_total="x" # total number of CWA violations in 2019
    
    for file in files:
        path = os.path.join(folder, file)
        
        # CWA violations
        if "violations_CWA_pg3" in file: 
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                cwadata = list(read)
            csvfile.close()
            for row in cwadata[1:len(cwadata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_cwa.append(int(row[1]))
                elif (yr >=2017) & (yr < 2020):
                    trump_cwa.append(int(row[1]))
                    if yr == 2019:
                        cwa_total = int(row[1]) # Get the 2019 CWA violations count specifically
            cwa_pct_chg = 100 * ((np.mean(trump_cwa) - np.mean(pre_cwa)) / np.mean(pre_cwa)) # percent change in average number of CWA violations 01-16 vs 17-19
        
        # Get CWA facilities count            
        elif "active-facilities_All" in file:
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                facdata = list(read)
            csvfile.close()
            for row in facdata[1:len(facdata)]: #1 to not do header
                print(row)
                if row[0] == "CWA":
                    fac = int(row[1]) # Count of CWA facilities
                    
        # CWA inspections
        elif "inspections_CWA_pg6" in file: 
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                cwainspdata = list(read)
            csvfile.close()
            for row in cwainspdata[1:len(cwainspdata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_insp_cwa.append(int(row[1]))
                elif (yr >=2017) & (yr < 2020):
                    trump_insp_cwa.append(int(row[1]))
            cwa_insp_pct_chg = 100 * ((np.mean(trump_insp_cwa) - np.mean(pre_insp_cwa)) / np.mean(pre_insp_cwa)) # percent change in average inspections under CWA 01-16 vs 17-19
        
        # CAA inspections    
        elif "inspections_CAA_pg5" in file: 
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                caainspdata = list(read)
            csvfile.close()
            for row in caainspdata[1:len(caainspdata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_insp_caa.append(int(row[1]))
                elif (yr >=2017) & (yr < 2020):
                    trump_insp_caa.append(int(row[1]))
            caa_insp_pct_chg = 100 * ((np.mean(trump_insp_caa) - np.mean(pre_insp_caa)) / np.mean(pre_insp_caa)) # percent change in average inspections under CAA 01-16 vs 17-19
         
        # RCRA inspections    
        elif "inspections_RCRA_pg7" in file: 
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                rcrainspdata = list(read)
            csvfile.close()
            for row in rcrainspdata[1:len(rcrainspdata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_insp_rcra.append(int(row[1]))
                elif (yr >=2017) & (yr < 2020):
                    trump_insp_rcra.append(int(row[1]))
            rcra_insp_pct_chg = 100 * ((np.mean(trump_insp_rcra) - np.mean(pre_insp_rcra)) / np.mean(pre_insp_rcra)) # percent change in average inspections under RCRA 01-16 vs 17-19
        
        # Inspections per year for all three programs
        elif "inspections_All_pg3" in file: 
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                inspdata = list(read)
            csvfile.close()
            for row in inspdata[1:len(inspdata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_insp.append(int(row[1]))
                elif (yr >=2017) & (yr < 2020):
                    trump_insp.append(int(row[1]))
            insp_pct_chg = 100 * ((np.mean(trump_insp) - np.mean(pre_insp)) / np.mean(pre_insp)) # percent change in average inspections 01-16 vs 17-19

        # Enforcement actions and penalties for all three programs
        elif "enforcements_All_pg3" in file:
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                enfdata = list(read)
            csvfile.close()
            for row in enfdata[1:len(enfdata)]: #1 to not do header
                yr = int(row[0])
                if yr < 2017:
                    pre_enf.append(float(row[2]))
                    pre_pen.append(float(row[1])*inf[yr])
                elif (yr >=2017) & (yr < 2020):
                    trump_enf.append(float(row[2]))
                    trump_pen.append(float(row[1])*inf[yr])
            enf_pct_chg = 100 * ((np.mean(trump_enf) - np.mean(pre_enf)) / np.mean(pre_enf)) # percent change in average number of enforcements 01-16 vs 17-19
            pen_pct_chg = 100 * ((np.mean(trump_pen) - np.mean(pre_pen)) / np.mean(pre_pen)) # percent change in the average penalties 01-16 vs 17-19
            
        # Record the percent of recurring violators over the past 12/13 quarters
        elif "recurring-violations_All" in file:
            with open(path) as csvfile: 
                read = csv.reader(csvfile)
                violdata = list(read)
            csvfile.close()
            for row in violdata[1:len(violdata)]: #1 to not do header
                print(row)
                if row[0] == "CAA":
                    caa_pct = row[4]
                elif row[0] == "CWA":
                    cwa_pct = row[4]
                elif row[0] == "RCRA":
                    rcra_pct = row[4]
            
    print("Making final data for"+district)
    final[district] = [district, cwa_pct_chg, enf_pct_chg, pen_pct_chg, caa_pct, cwa_pct, rcra_pct, cwa_insp_pct_chg, caa_insp_pct_chg, rcra_insp_pct_chg, insp_pct_chg, cwa_total, fac]
    
output=list(final.values())
with open('echo_map_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in output:
        writer.writerow(row)
csvfile.close()