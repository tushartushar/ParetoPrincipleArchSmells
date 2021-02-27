import glob
import os
import re
from collections import Counter

import pandas as pd
from pandas.errors import EmptyDataError

# Setting option to hide warnings
pd.options.mode.chained_assignment = None


### Read csv file and create pandas DataFrame
def read_file(filePath, columnList, duplicateFlag=True):
    if os.path.exists(filePath):
        try:
            dataFrame = pd.read_csv(filePath, usecols=columnList) ### .fillna(value = 'Empty_cell')
            dataFrame = dataFrame.dropna()
            if not dataFrame.empty:
                if duplicateFlag:
                    return dataFrame
                else:
                    return dataFrame.drop_duplicates()
            else:
                return None
        except EmptyDataError:
            return None
    else:
        return None


def aggregation_function(x):
    d = {}
    d['Count namespaces'] = x['Combination'].nunique()
    d['Sum LOC'] = x['LOC'].sum()
    d['Average LOC'] = x['LOC'].mean()

    return pd.Series(d, index=['Count namespaces', 'Sum LOC', 'Average LOC'])


### Parse repo to calculate metrics
def analyze_repository(repositoryPath, projectList):
    namespaceList = []
    metricsList = []

    for project in projectList:
        projectPath = os.path.join(repositoryPath, project)
        namespaceRaw = read_file(projectPath + r'_NamespaceMetrics.csv', ['Namespace'], False)
        if namespaceRaw is not None:
            ## Filter test/sample packages
            namespaceRaw = namespaceRaw[
                namespaceRaw['Namespace'].str.contains('test|sample', flags=re.IGNORECASE, regex=True) == False]

            namespaceList.append(namespaceRaw)

        metricsRaw = read_file(projectPath + r'_ClassMetrics.csv', ['Namespace', 'Type', 'LOC'], True)
        if metricsRaw is not None:
            metricsRaw = metricsRaw[
                metricsRaw['Namespace'].str.contains('test|sample', flags=re.IGNORECASE, regex=True) == False]

            metricsRaw.insert(0, 'Project', project)
            metricsRaw['Combination'] = metricsRaw['Project'] + metricsRaw['Namespace']
            metricsList.append(metricsRaw)


    repoName = os.path.basename(os.path.dirname(projectPath))
    namespaceData = pd.concat(namespaceList).drop_duplicates()
    namespaceData.insert(0, 'Repository', repoName)

    metricsData = pd.concat(metricsList).drop_duplicates()
    metricsData.insert(0, 'Repository', repoName)

    groupbyDataset = metricsData.groupby(['Repository']).apply(aggregation_function)
    groupbyDataset.reset_index(level=0, inplace=True)

    categories = category_file
    categoriesData = read_file(categories,
                            ['Project', 'Pareto category'], True)

    finalDataset = pd.merge(groupbyDataset, categoriesData, left_on='Repository', right_on='Project', how='left')
    del finalDataset['Project']

    return finalDataset


### Export results to csv [mode: appending]
def export_data(dataFrame, outputFile, headerFlag):
    dataFrame.to_csv(outputFile, header=headerFlag, index=False, mode='a')


### Parse all repos in a directory
def parse_repositories():

    with open(output_file, 'w') as writer:
        writer.write('Repository Name,Count namespaces,Sum LOC,Average LOC,Pareto category\n')

    for folder in [f for f in glob.glob(project_path + '**/**/', recursive=True)]:
        projectList = []
        for file in os.listdir(folder):
            if file.endswith('_NamespaceMetrics.csv'):
                project = file.rsplit('_', 1)[0]
                if project not in projectList:
                    projectList.append(project)

        if len(projectList) != 0:
            print('Analyzing repository: ' + os.path.basename(os.path.dirname(folder)))
            finalDataset = analyze_repository(folder, projectList)
            if finalDataset is not None:
                if 'Sum LOC' in finalDataset:
                    finalDataset = finalDataset[finalDataset['Sum LOC'] >= 1000]
                export_data(finalDataset, output_file, False)
            else:
                # logList.append(folder)
                print('Error in exporting data from path: ' + folder)

# Define variables
project_path = r'/path/data/designite_out'
output_file = r'/path/data/results/boxplot_cs.csv'
category_file = r'/path/data/results/pareto_cs.csv'

if __name__ == "__main__":
    parse_repositories()
