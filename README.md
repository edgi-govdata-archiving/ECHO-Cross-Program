[![Code of Conduct](https://img.shields.io/badge/%E2%9D%A4-code%20of%20conduct-blue.svg?style=flat)](https://github.com/edgi-govdata-archiving/overview/blob/master/CONDUCT.md)

# ECHO-Cross-Programs
This repository contains Jupyter notebooks for processing the EPA's Environmenal Compliance History Online (ECHO) data from multiple
EPA programs. These notebooks let viewers examine facilities by state, county, congressional district, or zip code, and collect the program-specific data for all the facilities in the region. The notebooks look at emissions, violations, inspections, and enforcement for the Clean Air Act, Clean Water Act, and Resouce Conservation and Recovery Act.

Background on the EPA's ECHO data and the organization of code supporting the notebooks in this repository can be found at [this page] (https://github.com/edgi-govdata-archiving/ECHO-Cross-Program/blob/main/background-overview.md)

- The ECHO-Cross-Program notebook is a user-interactive notebook for investigating ECHO data.  It lets the user select a geographic region--state, Congressional District, county or zip code--and then view data from the various EPA programs for facilities in the region.  A link to the notebook on Google Colab is here: https://colab.research.google.com/github/edgi-govdata-archiving/ECHO-Cross-Program/blob/master/ECHO-Cross-Programs.ipynb
- The ECHO_National notebook produces data on national metrics, which were used in the creation of the Environmental Enforcement Watch's 2020 congressional report cards for Senators and members of the House of Representatives serving on two key committees overseeing the EPA. This functionality has been moved to Python code in the EEW-ReportCard-Data repository for the next version of report cards.
- The Spanish_ECHO_National notebook is a Spanish translation of the ECHO_National notebook.
- The RegionMaps notebook produced maps of congressional districts showing facility locations.  It was also used for the 2020 congressional report cards, and its functionality has been moved into the EEW-REportCard-Data repository.

The notebooks in this repository rely on code in the [ECHO_modules repository](https://github.com/edgi-govdata-archiving/ECHO_modules), where we house code that is common to a number of different projects. Moving the code out of the Jupyter notebook allows a user to see the high-level flow of the analysis in the notebook without having to see all the details of the code that works behind the scenes.

#### [Here are suggestions for how you can help us with issues in this repository.](https://github.com/edgi-govdata-archiving/ECHO-Cross-Program/blob/main/helping.md)

## License & Copyright

Copyright (C) <year> Environmental Data and Governance Initiative (EDGI)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.0.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the [`LICENSE`](/LICENSE) file for details.
