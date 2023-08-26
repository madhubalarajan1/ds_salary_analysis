# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:29:01 2023

@author: madhu
"""

import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/madhu/Documents/ds_salary_analysis/chromedriver"

df = gs.get_jobs('data scientist', 3, False, 5, path)

print(df.head())

# import glassdoor_scraper_1 as gs
# import pandas as pd

# path = "C:/Users/madhu/Documents/ds_salary_analysis/chromedriver"

# df = gs.fetch_jobs('data scientist', 2, path)