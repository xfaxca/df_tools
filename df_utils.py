# df_utils.py

# Module import
import df_tools._err_check as ec
import pandas as pd

__doc__ = "\n-------------------------------------------------------------------------\n" \
          "This module provide tools for functional manipulation of single pandas \n" \
          "DataFrames, such as normalization, reindexing, modification of index values,\n" \
          "column averaging/summing, etc. For functions that handle lists of DataFrames,\n" \
          "please use df_tools.list_utils.\n" \
          "\nFunctions:\n" \
          "idx0, avg_cols, avg_rows, drop_cols, top_series_mean, top_series_max,\n" \
          "top_series_quantile, norm_cols_each, norm_cols_all.\n\n" \
          "See doc strings of the individual functions for further information.\n" \
          "-------------------------------------------------------------------------\n"


def idx0(df):
    """
    This function subtracts the DataFrame's first index value from all values in the index. This was designed
        with the aim of create a "t_0" (or "time elapsed") time series - that is, a time series where the first
         time index is t = 0. This function does not account for units of time and subtracts the first index value
         from all other values in the index. Use is only suggested for DataFrames containing time series, but it
         should function with all numeric indices.

    Parameters:
    :param df: pandas DataFrame for which the index is to be offset.
    :return: pandas DataFrame with offset index.
    """
    # Check to make sure index values are numeric and in a pandas DataFrame.
    ec.check_dfs(values=[df])
    ec.check_numeric(values=df.index.values)
    df_idx0 = df.copy()
    df_idx0.index = (df.index.values - df.index.values[0])

    return df_idx0


def avg_cols(df):
    """
    This function averages the columns of a pandas DataFrame, and compiles the average values into a new DataFrame,
        df_avgs.

    Parameters:
    :param df: pandas DataFrame for which you wish to average the columns
    :return: df_avgs: A 2 column DataFrame, with the original DataFrame's column names as the index, and the average
        column values in the first column, 'Averages'
    """
    # Check to make sure passed object is a pandas DataFrame
    ec.check_dfs(values=[df])

    df_avgs = pd.DataFrame({'Averages': df.mean(axis=0)},
                           index=df.columns.values)
    return df_avgs


def avg_rows(df):
    """
    This function averages the rows of a pandas DataFrame and compiles the average values into a new DataFrame, df_avgs.

    Parameters:
    :param df: pandas DataFrame for which you wish to average the rows
    :return: df_avgs: A 2 column DataFrame with the original DataFrame's row names as the index and the average
        column values in the first column, Averages.
    """
    # check to make sure the passed object is a pandas DataFrame
    ec.check_dfs(values=[df])

    df_avgs = pd.DataFrame({'Averages': df.mean(axis=1)},
                           index=df.column.values)

    return df_avgs


def drop_cols(df, cols2drop=[""]):
    """
    This function drops a list of columns from a pandas DataFrame.

    Parameters:
    :param df: DataFrame from which to drop columns
    :return:
    """
    # Check data types to prevent errors in column dropping loop.
    ec.check_ls(ls=cols2drop)
    ec.check_dfs(values=[df])
    ec.check_string(values=cols2drop)

    cols_dropped = 0
    for col in cols2drop:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
            cols_dropped += 1
        else:
            pass
    print('Number of columns dropped from DataFrame: %i' % cols_dropped)

    return 0


def top_series_mean(df, n_series=10):
    """
    This function takes a pandas DataFrame as input and then selects the top [n_series] series (i.e., columns),
        based on the average value of the column over all indices. A smaller DataFrame with [n_series] number of
        columns is returned. The function was initially written for DataFrames containing time series, but could
        work for any index if the average of column values are comparable on the same scale. Otherwise, the results
        may not make sense in the context of the data being processed.

    Parameters
    :param df: A pandas DataFrame from which the series with the highest values, by column mean, are returned.
    :param n_series: The user-specified number of time series to choose as the 'top' time series; that is, the time
        series with the top [n_series] average values in the set.
    :return:df_top: The returned pandas DataFrame that is a subset of the original DataFrame and contains [n_series]
        columns with the highest averages (on a column-wise basis) in the original set.
            :max_idx_list: The indices of the maximum average values, as found in df_avg, the average values of the
        columns in the original DataFrame.
    """
    # Check input types to prevent errors in subsequent loops.
    ec.check_dfs(values=[df])
    ec.check_int(values=[n_series])

    # Create list of indices (columns) that contain the n_series highest average values in order
    # to later make the returned df_top DataFrame.
    max_idx_list = []
    df_avg = df.mean(axis=0)

    for i in range(0, n_series):
        max_idx_list.append(df_avg.idmax())
        df_avg.drop(df_avg.idmax(), axis=0, inplace=True)

    # Create df_top to return, along with the indices labels of the maximum average values.
    df_top = df.ix[:, max_idx_list]

    return df_top, max_idx_list


