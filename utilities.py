'''
Provide a number of utility Python functions that can de-clutter
the Jupyter notebooks that use them.
'''

# Import libraries

import os 
import csv
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import seaborn as sns
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


def fix_county_names( in_counties ):
    '''
    ECHO_EXPORTER has counties listed both as ALAMEDA and ALAMEDA COUNTY, seemingly
    for every county.  We drop the 'COUNTY' so they only get listed once.

    Parameters
    ----------
    in_counties : list of county names (str)

    Returns
    -------
    list
        The list of counties without duplicates
    '''

    counties = []
    for county in in_counties:
        if (county.endswith( ' COUNTY' )):
            county = county[:-7]
        counties.append( county.strip() )
    counties = np.unique( counties )
    return counties


def show_region_type_widget():
    '''
    Create and return a dropdown list of types of regions

    Returns
    -------
    widget
        The dropdown widget with the list of regions
    '''

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


def show_state_widget():
    '''
    Create and return a dropdown list of states

    Returns
    -------
    widget
        The dropdown widget with the state list
    '''

    dropdown_state=widgets.Dropdown(
        options=states,
        description='State:',
        disabled=False,
    )
    
    display( dropdown_state )
    return dropdown_state


def show_pick_region_widget( type, state_widget=None ):
    '''
    Create and return a dropdown list of regions appropriate
    to the input parameters

    Parameters
    ----------
    type : str
        The type of region
    state_widget : widget
        The widget in which a state may have been selected

    Returns
    -------
    widget
        The dropdown widget with region choices
    '''

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


def show_data_set_widget( data_sets ):
    '''
    Create and return a dropdown list of data sets with appropriate
    flags set in the echo_data.

    Parameters
    ----------
    data_sets : dict
        The data sets, key = name, value = DataSet object

    Returns
    -------
    widget
        The widget with data set choices
    '''
    
    data_set_choices = list( data_sets.keys() )
    
    data_set_widget=widgets.Dropdown(
        options=list(data_set_choices),
        description='Data sets:',
        disabled=False,
    ) 
    display(data_set_widget)
    return data_set_widget


def show_fac_widget( fac_series ):
    '''
    Create and return a dropdown list of facilities from the 
    input Series

    Parameters
    ----------
    fac_series : Series
        The facilities to be shown.  It may have duplicates.

    Returns
    -------
    widget
        The widget with facility names
    '''

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


def get_active_facilities( state, region_type, region_selected ):
    '''
    Get a Dataframe with the ECHO_EXPORTER facilities with FAC_ACTIVE_FLAG
    set to 'Y' for the region selected.

    Parameters
    ----------
    state : str
        The state, which could be None
    region_type : str
        The type of region:  'State', 'Congressional District', etc.
    region_selected : str
        The selected region of the specified region_type

    Returns
    -------
    Dataframe
        The active facilities returned from the database query
    '''

    if ( region_type == 'State' ):
        sql = 'select * from "ECHO_EXPORTER" where "FAC_STATE" = \'{}\''
        sql += ' and "FAC_ACTIVE_FLAG" = \'Y\''
        sql = sql.format( state )
        df_active = get_data( sql, 'REGISTRY_ID' )
    elif ( region_type == 'Congressional District'):
        sql = 'select * from "ECHO_EXPORTER" where "FAC_STATE" = \'{}\''
        sql += ' and "FAC_DERIVED_CD113" = \'{}\''
        sql += ' and "FAC_ACTIVE_FLAG" = \'Y\''
        sql = sql.format( state, region_selected )
        df_active = get_data( sql, 'REGISTRY_ID' )
    elif ( region_type == 'County' ):
        sql = 'select * from "ECHO_EXPORTER" where "FAC_STATE" = \'{}\''
        sql += ' and "FAC_COUNTY" = \'{}\''
        sql += ' and "FAC_ACTIVE_FLAG" = \'Y\''
        sql = sql.format( state, region_selected )
        df_active = get_data( sql, 'REGISTRY_ID' )
    else:  ## Zip code
        sql = 'select * from "ECHO_EXPORTER" where "FAC_ZIP" = \'{}\''
        sql += ' and "FAC_ACTIVE_FLAG" = \'Y\''
        sql = sql.format( region_selected )
        df_active = get_data( sql, 'REGISTRY_ID' )
    return df_active


def marker_text( row, no_text ):
    '''
    Create a string with information about the facility or program instance.

    Parameters
    ----------
    row : Series
        Expected to contain FAC_NAME and DFR_URL fields from ECHO_EXPORTER
    no_text : Boolean
        If True, don't put any text with the markers, which reduces chance of errors 

    Returns
    -------
    str
        The text to attach to the marker
    '''

    text = ""
    if ( no_text ):
        return text
    if ( type( row['FAC_NAME'] == str )) :
        try:
            text = row["FAC_NAME"] + ' - '
        except TypeError:
            print( "A facility was found without a name. ")
        text += " - <p><a href='"+row["DFR_URL"]
        text += "' target='_blank'>Link to ECHO detailed report</a></p>"
    return text


def check_bounds( row, bounds ):
    '''
    See if the FAC_LAT and FAC_LONG of the row are interior to
    the minx, miny, maxx, maxy of the bounds.

    Parameters
    ----------
    row : Series
	Must contain FAC_LAT and FAC_LONG
    bounds : Dataframe
	Bounding rectangle--minx,miny,maxx,maxy

    Returns
    -------
    True if the row's point is in the bounds
    '''

    if ( row['FAC_LONG'] < bounds.minx[0] or row['FAC_LAT'] < bounds.miny[0] \
         or row['FAC_LONG'] > bounds.maxx[0] or row['FAC_LAT'] > bounds.maxy[0]):
        return False
    return True


