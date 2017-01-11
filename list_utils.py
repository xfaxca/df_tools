# list_utils.py

"""
This module provides functions for handling lists of pandas DataFrames.
Examples include: normalization of columns, dropping of specific columns
truncation of DataFrames to a maximum length, re-indexing, and pairwise
concatenation of DataFrame lists. For functions handling single DataFrames
please use df_utils.

Functions:
create_df_ls, idx0_ls, drop_cols_df_ls, norm_by_factors, df_col_avg_sum
find_min_rows, truncate_dfs, dropna_df_ls, set_indices_ls, top_series_mean_ls
top_series_max_ls, top_series_quantile_ls, concat_ls, norm_cols_each_ls
norm_cols_all_ls.

See the doc strings for individual functions for further information.
"""

from df_tools.df_utils import *
import df_tools._err_check as _ec
import sys
import pandas as pd
from pathlib import Path

__all__ = ['create_df_ls',
           'idx0_ls',
           'drop_cols_df_ls',
           'norm_by_factors',
           'df_col_avg_sum',
           'find_min_rows',
           'truncate_dfs',
           'dropna_df_ls',
           'set_indices_ls',
           'top_series_mean_ls',
           'top_series_max_ls',
           'top_series_quantile_ls',
           'concat_ls',
           'concat_trans_ls',
           'norm_cols_each_ls',
           'norm_cols_all_ls']


def create_df_ls(flist=[""], indir=""):
    """
    This function takes a list of string values that are the paths and file names to csv files. The csv files are
        then individually loaded into pandas DataFrames and returned in a list containing a DataFrame for each csv
        in flist.

    Parameters:
    :param flist: A list of string values that contain the names of csv files to be loaded into pandas DataFrames
    :param indir: A string value that is the optional base directory of all of the csv files. If the full path for
        each file is included in flist, then this parameter should be left blank (""). Otherwise, the base directory
        where the csv files reside should be used.
    :return: df_ls: A list of pandas DataFrames loaded from the csvs specified in flist.
    """
    # Check passed parameter values to prevent error in future.
    _ec.check_ls(ls=flist)
    _ec.check_string(values=flist)
    _ec.check_string(values=[indir])

    df_ls = []
    for f in flist:
        file = Path(indir+f)
        if file.is_file():
            df = pd.DataFrame.from_csv(indir+f)
            df_ls.append(df)
            print('file "%s" added to list.' % f)
        else:
            print("File '%s' not found. Not included in DataFrame list." % (indir+f))

    return df_ls


def idx0_ls(df_ls):
    """
    This function subtracts each DataFrame's first index value from all values in the index. This was designed
        with the aim of create a "t_0" (or "time elapsed") time series - that is, a time series where the first
         time index is t = 0. This function does not account for units of time and subtracts the first index value
         from all other values in the index. Use is only suggested for DataFrames containing time series, but it
         should function with all numeric indices.

    Parameters:
    :param df_ls: A list of pandas DataFrames for which the index of each is to be offset by the first index value.
    :return: df_t0_ls: A list of pandas DataFrames with offset indices.
    """
    # Check to make sure index values are numeric and in a pandas DataFrame.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)

    df_idx0_ls = []
    for df in df_ls:
        _ec.check_numeric(values=df.index.values)
        df_idx0 = df.copy()
        df_idx0.index = (df.index.values - df.index.values[0])
        df_idx0_ls.append(df_idx0)

    return df_idx0_ls


