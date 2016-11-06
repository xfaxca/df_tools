"""
This module contains functions to manipulate pandas DataFrames, both individually
and in lists. Originally written and intended for >= Python 3.5. Not yet tested
on previous versions.
"""

import df_tools.df_utils
import df_tools.list_utils

# df_utils.py function import
from df_tools.df_utils import idx0
from df_tools.df_utils import avg_cols
from df_tools.df_utils import avg_rows
from df_tools.df_utils import drop_cols
from df_tools.df_utils import top_series_mean
from df_tools.df_utils import top_series_max
from df_tools.df_utils import top_series_quantile
from df_tools.df_utils import norm_cols_each
from df_tools.df_utils import norm_cols_all
#
# list_utils.py function import
from df_tools.list_utils import idx0_ls
from df_tools.list_utils import create_df_ls
from df_tools.list_utils import drop_cols_df_ls
from df_tools.list_utils import norm_by_factors
from df_tools.list_utils import df_col_avg_sum
from df_tools.list_utils import find_min_rows
from df_tools.list_utils import truncate_dfs
from df_tools.list_utils import dropna_df_ls
from df_tools.list_utils import set_indices_ls
# Time series functions
from df_tools.list_utils import top_series_mean_ls
from df_tools.list_utils import top_series_max_ls
from df_tools.list_utils import top_series_quantile_ls
from df_tools.list_utils import norm_cols_all_ls
from df_tools.list_utils import norm_cols_each_ls
# DataFrame joining/concatenation/merging functions
from df_tools.list_utils import concat_ls
from df_tools.list_utils import concat_trans_ls


# Documentation, version #, etc.
__doc__ = "Package: df_tools v1.0\n" \
          "Created: 09/20/2016\n" \
          "Author contact: gnomeslice@tutanota.com \n" \
          "Description: A package for manipulation and modification of pandas DataFrames, both single objects and \n" \
          "lists. Functions for single DataFrames are in df_tools.df_utils, those for lists of DataFrames are in  \n" \
          "df_tools.list_utils and error checking functions are in df_tools.err_check. \n"
__author__ = "Cameron Faxon"
__copyright__ = "Copyright (C) 2016 Cameron Faxon"
__license__ = "GNU GPLv3"
__version__ = "1.0"
__all__ = ["create_df_ls", "idx0_ls", "drop_cols_df_ls", "norm_by_factors", "df_col_avg_sum", "find_min_rows",
           "truncate_dfs", "dropna_df_ls", "set_indices_ls", "top_series_mean_ls", "top_series_max_ls",
           "top_series_quantile_ls", "concat_ls", "norm_cols_all_ls", "norm_cols_each_ls", "idx0", "avg_cols",
           "avg_rows", "drop_cols", "top_series_mean", "top_series_max", "top_series_quantile", "norm_cols_each",
           "norm_cols_all"]




