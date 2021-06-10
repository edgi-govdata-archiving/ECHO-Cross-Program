[![Code of Conduct](https://img.shields.io/badge/%E2%9D%A4-code%20of%20conduct-blue.svg?style=flat)](https://github.com/edgi-govdata-archiving/overview/blob/master/CONDUCT.md)

# ECHO-Cross-Programs
This repository contains Jupyter notebooks for ECHO that use data from multiple
EPA programs. These notebooks let viewers examine facilities by state, county, congressional district, or zip code, and collect the program-specific data for all the facilities in the region. The notebooks look at emissions, violations, inspections, and enforcement for the Clean Air Act, Clean Water Act, and Resouce Conservation and Recovery Act.

- The AllPrograms notebook gathers data for specified Congressional Districts and States and outputs CSV files used in the creation of congressional report cards.  A link to the notebook on Google Colab is here: https://colab.research.google.com/github/edgi-govdata-archiving/ECHO-Cross-Program/blob/master/AllPrograms.ipynb.
- The ECHO_National notebook produces data on national metrics, also used in the creation of congressional report cards.  On Google Colab it is here: https://colab.research.google.com/github/edgi-govdata-archiving/ECHO-Cross-Program/blob/master/ECHO_National.ipynb

- The ECHO-Cross-Program notebook is the more user-interactive notebook for investigating ECHO data.  It lets the user select a geographic region--state, Congressional District, county or zip code--and then view data from the various EPA programs for facilities in the region.  A link to the notebook on Google Colab is here: https://colab.research.google.com/github/edgi-govdata-archiving/ECHO-Cross-Program/blob/master/ECHO-Cross-Programs.ipynb

## Report Cards
The report cards that are based on the data collected by the AllPrograms and ECHO_National notebooks can be seen on the EEW website at this link:  https://environmentalenforcementwatch.org/reports

## License & Copyright

Copyright (C) <year> Environmental Data and Governance Initiative (EDGI)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.0.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the [`LICENSE`](/LICENSE) file for details.
