# test_script.py

import pandas as pd
import numpy as np
import df_tools

__doc__ = "This is a test script to demonstrate some of the functionality of the df_tools package."


def main():
    """
    This script is included to quickly demonstrate some of the list functions in df_tools for handling lists
        of pandas DataFrames.
        Function examples include:
        1. Dropping a specified list of columns from each DataFrame
        2. Finding the minimum number of rows in a list of DataFrames and truncating all to the minimum number
            of rows.
        3. Concatenating the truncated list with the original DataFrames
    :return: Nothing.
    """

    # 0. Create a list of DataFrames for the purpose of this demonstration. DataFrames are 5 columns,
    df_ls = example_dfs()
    # List shapes of DataFrames
    for df, df_num in zip(df_ls, range(len(df_ls))):
        print('Shape of df #%i:' % df_num, df.shape)
    print('\n')

    # 1. Example 1: Dropping a list of columns from all DataFrames
    drop_cols = ['Col2', 'Col5']
    for df, df_num in zip(df_ls, range(len(df_ls))):
        print('df# %i: Columns before drop = ' % df_num, df.columns)
    df_dropped_cols_ls = df_tools.list_utils.drop_cols_df_ls(df_ls=df_ls, cols2drop=drop_cols, inplace=False)
    for df, df_num in zip(df_dropped_cols_ls, range(len(df_dropped_cols_ls))):
        print('df# %i: Columns after drop = ' % df_num, df.columns)

    # Example 2: Find minimum number of rows in a list of DataFrames:
    min_rows = df_tools.list_utils.find_min_rows(df_ls=df_ls, max_len=10000)
    print('\nMinimum # of rows in set:', min_rows)
    # 2b. Truncate all DataFrames to the minimum row number of all DataFrames
    df_ls2 = example_dfs()
    for df, df_num in zip(df_ls2, range(len(df_ls2))):
        print('Shape of DataFrame #%i before truncation:' % df_num, df.shape)
    # df_tools.list_utils.truncate_dfs(df_ls=df_ls_trunc, min_rows=min_rows)
    df_tools.list_utils.truncate_dfs(df_ls=df_ls2, min_rows=min_rows)
    for df, df_num in zip(df_ls2, range(len(df_ls2))):
        print('Shape of DataFrame #%i after truncation:' % df_num, df.shape)

    # Example 3: Pair-wise concatenation of the truncated DataFrames with the original DataFrames
    df_ls_concat = df_tools.list_utils.concat_ls(df_ls1=df_ls, df_ls2=df_ls2, axis=0, join='inner')
    print('\n')
    for df, df_num in zip(df_ls_concat, range(len(df_ls_concat))):
        print('Shape of concatenated DataFrame #%i:' % df_num, df.shape)

    return 0


def example_dfs():
    """
    This function creates a list of pandas DataFrames for demonstration of the functions in df_tools
    :return: df_ls: A list of DataFrames intended for use in df_tools examples within test_script.py
    """
    # Column names for random df
    colnames = ['Col1', 'Col2', 'Col3', 'Col4', 'Col5']
    # Lists for trig functions
    x = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    x2 = [30, 60, 90, 120, 0, 240, 270, 300, 150, 180, 210, 330]
    x3 = [120, 0, 30, 90, 60, 270, 240, 300, 180, 150, 330, 210]
    x4 = [60, 90, 30, 0, 180, 120, 150, 330, 300, 360, 270, 210]
    x5 = [330, 300, 270, 240, 210, 180, 150, 120, 90, 60, 30, 0]
    x_ls = [x, x2, x3, x4, x5]
    y_ls = repeat_multi_ls(ls_of_ls=x_ls, iterations=10)

    # Random number df with 150 columns
    df_rand = pd.DataFrame(abs(np.random.randn(150, 5) * 1000), columns=colnames)
    # Sine df with 120 columns
    df_sin = pd.DataFrame(data={"Col1": np.sin(y_ls[0]) * 1,
                                "Col2": np.sin(y_ls[1]) * 2,
                                "Col3": np.sin(y_ls[2]) * 3,
                                "Col4": np.sin(y_ls[3]) * 4,
                                "Col5": np.sin(y_ls[4]) * 5})
    # Cosine df with 120 columns
    df_cos = pd.DataFrame(data={"Col1": np.cos(y_ls[0]) * 4,
                                "Col2": np.cos(y_ls[1]) * 3,
                                "Col3": np.cos(y_ls[2]) * 5,
                                "Col4": np.cos(y_ls[3]) * 1,
                                "Col5": np.cos(y_ls[4]) * 2})
    # Tangent df with 120 columns
    df_tan = pd.DataFrame(data={"Col1": np.tan(y_ls[0]) * 5,
                                "Col2": np.tan(y_ls[1]) * 1,
                                "Col3": np.tan(y_ls[2]) * 2,
                                "Col4": np.tan(y_ls[3]) * 4,
                                "Col5": np.tan(y_ls[4]) * 3})

    df_ls = [df_rand, df_sin, df_cos, df_tan]

    return df_ls


def repeat_multi_ls(ls_of_ls=[], iterations=2):
    """
    This function extends multiple lists by repeating each list and appending it to the end of the original lists. This
        is performed iterations number of times.
    :param ls_of_ls: A list of lists for which the repretition/extension is to be performed
    :param iterations: The number of iterations by which to repeat each list in ls_of_ls
    :return: ls_of_ls_new: A new list of lists wherein each member list corresponds to the list in ls_of_ls at the
        same index. Each list will be extended by repetitions of itself and will have a length of
        iterations*len(ls_of_ls[i]) for list i.
    """
    ls_of_ls_new = []
    for ls in ls_of_ls:
        new_ls_tmp = []
        for iter in range(iterations):
            for element in ls:
                new_ls_tmp.append(element)
                # print('y_tmp is now:', y_tmp)
        ls_of_ls_new.append(new_ls_tmp)

    return ls_of_ls_new

if __name__ == "__main__":
    main()
else:
    pass
