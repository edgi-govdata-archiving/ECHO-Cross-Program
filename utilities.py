# Import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
from ECHO_modules.DataSet import get_data

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

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

region_field = { 
    'State': { "field": 'FAC_STATE' },
    'Congressional District': { "field": 'FAC_DERIVED_CD113' },
    'County': { "field": 'FAC_COUNTY' },
    'Zip Code': { "field": 'FAC_DERIVED_ZIP' }
}


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
    output_state = widgets.Output()
    
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
    selected_region_field = region_field[ type ]
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
# show_data_set_widget( data_sets, echo_data ):
#    
# Create and return a dropdown list of data sets with appropriate
# flags set in the echo_data. 
#
# Parameters:
#    data_sets -- The Dictionary of data sets. Values are instances
#        of class DataSet.
#    echo_data -- The ECHO_EXPORTER data with flags for program types
#
# Return: The widget of data set choices
#
#####################

def show_data_set_widget( data_sets, echo_data ):
    # Only list the data set if it has the correct flag set.
    data_set_choices = []
    for k, v in data_sets.items():
        if ( v.has_echo_flag( echo_data ) ):
            data_set_choices.append( k )
    
    # data_set_choices = list( data_sets.keys() )
    
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
#  show_fac_pgm_widget( fac_data, data_sets ):
#    
# Create and return a dropdown list of program data sets associated
# with the facility (ECHO_EXPORTER) data.
#
# Parameters:
#    fac_data -- A DataFrame of ECHO_EXPORTER facilities
#    data_sets -- The Dictionary of DataSet instances
#
# Return: The widget with associated data sets
#
#####################

def show_fac_pgm_widget( fac_data, data_sets ):
    data_set_choices = []
    for k, v in data_sets.items():
        if ( v.has_echo_flag( fac_data ) ):
            data_set_choices.append( k )
    
    widget=widgets.Dropdown(
        options=data_set_choices,
        description='Data sets:',
        disabled=False,
    )
    display(widget)
    return widget


#####################
#  get_echo_data( region_type, region_widget, state_widget = None ):
#    
# Query the database for ECHO_EXPORTER data appropriate to the parameters.
#
# Parameters:
#    region_type -- The type of region
#    region_widget -- The widget that will contain the region selected.
#    state_widget -- The widget that will contain the state selected.
#
# Return: A DataFrame of the data retrieved.
#
#####################

def get_echo_data( region_type, region_widget, state_widget = None ):
    if ( region_type == 'State'):
        region_value = state_widget.value
    else:
        region_value = region_widget.value

    echo_data_sql = "select * from ECHO_EXPORTER where " + region_field[region_type]['field']
    if ( region_type == 'County' ):    
        echo_data_sql += " like \'" + str( region_value) + "%\'"
    else:
        echo_data_sql += " = '" + str( region_value ) + "'"
    if ( region_type == 'Congressional District' or region_type == 'County' ):
        echo_data_sql += " and FAC_STATE = \'" + state_widget.value + "\'"
    echo_data = None
    try:
        echo_data = get_data( echo_data_sql, 'REGISTRY_ID' )
    except pd.errors.EmptyDataError:
        pass
    if ( echo_data.empty ):
        print("\nThere are no EPA facilities in this region.\n")
    else:
        print("\nThere are %s EPA facilities in this region tracked in the ECHO database." \
              %(echo_data.shape[0] ))
    return echo_data


#####################
#  get_program_data( program, echo_data ):
#    
# Based on the program requested, get the appropriate IDs from the echo_data.
# Then use the program DataSet class to query the database for the set of
# records by the ID list.
#
# Parameters:
#    program -- An instance of class DataSet for a program
#    echo_data -- The ECHO_EXPORTER facility records containing flags and
#        IDs for programs associated with the facilities
#
# Return: A DataFrame containing the retrieved program data.
#
#####################