def top_series_max(df, n_series=10):
    """
    This function takes a pandas DataFrame as input and then selects the top [n_series] series (i.e., columns),
        based on the maximum value of the column over all indices. A smaller DataFrame with [n_series] number of
        columns is returned. The function was initially written for DataFrames containing time series, but could
        work for any index if the maximum of column values are comparable on the same scale. Otherwise, the results
        may not make sense in the context of the data being processed.

    Parameters:
    :param df: A pandas DataFrame in which the
    :param n_series: The user-specified number of time series to choose as the 'top' time series; that is, the time
        series with the top [n_series] maximum values in the set.
    :return:df_top: The returned pandas DataFrame that is a subset of the original DataFrame and contains [n_series]
        columns with the highest maximums (on a column-wise basis) in the original set.
            :max_idx_list: The indices of the maximum maximum values, as found in df_avg, the maximum values of the
        columns in the original DataFrame.
    """
    # Check input types to prevent errors in subsequent loops.
    ec.check_dfs(values=[df])
    ec.check_int(values=[n_series])

    # Create list of indices (columns) that contain the n_series highest maximum values in order
    # to later make the returned df_top DataFrame.
    max_idx_list = []
    df_max = df.max(axis=0)

    for i in range(0, n_series):
        max_idx = df_max.idxmax()
        max_idx_list.append(df_max.idxmax())
        df_max.drop(df_max.idxmax(), axis=0, inplace=True)

    # Create df_top to return, along with the indices labels of the maximum values.
    df_top = df.ix[:, max_idx_list]

    return df_top, max_idx_list


def top_series_quantile(df, quant=0.9):
    """
    This function takes a pandas DataFrame and returns the top [quant] quantile of the time series, based
        on the mean value of each column (averaged along index). Originally designed to find the [quantile] percentile
        of time series, based on average value, assuming that all time series units are on the same scale. Uses the
        pandas built-in method, 'df.quantile(percentile)' to find the [quant] percentile.

    Parameters:
    :param df: A pandas DataFrame, containing the time series from which those with the top [quant] percentile of
        mean values are selected and returned.
    :param quant: The quantile/percentile to select from the time series present in param df.
    :return: df_quant: The top [quant] percentile of time series (columns) from the original DataFrame, based on the
        mean values of the columns.
    """
    # Verify parameter of type pandas.DataFrame, there is a numeric value for quantile, and that quantile is <=1.0.
    ec.check_dfs(values=[df])
    ec.check_numeric(values=[quant])
    ec.check_threshold(values=[quant], thresh=1.0, how='under')
    # Take average of original DataFrame for processing and make a 'quant_index_list' to be able to create a new
    # returnable DataFrame from the original using a mask.
    quant_index_list = []
    df_proc = df.mean(axis=0)

    quantile = df_proc.quantile(quant)
    for i in df_proc.index:
        if df_proc[i] > quantile:
            quant_index_list.append(i)
        else:
            pass
    df_quant = df[quant_index_list]

    return df_quant


def norm_cols_each(df):
    """
    This function takes a pandas DataFrame and normalizes each column to the maximum absolute value in that column,
        resulting in values ranging -1 to 1. This was originally designed for normalizing multiple time series within
        a DataFrame to a maximum of 1 so that they can be plotted on the same scale for qualitative comparison.
        You may encounter an error if non-numeric values are present in the DataFrame.

    Parameters:
    :param df: Expected: A pandas DataFrame containing the columns to be normalized.
    :return: df_norm: A new DataFrame with each column normalized to its maximum value. Values will be in the range
        -1 to 1.
    """
    # Check for correct data type of df (pandas.DataFrame) to prevent subsequent errors.
    ec.check_dfs(values=[df])

    df_norm = df.copy(deep=True)
    for col in df.axes[1]:
        max_abs_val = max(abs(df[col].max()), abs(df[col].min()))
        df_norm[col] = df_norm[col] / max_abs_val
    return df_norm


def norm_cols_all(df):
    """
    This takes a pandas DataFrame and normalizes each column to the maximum absolute value present in all columns,
        resulting in values ranging -1 to 1. This was originally designed for normalizing multiple time series within
        a DataFrame to a maximum of 1 so that they can be plotted on the same scale for qualitative comparison.
        You may encounter an error if non-numeric values are present in the DataFrame.

    Parameters:
    :param df: pandas DataFrame in which to normalize the columns.
    :return: df_norm: A new pandas DataFrame with the normalized columns in it.
             max_in_all: The maximum value present in all columns.
    """
    # Check df type (expected: pandas DataFrame) to prevent errors during normalization.
    ec.check_dfs(values=[df])

    max_abs_val = max(abs(df.values.max()), abs(df.values.min()))
    df_norm = df / max_abs_val

    return df_norm, max_abs_val
