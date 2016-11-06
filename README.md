# df_tools
Additional tools for pandas DataFrames, specifically lists of DataFrames.

Version: 1.0
Created: 10/15/2016
Author email: cameron@tutanota.com

Dependencies:
1. pandas: Required for basic pandas DataFrame functionality and methods.
2. numpy: Used for checking and manipulation of numpy data types.

General Notes:
The df_tools package was originally created from disparate functions that were
written as parts of other projects before being added to this package. Most of the
functions are designed to handle lists of pandas dataframes, and were originally written
to handle a series of data frames containing multiple time series of chemical concentration data.
However, they are written generally and should handle similar numerical data. All functions 
were tested on numerical time series during intial implementation, and caution should be used
if your data frames contain non-numeric data.

Please email the author with any suggestions, comments or questions.