def drop_cols_df_ls(df_ls, cols2drop=['none'], inplace=True):
    """
    This function drops a single specified column of a given name in each pandas DataFrame in list if it exists. It
        does this 'in place' such that nothing is returned, but the passed DataFrames are modified in the original
        script.

    Parameters:
    :param df_ls: A list of pandas DataFrames from which to drop columns.
    :param cols2drop: Column name (string) to drop from DataFrames.
    :param inplace: The option whether or not to perform the column drop in place. If True, the original DataFrames
        are modified. If false, a new list of DataFrames with the specified columns dropped is returned, and the
        original DataFrames are preserved.
    :return: nothing
    """
    # Check data types to prevent errors in column dropping loop.
    _ec.check_ls(ls=df_ls)
    _ec.check_ls(ls=cols2drop)
    _ec.check_dfs(values=df_ls)
    _ec.check_string(values=cols2drop)

    if not inplace:
        df_dropped_ls = []
    for df, df_num in zip(df_ls, range(len(df_ls))):
        cols_dropped = 0
        if not inplace:
            df_dropped = df.copy(deep=True)
        for col in cols2drop:
            if col in df.columns:
                if inplace:
                    df.drop(col, axis=1, inplace=inplace)
                    cols_dropped += 1
                else:
                    df_dropped = df_dropped.drop(col, axis=1, inplace=inplace)
                    cols_dropped += 1
            else:
                print('Column %s not present in DataFrame # %i. Proceeding to next in list.' % (col, df_num))
        if not inplace:
            df_dropped_ls.append(df_dropped)
        print('Number of columns dropped from DataFrame #%i: %i' % (df_num, cols_dropped))
    if inplace:
        return 0
    else:
        return df_dropped_ls


def norm_by_factors(df_ls, factor_ls=[0.0]):
    """
    This function takes in a list of pandas DataFrames and normalizes each column by a list of normalization factors.
        The list of factors and DataFrames must be of equal length. Otherwise, an error is returned using the external
        function _ec.check_eq_ls_len, which is called from _err_check.py. The normalization factors should be paired to the
        same indices as the DataFrames you wish to be normalized by each factor. For example, it will normalize
        df_ls[0] by factor_ls[0], ... df_ls[n] by factor_ls[n].
    Parameters:
    :param df_ls: List of pandas DataFrames for which you wish the columns to be normalized.
    :param factor_ls: List of normalization factors by which you wish to normalize the columns of the DataFrames in
        df_ls
    :return: df_ls_out: A list of the normalized DataFrames. The passed list of DataFrames is unchanged unless
        over-written by the returned list in the script from which this function is called.
    """
    # Check for equal length of passed lists and data types to prevent error in normalization loop.
    _ec.check_ls(ls=df_ls)
    _ec.check_ls(ls=factor_ls)
    _ec.check_eq_ls_len(list_ls=[df_ls, factor_ls])
    _ec.check_dfs(values=df_ls)
    _ec.check_numeric(values=factor_ls)

    df_ls_out = df_ls.copy()
    for df_in, factor, df_out, df_num in zip(df_ls, factor_ls, df_ls_out, range(len(df_ls))):
        for col in range(0, len(df_in.columns)):
            df_out.ix[:, col] = df_in.ix[:, col] / factor
    return df_ls_out


def df_col_avg_sum(df_ls, df_name_ls=[]):
    """
    This function takes a list of DataFrames, sums the columns, and then averages the sums of all columns to
        calculate one "average sum" value for each DataFrame. Then, a list of averaged column sums from all processed data
        frames is compiled into a new pandas DataFrame and returned. One example usage would be if a primary dataset
        was split into multiple subsets, and a comparison of the average sum of columns is desired.

    Parameters:
    :param df_ls: List of pandas DataFrames
    :param df_name_ls: A string list of DataFrame names (i.e., data set string labels)
    :return: df_out: A compiled DataFrame of original DataFrame names (column 1), and the average of column sums (col 2)
        each DataFrame
    """
    # Check for equal length of DataFrame list and factor list to prevent error in averaging/summing loop
    _ec.check_ls(ls=df_ls)
    _ec.check_ls(ls=df_name_ls)
    _ec.check_eq_ls_len(list_ls=[df_ls, df_name_ls])
    _ec.check_dfs(values=df_ls)
    _ec.check_string(values=df_name_ls)

    avgsums = []
    for df, df_name, df_num in zip(df_ls, df_name_ls, range(len(df_ls))):
        avgsum = df.sum(axis=0).mean(axis=0)
        avgsums.append(avgsum)
    # Create single DataFrame with average sums of each DataFrame in the first column.
    df_out = pd.DataFrame({"Dataset Name": df_name_ls,
                           "Mean of Column Sums": avgsums})
    return df_out