def get_program_data( program, echo_data ):
    program_data = None
    key=dict() # Create a way to look up Registry IDs in ECHO_EXPORTER later
    
    # We need to provide a custom list of program ids for some programs.
    if ( program.name == "Air Inspections" or program.name == "Air Enforcements" ):
        # The REGISTRY_ID field is the index of the echo_data
        registry_ids = echo_data[echo_data['AIR_FLAG'] == 'Y'].index.values
        key = { i : i for i in registry_ids }
        program_data = program.get_data( ee_ids=registry_ids )
    elif ( program.name == "Combined Air Emissions" ):
        ghg_registry_ids = echo_data[echo_data['GHG_FLAG'] == 'Y'].index.values
        tri_registry_ids = echo_data[echo_data['TRI_FLAG'] == 'Y'].index.values
        id_set = np.union1d( ghg_registry_ids, tri_registry_ids )
        registry_ids = list(id_set)
        program_data = program.get_data( ee_ids=registry_ids )
        key = { i : i for i in registry_ids }
    elif ( program.name == "Greenhouse Gases" or program.name == "Toxic Releases" ):
        program_flag = program.echo_type + '_FLAG'
        registry_ids = echo_data[echo_data[ program_flag ] == 'Y'].index.values
        program_data = program.get_data( ee_ids=registry_ids )
        key = { i : i for i in registry_ids }
    else:
        ids_string = program.echo_type + '_IDS'
        ids = list()
        registry_ids = list()
        for index, value in echo_data[ ids_string ].items():
            try:
                for this_id in value.split():
                    ids.append( this_id )
                    key[this_id]=index
            except ( KeyError, AttributeError ) as e:
                pass
        program_data = program.get_data( ee_ids=ids )
    
    # Find the facility that matches the program data, by REGISTRY_ID.  
    # Add lat and lon, facility name and REGISTRY_ID as fac_registry_id. 
    # (Note: not adding REGISTRY_ID right now as it is sometimes interpreted 
    # as an int and that messes with the charts...)
    my_prog_data = pd.DataFrame()
    no_data_ids = []
    
    # Look through all the facilities in my area and program and get supplemental 
    # echo_data info
    if (program_data is None): # Handle no data
        print("Sorry, we don't have data for this program! That could be an error" \
            " on our part, or ECHO's, or because the data type doesn't apply to this area.")
    else:
        # breakpoint()
        for fac in program_data.itertuples():
            fac_id = fac.Index
            try:
                reg_id = key[fac_id] # Look up this facility's Registry ID through its Program ID
                echo_row = pd.DataFrame(echo_data.loc[reg_id].copy()).T.reset_index() # Find and filter to the corresponding row in ECHO_EXPORTER
                echo_row = echo_row[['FAC_NAME', 'FAC_LAT', 'FAC_LONG']] # Keep only the columns we need
                program_row =  pd.DataFrame([list(fac)[1:]], columns=program_data.columns.values) # Turn the program_data tuple into a DataFrame
                full_row = pd.concat([program_row, echo_row], axis=1) # Join the EE row df and the program row df
                frames = [my_prog_data, full_row]
                my_prog_data = pd.concat( frames, ignore_index=False)
            except KeyError:
                # The facility wasn't found in the program data.
                no_data_ids.append( fac.Index )
    return my_prog_data


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
            d = d.resample("Y").count()
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
            if ( row['AIR_FLAG'] == 'Y' ):
                text += 'CAA, ' 
            if ( row['NPDES_FLAG'] == 'Y' ):
                text += 'CWA, ' 
            if ( row['SDWIS_FLAG'] == 'Y' ):
                text += 'SDWIS, ' 
            if ( row['RCRA_FLAG'] == 'Y' ):
                text += 'RCRA, ' 
            if ( row['TRI_FLAG'] == 'Y' ):
                text += 'TRI, ' 
            if ( row['GHG_FLAG'] == 'Y' ):
                text += 'GHG, ' 
            text = text[:-1]
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
def write_file( df, base, type, state, region ):
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
