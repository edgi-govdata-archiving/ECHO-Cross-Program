# Create a DataSet object for each of the programs we track.  
# Initialize each one with the information it needs to do its query
# of the database.
# Store the DataSet objects in a dictionary with keys being the
# friendly names of the program, which will be used in selection
# widgets.

# In the following line, 'from DataSet' refers to the file DataSet.py
# while 'import DataSet' refers to the DataSet class within DataSet.py.

from ECHO_modules.DataSet import DataSet

def make_data_sets():
    data_sets = {}
    ds = DataSet( name='RCRA Violations', idx_field='ID_NUMBER', 
                    table_name='RCRA_VIOLATIONS_VIEW', echo_type="RCRA",
                    date_field='DATE_VIOLATION_DETERMINED', date_format='%m/%d/%Y')
    data_sets[ ds.name ] = ds
    ds = DataSet( name='RCRA Inspections', idx_field='ID_NUMBER', 
                    table_name='RCRA_EVALUATIONS_VIEW', echo_type="RCRA",
                    date_field='EVALUATION_START_DATE', date_format='%m/%d/%Y')
    data_sets[ ds.name ] = ds
    ds = DataSet( name='RCRA Enforcements',  echo_type="RCRA",
                    table_name='RCRA_ENFORCEMENTS_VIEW', idx_field='ID_NUMBER', 
                    date_field='EVALUATION_START_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Air Inspections', echo_type="AIR",
                    table_name='AIR_INSPECTIONS_VIEW', idx_field='REGISTRY_ID', 
                    date_field='ACTUAL_END_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Air Enforcements',  echo_type="AIR",
                    table_name='AIR_ENFORCEMENTS_VIEW', idx_field='REGISTRY_ID',
                    date_field='FISCAL_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Air Violations',  echo_type="AIR",
                    table_name='AIR_VIOLATIONS_VIEW', idx_field='pgm_sys_id', 
                    date_field='HPV_DAYZERO_DATE', date_format='%m-%d-%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Air Formal Actions', echo_type="AIR",
                    table_name='AIR_FORMAL_ACTIONS_VIEW', idx_field='pgm_sys_id',
                    date_field='SETTLEMENT_ENTERED_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Air Compliance', echo_type="AIR",
                    table_name='AIR_COMPLIANCE_VIEW', idx_field='PGM_SYS_ID',
                    date_field='ACTUAL_END_DATE', date_format='%m-%d-%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Combined Air Emissions', echo_type=["GHG","TRI"],
                    table_name='COMBINED_AIR_EMISSIONS_VIEW', idx_field='REGISTRY_ID',
                    date_field='REPORTING_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Greenhouse Gases', echo_type="GHG",
                    table_name='GREENHOUSE_GASES_VIEW', idx_field='REGISTRY_ID',
                    date_field='REPORTING_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Toxic Releases', echo_type="TRI",
                    table_name='TOXIC_RELEASES_VIEW', idx_field='REGISTRY_ID',
                    date_field='REPORTING_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Water Quarterly Violations', echo_type="NPDES",
                    table_name='WATER_QUARTERLY_VIOLATIONS_VIEW', idx_field='NPDES_ID',
                    date_field='YEARQTR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Clean Water Inspections', echo_type="NPDES",
                    table_name='CLEAN_WATER_INSPECTIONS_VIEW', idx_field='NPDES_ID',
                    date_field='ACTUAL_END_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='Clean Water Enforcements', echo_type="NPDES",
                    table_name='CLEAN_WATER_ENFORCEMENT_ACTIONS_VIEW', idx_field='NPDES_ID',
                    date_field='SETTLEMENT_ENTERED_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='SDWA Site Visits', echo_type="SDWA",
                    table_name='SDWA_SITE_VISITS_VIEW', idx_field='PWSID',
                    date_field='SITE_VISIT_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='SDWA Enforcements', echo_type="SDWA",
                    table_name='SDWA_ENFORCEMENTS_VIEW', idx_field='PWSID',
                    date_field='ENFORCEMENT_DATE', date_format='%m/%d/%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='SDWA Public Water Systems', echo_type="SDWA",
                    table_name='SDWA_PUB_WATER_SYSTEMS_VIEW', idx_field='PWSID',
                    date_field='FISCAL_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='SDWA Violations', echo_type="SDWA",
                    table_name='SDWA_VIOLATIONS_VIEW', idx_field='PWSID',
                    date_field='FISCAL_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    ds = DataSet( name='SDWA Serious Violators', echo_type="SDWA",
                    table_name='SDWA_SERIOUS_VIOLATORS_VIEW', idx_field='PWSID',
                    date_field='FISCAL_YEAR', date_format='%Y' )
    data_sets[ ds.name ] = ds
    # ds = DataSet( name='SDWA Return to Compliance', echo_type="SDWA",
    #                 table_name='SDWA_RETURN_TO_COMPLIANCE', idx_field='PWSID',
    #                 date_field='FISCAL_YEAR', date_format='%Y' )
    # data_sets[ ds.name ] = ds
    return data_sets