def find_min_rows(df_ls, max_len=99999999999):
    """
    This function finds the smallest number of rows in a pandas DataFrame from those present in a list of DataFrames,
        df_ls. This minimum number of rows can then be used to

    Parameters:
    :param df_ls: list of pandas DataFrames in which to find the minimum number of rows in the set.
    :param max_len: The maximum number of rows in DataFrames. If all DataFrames have more than max_len rows, then the
        returned min_rows = max_len
    :return: nrows_min: The number of rows in the DataFrame with the smallest number of rows.
    """
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_int(values=[max_len])

    nrows_min = max_len
    for df in df_ls:
        if df.shape[0] < nrows_min:
            nrows_min = df.shape[0]
        else:
            pass
    return nrows_min


def truncate_dfs(df_ls, min_rows=1000):
    """
    This function takes a list of pandas DataFrames and truncates them to the number of rows specified by parameter
        min_rows. By default, it truncates the DataFrames to 1000 rows.

    Parameters:
    :param df_ls: List of pandas DataFrames which will be truncated.
    :param min_rows: The number of rows to truncate each DataFrame to.
    :return: Nothing. The original DataFrames are modified in-place.
    """
    # Check that data types are those expected.
    _ec.check_ls(ls=df_ls)
    _ec.check_int(values=[min_rows])
    _ec.check_dfs(values=df_ls)

    for df in df_ls:
        cut = df.shape[0] - min_rows
        if cut > 0:
            df.drop(df.index[-cut:], inplace=True)
        else:
            pass
    return 0


def dropna_df_ls(df_ls, axis=0, rm_method='any', inplace=True):
    """
    This function works as a wrapper to the built in pandas DataFrame.dropna(), performing dropna on each member of a
        list of DataFrames. Dropna is performed along axis 0 (row dimension for a 2D df) and NaNs are dropped in place
        by default, such that the original DataFrames are modified. If

    Parameters:
    :param df_ls: List of pandas DataFrames on which the DataFrame.dropna() function is
    :param axis: axis along which to search for nans. Corresponds to the value used for the 'axis' keyword in
        the pandas DataFrame.dropna().
    :param rm_method: Corresponds to the value for the keyword 'how' in the pandas DataFrame.dropna().
    :param inplace: A choice whether to drop nans in place or to return a copy of the list of DataFrames with the
        nans removed as specified by axis and rm_method.
    :return: If inplace == True, DataFrames are modified in place, and nothing is returned. Otherwie, df_no_nan_ls
        is returned, which is a list of the DataFrames with nans removed as specified by axis and rm_method parameters.
    """
    # Check to verify parameter inputs are correct types to avoid pandas errors downstream
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_bool(values=[inplace])
    _ec.param_exists_in_set(value=axis, val_set=[0, 1])
    _ec.param_exists_in_set(value=rm_method, val_set=['any', 'all'])
    _ec.param_exists_in_set(value=inplace, val_set=[True, False])

    df_no_nan_ls = []
    for df in df_ls:
        print('shape before dropna:', df.shape)
        if inplace:
            df.dropna(axis=0, how=rm_method, inplace=inplace)
        else:
            df_dropna_temp = df.dropna(axis=0, how=rm_method, inplace=inplace)
            df_no_nan_ls.append(df_dropna_temp)
        print('shape after dropna:', df.shape)
    if inplace:
        return 0
    else:
        return df_no_nan_ls


