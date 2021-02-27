import os
import re

import pandas as pd
from pandas.errors import EmptyDataError

### Read csv file and create pandas DataFrame
def read_file(filepath, column_list, duplicate_flag=True):
    if os.path.exists(filepath):
        try:
            data_frame = pd.read_csv(filepath, usecols=column_list, encoding='utf-8')
            if not data_frame.empty:
                if duplicate_flag:
                    return data_frame
                else:
                    return data_frame.drop_duplicates()
            else:
                return None
        except EmptyDataError:
            return None
        except UnicodeDecodeError:
            return None
    else:
        return None


def aggregation_function(x):
    d = {}
    d['Count packages'] = x['Package Name'].nunique()
    d['Sum LOC'] = x['LOC'].sum()
    d['Average LOC'] = x['LOC'].mean()

    return pd.Series(d, index=['Count packages', 'Sum LOC', 'Average LOC'])


### Export results to csv [mode: appending]
def export_data(dataFrame, outputFile, headerFlag):
    dataFrame.to_csv(outputFile, header=headerFlag, index=False, mode='a')


def parse_projects(path, out_file, category_file):
    with open(out_file, 'w') as writer:
        writer.write('Project Name,Count packages,Sum LOC,Average LOC,Pareto category\n')

    categoriesData = read_file(category_file,
                            ['Project', 'Pareto category'], True)

    for projectPath in os.listdir(path):
        cur_project_path = os.path.join(path, projectPath)
        if not os.path.isdir(cur_project_path):
            continue

        print('Analyzing project: ' + projectPath)

        packageData = read_file(os.path.join(cur_project_path, r'TypeMetrics.csv'),
                                ['Project Name', 'Package Name', 'LOC'], True)

        if packageData is not None:
            ## Filter test/sample packages
            packageData = packageData[
                packageData['Package Name'].str.contains('test|sample', flags=re.IGNORECASE, regex=True) == False]
            groupbyDataset = packageData.groupby(['Project Name']).apply(aggregation_function)
            groupbyDataset.reset_index(level=0, inplace=True)
            finalDataset = pd.merge(groupbyDataset, categoriesData, left_on='Project Name', right_on='Project', how='left')
            del finalDataset['Project']

            if finalDataset is not None:
                export_data(finalDataset, out_file, False)
        else:
            print('Error in exporting data from path: ' + cur_project_path)


parse_projects(r'/path/data/designitejava_out',
               r'/path/data/results/boxplot_java.csv',
               r'/path/data/results/pareto_java.csv')
