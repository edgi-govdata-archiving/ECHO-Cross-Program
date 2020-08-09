# Import libraries

import csv
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
from ECHO_modules.DataSet import get_data
from ECHO_modules.geographies import region_field, states

from IPython.display import display


# Set up some default parameters for graphing
from matplotlib import cycler
colour = "#00C2AB" # The default colour for the barcharts
colors = cycler('color',
                ['#4FBBA9', '#E56D13', '#D43A69',
                 '#25539f', '#88BB44', '#FFBBBB'])
plt.rc('axes', facecolor='#E6E6E6', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')
plt.rc('lines', linewidth=2)
font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 16}
plt.rc('font', **font)
plt.rc('legend', fancybox = True, framealpha=1, shadow=True, borderpad=1)


#####################
#  fix_county_names( in_counties )
#    
# ECHO_EXPORTER has counties listed both as ALAMEDA and ALAMEDA COUNTY, seemingly
# for every county.  We drop the 'COUNTY' so they only get listed once.
#
# Parameters:  in_counties -- list of county names
# Return: The new list of counties without duplicates
#
#####################

def fix_county_names( in_counties ):
    counties = []
    for county in in_counties:
        if (county.endswith( ' COUNTY' )):
            county = county[:-7]
        counties.append( county.strip() )
    counties = np.unique( counties )
    return counties


#####################
#  show_region_type_widget()
#    
# Create and return a dropdown list of types of regions.
#
# Return: The widget 
#
#####################

def show_region_type_widget():
    style = {'description_width': 'initial'}
    select_region_widget = widgets.Dropdown(
        options=region_field.keys(),
        style=style,
        value='County',
        description='Region of interest:',
        disabled=False
    )
    display( select_region_widget )
    return select_region_widget


#####################
#  show_state_widget()
#    
# Create and return a dropdown list of states
#
# Return: The widget 
#
#####################

def show_state_widget():
    dropdown_state=widgets.Dropdown(
        options=states,
        description='State:',
        disabled=False,
    )
    
    display( dropdown_state )
    return dropdown_state


#####################
# show_pick_region_widget( type, state_widget=None ):
#    
# Create and return a dropdown list of regions appropriate
# to the input parameters
#
# Parameters:
#    type -- The type of region
#    state_widget -- The widget in which a state may have been selected.
#
# Return: The widget or None 
#
#####################

def show_pick_region_widget( type, state_widget=None ):
    region_widget = None
    
    if ( type != 'Zip Code' ):
        if ( state_widget is None ):
            print( "You must first choose a state." )
            return
        my_state = state_widget.value
    
    if ( type == 'Zip Code' ):
        region_widget = widgets.IntText(
            value=98225,
            description='Zip Code:',
            disabled=False
        )
    elif ( type == 'County' ):
        df = pd.read_csv( 'ECHO_modules/state_counties.csv' )
        counties = df[df['FAC_STATE'] == my_state]['FAC_COUNTY']
        region_widget=widgets.Dropdown(
            options=fix_county_names( counties ),
            description='County:',
            disabled=False
        )
    elif ( type == 'Congressional District' ):
        df = pd.read_csv( 'ECHO_modules/state_cd.csv' )
        cds = df[df['FAC_STATE'] == my_state]['FAC_DERIVED_CD113']
        region_widget=widgets.Dropdown(
            options=cds.to_list(),
            description='District:',
            disabled=False
        )
    if ( region_widget is not None ):
        display( region_widget )
    return region_widget


#####################
# show_data_set_widget( data_sets ):
#    
# Create and return a dropdown list of data sets with appropriate
# flags set in the echo_data. 
#
# Parameters:
#    data_sets -- The Dictionary of data sets. Values are instances
#        of class DataSet.
#
# Return: The widget of data set choices
#
#####################

def show_data_set_widget( data_sets ):
    
    data_set_choices = list( data_sets.keys() )
    
    data_set_widget=widgets.Dropdown(
        options=list(data_set_choices),
        description='Data sets:',
        disabled=False,
    ) 
    display(data_set_widget)
    return data_set_widget


#####################
#  show_fac_widget( fac_series ):
#    
# Create and return a dropdown list of facilities from the Series
#
# Parameters:
#    fac_series -- A Series containing the facilities to be shown.
#        It may have duplicates
#
# Return: The widget of facility names
#
#####################

def show_fac_widget( fac_series ):
    fac_list = fac_series.dropna().unique()
    fac_list.sort()
    style = {'description_width': 'initial'}
    widget=widgets.Dropdown(
        options=fac_list,
        style=style,
        layout=Layout(width='70%'),
        description='Facility Name:',
        disabled=False,
    )
    display(widget)
    return widget


#####################
#  show_chart( program, region, data, state=None, fac_name=None ):
#    
# Display a chart based on the parameters.
#
# Parameters:
#    program -- A Dictionary entry with name and DataSet to be displayed
#    region -- The region, for the chart's title
#    state -- The state, for the chart's title
#    fac_name -- The name of the facility, for the chart's title
#
#####################