def set_indices_ls(df_ls, index_name=''):
    """
    This function takes a list of pandas DataFrames and sets the index to a specified column. The specified
        column should exist in every DataFrame. Otherwise, the results may be inconsistent and some DataFrames
        may not have their index set to that which is specified.

    Parameters:
    :param df_ls: List of pandas DataFrames for which to attempt reindexing with the specified column.
    :param index_name: The user-specified column to reassign as the index of each pandas DataFrame in df_ls.
    :return: Nothing. DataFrames are modified in place.
    """
    # TODO: test the functionality of this function.
    # Input type checking to prevent errors during index setting.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_string(values=[index_name])

    for df, df_num in zip(df_ls, range(0, len(df_ls))):
        if index_name in df.columns:
            df.set_index(index_name, inplace=True)
        else:
            print("Target index not found in current DataFrame (#%i in list). Skipping re-indexing"
                  "of current DataFrame." % df_num)

    return 0


def top_series_mean_ls(df_ls, n_series=10):
    """
    This function takes a list of pandas DataFrames as input and then selects the top [n_series] series
        (i.e., columns) for each DataFrame, based on the average value of the column over all indices.
        A smaller DataFrame with [n_series] number of columns is returned for each DataFrame in the list.
        The function was initially written for DataFrames containing time series, but could work for any
        index if the average of column values are comparable on the same scale. Otherwise, the results may
        not make sense in the context of the data being processed.

    Parameters:
    :param df_ls: A pandas DataFrame in which the
    :param n_series: The user-specified number of time series to choose as the 'top' time series; that is, the time
        series with the top [n_series] average values in the set.
    :return:df_top_ls: The returned pandas DataFrame that is a subset of the original DataFrame and contains [n_series]
        columns with the highest averages (on a column-wise basis) in the original set.
            :max_idx_list: The indices of the maximum average values, as found in df_avg, the average values of the
        columns in the original DataFrame.
    """
    print("Picking the top %i time series by mean column values for %i DataFrames" % (n_series, len(df_ls)))
    # Check input types to prevent errors in subsequent loops.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_int(values=[n_series])

    # Create list of indices (columns) that contain the n_series highest average values in order
    # to later make the returned df_top DataFrame.
    df_top_ls = []
    max_idx_ls_all = []
    for df in df_ls:
        max_idx_list = []
        df_avg = df.mean(axis=0)
        # Loop through the averaged DataFrame, dropping each maximum idx after adding that idx to a list.
        for i in range(0, n_series):
            max_idx_list.append(df_avg.idxmax())
            df_avg.drop(df_avg.idxmax(), axis=0, inplace=True)
        # Create df_top from max_idx_list to pick the n_series top columns, based on mean values.
        # df_top = df.ix[:, max_idx_list]
        # Append to lists that are to be returned.
        df_top_ls.append(df.ix[:, max_idx_list])
        max_idx_ls_all.append(max_idx_list)

    return df_top_ls, max_idx_ls_all


