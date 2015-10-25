def RemoveColumns(columnsToRemove, resultsDf):
    columnsToRemove = set(resultsDf.columns).intersection(set(columnsToRemove))
    resultsDf = resultsDf.drop(columnsToRemove, 1) #drop and earnings country column
    resultsDf = resultsDf.reset_index(drop = True)
    return resultsDf