def show_chart( program, region, data, state=None, fac_name=None ):
    chart_title = program.name 
    if ( state is not None ):
        chart_title += ' - ' + state
    chart_title += ' - ' + str( region )
    if ( fac_name is not None ):
        chart_title += ' - ' + fac_name

    # Handle NPDES_QNCR_HISTORY because there are multiple counts we need to sum
    if (program.name == "Water Quarterly Violations"): 
        year = data["YEARQTR"].astype("str").str[0:4:1]
        data["YEARQTR"] = year
        data = data.drop(columns=['FAC_LAT', 'FAC_LONG']) # Remove lat/longs
        d = data.groupby(pd.to_datetime(data['YEARQTR'], format="%Y").dt.to_period("Y")).sum()
        d.index = d.index.strftime('%Y')
        d = d[ d.index > '2000' ]

        ax = d.plot(kind='bar', title = chart_title, figsize=(20, 10), fontsize=16)
        ax
    # These data sets use a FISCAL_YEAR field
    elif (program.name == "SDWA Public Water Systems" or program.name == "SDWA Violations" or
         program.name == "SDWA Serious Violators" or program.name == "SDWA Return to Compliance"):
        year = data["FISCAL_YEAR"].astype("str")
        data["FISCAL_YEAR"] = year
        d = data.groupby(pd.to_datetime(data['FISCAL_YEAR'], format="%Y").dt.to_period("Y"))[['PWS_NAME']].count()
        d.index = d.index.strftime('%Y')
        d = d[ d.index > '2000' ]

        ax = d.plot(kind='bar', title = chart_title, figsize=(20, 10), fontsize=16)
        ax        
    elif (program.name == "Combined Air Emissions" or program.name == "Greenhouse Gases" \
              or program.name == "Toxic Releases"):
        d = data.groupby( 'REPORTING_YEAR' )[['ANNUAL_EMISSION']].sum()
        ax = d.plot(kind='bar', title = chart_title, figsize=(20, 10), fontsize=16)
        ax.set_xlabel( 'Reporting Year' )
        ax.set_ylabel( 'Pounds of Emissions')
        ax        
    # All other programs
    else:
        try:
            d = data.groupby(pd.to_datetime(data[program.date_field], format=program.date_format))[[program.date_field]].count()
            d = d.resample("Y").sum()
            d.index = d.index.strftime('%Y')
            d = d[ d.index > '2000' ]

            if ( len(d) > 0 ):
                ax = d.plot(kind='bar', title = chart_title, figsize=(20, 10), legend=False, fontsize=16)
                ax
            else:
                print( "There is no data for this program and region after 2000." )

        except AttributeError:
            print("There's no data to chart for " + program.name + " !")


#####################
#  marker_text( row, is_echo ):
#    
# Create a string with information about the facility or program instance.
#
# Parameters:  
#    row -- The row of data associated with the marker.
#    is_echo -- If True, put some information with the marker to show the 
#        programs that track the facility.
#
# Return:  The text to put with the marker
#
#####################

def marker_text( row, is_echo ):
    text = ""
    if ( type( row['FAC_NAME'] == str )) :
        try:
            text = row["FAC_NAME"] + ' - '
        except TypeError:
            print( "A facility was found without name. ")
        if ( is_echo ):
##            if ( row['AIR_FLAG'] == 'Y' ):
##                text += 'CAA, ' 
##            if ( row['NPDES_FLAG'] == 'Y' ):
##                text += 'CWA, ' 
##            if ( row['SDWIS_FLAG'] == 'Y' ):
##                text += 'SDWIS, ' 
##            if ( row['RCRA_FLAG'] == 'Y' ):
##                text += 'RCRA, ' 
##            if ( row['TRI_FLAG'] == 'Y' ):
##                text += 'TRI, ' 
##            if ( row['GHG_FLAG'] == 'Y' ):
##                text += 'GHG, ' 
##            text = text[:-1]
            
            text += " - <p><a href='"+row["DFR_URL"]
            text += "' target='_blank'>Link to ECHO detailed report</a></p>"
    return text


#####################
#  mapper(df, is_echo=True):
#    
# Display a map of the DataFrame passed in.
# Based on https://medium.com/@bobhaffner/folium-markerclusters-and-fastmarkerclusters-1e03b01cb7b1
#
# Parameters:  
#    df -- A DataFrame containing records with latitude and longitude fields
#        that can be plotted on a map
#    is_echo -- A flag indicating whether the data contains ECHO_EXPORTER fields
#        that can identify the EPA programs tracked for facilities
#
#####################

def mapper(df, is_echo=True):
    # Initialize the map
    m = folium.Map(
        location = [df.mean()["FAC_LAT"], df.mean()["FAC_LONG"]]
    )

    # Create the Marker Cluster array
    #kwargs={"disableClusteringAtZoom": 10, "showCoverageOnHover": False}
    mc = FastMarkerCluster("")
 
    # Add a clickable marker for each facility
    for index, row in df.iterrows():
        mc.add_child(folium.CircleMarker(
            location = [row["FAC_LAT"], row["FAC_LONG"]],
            popup = marker_text( row, is_echo ),
            radius = 8,
            color = "black",
            weight = 1,
            fill_color = "orange",
            fill_opacity= .4
        ))
    
    m.add_child(mc)
    bounds = m.get_bounds()
    m.fit_bounds(bounds)

    # Show the map
    return m

#####################
# write_file( df, base, type, state, region ):
#    
# Write a file of the DataFrame passed in.
#
# Parameters:  
#    df -- The DataFrame to write.
#    base -- The base name of the file to write.
#    type -- The region type of the data.
#    state -- The state (or None).
#    region -- The region identifier, e.g. CD number, County, Zip code.
#
#####################
def write_dataset( df, base, type, state, region ):
    if ( len( df ) > 0 ):
        filename = base
        if ( type != 'Zip Code' ):
            filename += '-' + state
        filename += '-' + type
        if ( region is not None ):
            filename += '-' + str(region)
        filename += '.csv'
        df.to_csv( filename ) 
        print( "Wrote " + filename )
    else:
        print( "There is no data to write." )

def make_filename( base, type, state, region ):
    x = datetime.datetime.now()
    filename = base + '_' + state + '-' + str(region) + '-' \
                + x.strftime( "%m%d%y") +'.csv'
    return filename