def top_series_max_ls(df_ls, n_series=10):
    """
    This function takes a list of pandas DataFrames as input and then selects the top [n_series] series
        (i.e., columns) for each DataFrame, based on the average value of the column over all indices.
        A smaller DataFrame with [n_series] number of columns is returned for each DataFrame in the list.
        The function was initially written for DataFrames containing time series, but could work for any
        index if the average of column values are comparable on the same scale. Otherwise, the results may
        not make sense in the context of the data being processed.
    Parameters:
    :param df_ls: A pandas DataFrame in which the
    :param n_series: The user-specified number of time series to choose as the 'top' time series; that is, the time
        series with the top [n_series] average values in the set.
    :return:df_top_ls: The returned pandas DataFrame that is a subset of the original DataFrame and contains [n_series]
        columns with the highest averages (on a column-wise basis) in the original set.
            :max_idx_list: The indices of the maximum average values, as found in df_avg, the average values of the
        columns in the original DataFrame.
    """
    print("Picking the top %i time series by maximum column values for %i DataFrames" % (n_series, len(df_ls)))
    # Check input types to prevent errors in subsequent loops.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_int(values=[n_series])

    # Create list of indices (columns) that contain the n_series highest average values in order
    # to later make the returned df_top DataFrame.
    df_top_ls = []
    max_idx_ls_all = []
    for df in df_ls:
        max_idx_list = []
        df_max = df.max(axis=0)
        # Loop through average DataFrame to find the top n_series indices, based on maximum values.
        for i in range(0, n_series):
            # max_idx = df_max.idxmax()
            max_idx_list.append(df_max.idxmax())
            df_max.drop(df_max.idxmax(), axis=0, inplace=True)
        # Create df_top to return, along with the indices labels of the maximum average values.
        # df_top = df.ix[:, max_idx_list]
        # Append to list of top DataFrames and list-of-list of top indices for each DataFrame to return.
        df_top_ls.append(df.ix[:, max_idx_list])
        max_idx_ls_all.append(max_idx_list)

    return df_top_ls, max_idx_ls_all


def top_series_quantile_ls(df_ls, quant=0.75):
    """
    This function uses the function top_series_quantile from df_utils.py, but applies it to each DataFrame in a lst
        of pandas DataFrames. This will select the columns in a DataFrame whose mean values are above the [quant]
        quantile of the user DataFrame, as determined by the pandas.DataFrame.quantile method once the columns have
        been averaged along the index axis. The percentile is determined individually for each DataFrame processed.

    Parameters:
    :param df_ls: A list of pandas DataFrames from which the [quant]x100th percentile of columns will be pulled.
    :param quant: The percentile at which to select only those columns whose mean value is greater.
    :return: df_percentile_ls: A list of pandas DataFrames of length len(df_ls), which are comprised of only the
        those columns whose values are above the [quant] percentile.
    """
    # Check data types to prevent errors during quantile selection
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    _ec.check_numeric(values=[quant])
    _ec.check_threshold(values=[quant], thresh=1.0, how='under')

    # Create list to put the quantile/percentile DataFrames into
    df_percentile_ls = []
    for df_idx in range(0, len(df_ls)):
        df_percentile_ls.append(top_series_quantile(df=df_ls[df_idx], quant=quant))     # Append quantile df to new list

    return df_percentile_ls


def concat_ls(df_ls1, df_ls2, axis=0, join='inner'):
    """
    This function takes two lists of pandas DataFrames and concatenates them. Options allow user to specify the axis
        along which to concatenate as well as the pandas join method (e.g., 'inner', 'outer'). Where available,
        inherent pandas DataFrame functionality is employed (e.g., transpose, axis selection, join method, etc).
        Parameter choice should be in line with the requirements of the pandas library and associated functions,
        and therefore the same convention is used for parameters axis and join. DataFrames are concatenated pairwise;
        that is, df_ls1[i] is concatenated with df_ls2[i].

    Parameters:
    :param df_ls1: A list of DataFrames on which to concatenate df_ls2
    :param df_ls2: A list of DataFrames to concatenate onto the corresponding DataFrames
    :param axis: The axis along which the DataFrames will be concatenated. axis=1 for column-wise, 0 for row-wise
        (standard pandas DataFrame syntax). Example: if axis=0, DataFrames will be concatenated in the row dimension
        (i.e., stacked vertically; will require same # of columns).  If axis=1, will be concatenated in the
        column dimension (i.e., side-by-side)
    :param join: Allows user to specify the join parameter for pandas.concat(). Must be compatible with choices
        available within the pandas package.
    :return: df_list: A list of DataFrames where elements are DataFrames from list 1 concatenated onto the corresponding
        DataFrame from list 2
    """
    # Check data types to prevent errors during processing.
    _ec.check_ls(ls=df_ls1)
    _ec.check_ls(ls=df_ls2)
    _ec.check_dfs(values=df_ls1)
    _ec.check_dfs(values=df_ls2)
    _ec.check_eq_ls_len(list_ls=[df_ls1, df_ls2])
    _ec.check_numeric(values=[axis])
    _ec.param_exists_in_set(value=axis, val_set=[0, 1])
    _ec.check_string(values=[join])
    _ec.param_exists_in_set(value=join, val_set=['inner', 'outer'])

    # Initialize return list for concatenated DataFrames
    df_ls_concat = []
    # Check row or column lengths of lists to make sure they're the same.  If not, tell user, but try to proceed.
    if axis == 0:
        for df1, df2 in zip(df_ls1, df_ls2):
            if df1.shape[1] != df2.shape[1]:
                print('WARNING: You chose concatenation in row dimension (i.e., vertical stacking) with '
                      'parameter axis=0,\n but some DataFrame pairs have different numbers of columns.  Proceeding...')
            else:
                pass
    elif axis == 1:
        for df1, df2 in zip(df_ls1, df_ls2):
            if df1.shape[0] != df2.shape[0]:
                print('WARNING: You chose to concatenate in column dimension (side-by-side) with axis=1, but'
                      'some DataFrame pairs have different number of rows.  Proceeding...')
    else:
        print('ERROR: Parameter axis must be set to 0 or 1')
        sys.exit()

    for df1, df2 in zip(df_ls1, df_ls2):
        df_ls_concat.append(pd.concat([df1, df2], axis=axis, join=join))

    return df_ls_concat