def mapper(df, bounds=None, no_text=False):
    '''
    Display a map of the Dataframe passed in.
    Based on https://medium.com/@bobhaffner/folium-markerclusters-and-fastmarkerclusters-1e03b01cb7b1

    Parameters
    ----------
    df : Dataframe
        The facilities to map.  They must have a FAC_LAT and FAC_LONG field.
    bounds : Dataframe
        A bounding rectangle--minx, miny, maxx, maxy.  Discard points outside.

    Returns
    -------
    folium.Map
    '''

    # Initialize the map
    m = folium.Map(
        location = [df.mean()["FAC_LAT"], df.mean()["FAC_LONG"]]
    )

    # Create the Marker Cluster array
    #kwargs={"disableClusteringAtZoom": 10, "showCoverageOnHover": False}
    mc = FastMarkerCluster("")
 
    # Add a clickable marker for each facility
    for index, row in df.iterrows():
        if ( bounds is not None ):
            if ( not check_bounds( row, bounds )):
                continue
        mc.add_child(folium.CircleMarker(
            location = [row["FAC_LAT"], row["FAC_LONG"]],
            popup = marker_text( row, no_text ),
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


def write_dataset( df, base, type, state, region ):
    '''
    Write out a file of the Dataframe passed in.

    Parameters
    ----------
    df : Dataframe
        The data to write.
    base: str
        A base string of the file to write
    type: str
        The region type of the data
    state: str
        The state, or None
    region: str
        The region identifier, e.g. CD number, County, State, Zip code
    '''
    if ( df is not None and len( df ) > 0 ):
        if ( not os.path.exists( 'CSVs' )):
            os.makedirs( 'CSVs' )
        filename = 'CSVs/' + base
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


def make_filename( base, type, state, region, filetype='csv' ):
    '''
    Make a filename from the parameters and return it.
    The filename will be in the Output directory relative to
    the current working directory, and in a sub-directory
    built out of the state and CD.

    Parameters
    ----------
    base : str
        A base string of the file
    type : str
        The region type
    state : str
        The state or None
    region : str
        The region
    filetype : str
        Optional file suffix.

    Returns
    -------
    str
        The filename created.

    Examples
    --------
    >>> filename = make_filename( 'noncomp_CWA_pg6', *df_type )
    '''
    # If type is 'State', the state name is the region.
    dir = 'Output/'
    if ( type == 'State' ):
        dir += region
        filename = base + '_' + region
    else:
        dir += state
        filename = base + '_' + state
        if ( region is not None ):
            dir += str(region)
            filename += '-' + str(region)
    x = datetime.datetime.now()
    filename += '-' + x.strftime( "%m%d%y") +'.' + filetype
    dir += '/'
    if ( not os.path.exists( dir )):
        os.makedirs( dir )
    return dir + filename


def get_top_violators( df_active, flag, state, cd, noncomp_field, action_field, num_fac=10 ):
    '''
    Sort the dataframe and return the rows that have the most number of
    non-compliant quarters.

    Parameters
    ----------
    df_active : Dataframe
        Must have ECHO_EXPORTER fields
    flag : str
        Identifies the EPA programs of the facility (AIR_FLAG, NPDES_FLAG, etc.)
    state : str
        The state
    cd : str
        The congressional district    
    noncomp_field : str
        The field with the non-compliance values, 'S' or 'V'.
    action_field
        The field with the count of quarters with formal actions
    num_fac
        The number of facilities to include in the returned Dataframe

    Returns
    -------
    Dataframe
        The top num_fac violators for the EPA program in the region

    Examples
    --------
    >>> df_violators = get_top_violators( df_active, 'AIR_FLAG', state, region_selected, 
        'CAA_3YR_COMPL_QTRS_HISTORY', 'CAA_FORMAL_ACTION_COUNT', 20 )
    '''
    df = df_active.loc[ df_active[flag] == 'Y' ]
    if ( len( df ) == 0 ):
        return None
    df_active = df.copy()
    noncomp = df_active[ noncomp_field ]
    noncomp_count = noncomp.str.count('S') + noncomp.str.count('V')
    df_active['noncomp_count'] = noncomp_count
    df_active = df_active[['FAC_NAME', 'noncomp_count', action_field,
            'DFR_URL', 'FAC_LAT', 'FAC_LONG']]
    df_active = df_active.sort_values( by=['noncomp_count', action_field], 
            ascending=False )
    df_active = df_active.head( num_fac )
    return df_active   

def chart_top_violators( ranked, state, cd, epa_pgm ):
    '''
    Draw a horizontal bar chart of the top non-compliant facilities.

    Parameters
    ----------
    ranked : Dataframe
        The facilities to be charted
    state : str
        The state
    cd : integer
        The Congressional District
    epa_pgm : str
        The EPA program associated with this list of non-compliant facilities

    Returns
    -------
    seaborn.barplot
        The graph that is generated
    '''
    sns.set(style='whitegrid')
    fig, ax = plt.subplots(figsize=(20,10))
    unit = ranked.index 
    values = ranked['noncomp_count'] 
    try:
        g = sns.barplot(values, unit, order=list(unit), orient="h") 
        g.set_title('{} facilities with the most non-compliant quarters in {} - {}'.format( 
                epa_pgm, state, str( cd )))
        ax.set_xlabel("Non-compliant quarters")
        ax.set_ylabel("Facility")
        ax.set_yticklabels(ranked["FAC_NAME"])
        return ( g )
    except TypeError as te:
        print( "TypeError: {}".format( str(te) ))
        return None
