from ECHO_modules.make_data_sets import make_data_sets
from ECHO_modules.utilities import mapper

data_sets = make_data_sets([
    "RCRA Violations",
    "RCRA Inspections",
    "RCRA Penalties",
    "CAA Violations",
    "CAA Penalties",
    "CAA Inspections",
    "Combined Air Emissions",
    "Greenhouse Gas Emissions",
    "Toxic Releases",
    "CWA Violations",
    "CWA Inspections",
    "CWA Penalties",
    "SDWA Site Visits",
    "SDWA Enforcements",
    "SDWA Public Water Systems",
    "SDWA Violations",
    "SDWA Serious Violators"
])

def _run_test(program, region_type, region_value, state=None, years=None):
    program_results = program.store_results( region_type='County',
                                region_value=['ADAMS', 'JEFFERSON'], state='CO', 
                                years=[2015,2023])
    program_data = None
    if ( program_results is not None ):
        program_data = program_results.dataframe.copy()
    else:
        print( "There is no data for this data set in this region.")
    print(len(program_data))
    mapper(program_data)

program = data_sets['RCRA Violations']
region_type = 'County'
region_value = ['ADAMS', 'JEFFERSON']
state = 'CO'
years = [2013, 2023]

_run_test(program=program, region_type=region_type, region_value=region_value, 
          state=state, years=years)

program = data_sets['CWA Violations']
region_type = 'Neighborhood'
years = [2010, 2023]
region_value = ((-95.983772, 41.2768), 
                (-95.898628, 41.295891), 
                (-95.927467, 41.270607), 
                (-95.919914, 41.238602), 
                (-95.956306, 41.230857), 
                (-95.998878, 41.244798))

_run_test(program=program, region_type=region_type, region_value=region_value, 
          state=None, years=years)