def concat_trans_ls(df_ls1, df_ls2, axis=0, join='inner', pad=True, rep_colnames=True, pad_name=''):
    """
    This function takes two lists of pandas DataFrames and concatenates them, after transposing the second.
        Options allow user to specify the axis along which to concatenate as well as the pandas join method
        (e.g., 'inner', 'outer'). Where available, inherent pandas DataFrame functionality is employed
        (e.g., transpose, axis selection, join method, etc). Parameter choice should be in line with the requirements
        of the pandas library and associated functions, and therefore the same convention is used for parameters
        axis and join. DataFrames are concatenated pairwise; that is, df_ls1[i] is concatenated with df_ls2[i].
        Additional options are available through the parameters rep_colnames, pad, and padName

        Note, when using this that you will likely run into pandas errors if the transposed version of the second
        DataFrame has a different number of columns than the corresponding DataFrame in df_ls1.

    Parameters:
    :param df_ls1: list of DataFrames on which to concatenate the second list, df_ls2
    :param df_ls2: list of DataFrames to transpose and concatenate
    :param axis: axis=1 for columns, 0 for rows (standard pandas DataFrame syntax). Ex: if axis=0, DataFrames will
        be concatenated in the row dimension (i.e., stacked; may require same # of columns). If axis=1, will be
        concatenated in the column dimension (i.e., side-by-side)
    :param join: Join method a used by pandas.concat
    :param pad: Lets the user select whether or not to pad the two datasets with a blank row.  Can specify column
            name to add to this blank row with parameter pad_name.
    :param pad_name: optional info to add by user to name the padded row added between the datasets. leave blank for
            an empty index (nan).
    :param rep_colnames: option to replicate the column names after the padding.  This will add the column names from
        the first DataFrame into the padding between the two concatenated DataFrames
    :return: df_concat_ls - list of DataFrames where elements are DataFrames from list 1 concatenated onto the DataFrame
     from list 1
    """
    # Check parameter data types, list lengths, and values to prevent errors during processing
    _ec.check_ls(ls=df_ls1)
    _ec.check_ls(ls=df_ls2)
    _ec.check_dfs(values=df_ls1)                    # DataFrame lists
    _ec.check_dfs(values=df_ls2)
    _ec.check_eq_ls_len(list_ls=[df_ls1, df_ls2])
    _ec.check_numeric(values=[axis])                # axis
    _ec.param_exists_in_set(value=axis, val_set=[0, 1])
    _ec.check_bool(values=[pad])
    _ec.check_bool(values=[rep_colnames])
    _ec.check_string(values=[pad_name])

    # Initialize internal function variables and return list
    df_concat_ls = []
    # check row or column lengths of lists to make sure they're the same.  If not, tell user, but try to proceed
    if axis == 0:
        for df1, df2 in zip(df_ls1, df_ls2):
            if df1.shape[1] != df2.T.shape[1]:
                print('WARNING: You chose concatenation in row dimension (i.e., stacking) with parameter axis=0,\n'
                      'but some DataFrame pairs have different numbers of columns.  Proceeding...')
            else:
                pass
    elif axis == 1:
        for df1, df2 in zip(df_ls1, df_ls2):
            if df1.shape[0] != df2.T.shape[0]:
                print('WARNING: You chose to concatenate in column dimension (side by side) with axis=1, but'
                      'some DataFrame pairs have different number of rows.  Proceeding...')
    else:
        print('ERROR: Parameter axis must be set to 0 or 1')
        sys.exit()

    # Proceed with concatenation
    for df1, df2 in zip(df_ls1, df_ls2):
        # Create pad row if selected, and pad b/t the two DataFrames in current pair
        if pad:
            padding = pd.DataFrame(index=['', pad_name], columns=df1.columns)
            if rep_colnames:
                padding.values[1] = df1.columns.values
            else:
                pass
            df_concat_ls.append(pd.concat([df1, padding, df2.T], axis=axis, join=join))
        else:
            df_concat_ls.append(pd.concat([df1, df2.T], axis=axis, join=join))
    return df_concat_ls


def norm_cols_each_ls(df_ls):
    """
    This function takes a list of pandas DataFrames and normalizes columns to the maximum absolute value in each column,
        resulting in values ranging -1 to 1. This was originally designed for normalizing multiple time series within
        a DataFrame to a maximum of 1 so that they can be plotted on the same scale for qualitative comparison.
        You may encounter an error if non-numeric values are present in the DataFrame.

    Parameters:
    :param df_ls: A list of pandas DataFrames containing the columns to be normalized.
    :return: df_norm_ls: A list of new DataFrames with each column normalized to its maximum value. Values will be
        in the range -1 to 1.
    """
    # Check for correct data type of df (pandas.DataFrame) to prevent subsequent errors.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)

    df_norm_ls = []
    for df in df_ls:
        df_norm = df.copy(deep=True)
        for col in df.axes[1]:
            max_abs_val = max(abs(df[col].max()), abs(df[col].min()))
            df_norm[col] = df_norm[col] / max_abs_val
        df_norm_ls.append(df_norm)

    return df_norm_ls


def norm_cols_all_ls(df_ls):
    """
    This takes a list of pandas DataFrames and normalizes each column to the maximum absolute value in all columns,
        resulting in values ranging -1 to 1. This was originally designed for normalizing multiple time series within
        a DataFrame to a maximum of 1 so that they can be plotted on the same scale for qualitative comparison.
        You may encounter an error if non-numeric values are present in the DataFrame.

    Parameters:
    :param df_ls: A list of pandas DataFrames in which to normalize the columns.
    :return: df_norm_ls: A new pandas DataFrame with the normalized columns in it.
             max_in_all_ls: A list of the maximum values present in all columns in each DataFrame.
    """
    # Check df type (expected: pandas DataFrame) to prevent errors during normalization.
    _ec.check_ls(ls=df_ls)
    _ec.check_dfs(values=df_ls)
    
    df_norm_ls = []
    max_abs_val_ls = []
    for df in df_ls:
        max_abs_val = max(abs(df.values.max()), abs(df.values.min()))
        df_norm = df / max_abs_val
        df_norm_ls.append(df_norm)
        max_abs_val_ls.append(max_abs_val)
        
    return df_norm_ls, max_abs_val_ls
