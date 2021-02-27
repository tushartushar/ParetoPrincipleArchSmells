# This script finds total number of arch smells as well as LOC from Java and C# analysis (produced by Designite)

import os
import re

import pandas as pd
from pandas.errors import EmptyDataError

arch_smells_list = ['Cyclic Dependency', 'Unstable Dependency', 'Ambiguous Interface',
                    'God Component', 'Feature Concentration', 'Scattered Functionality',
                    'Dense Structure']


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


def _get_arch_smell_count(cur_folder, lang):
    smell_dict = _init_dict()
    for file in os.listdir(cur_folder):
        columns = []
        if lang == 'java':
            arch_smell_str = 'Architecture Smell'
            columns = ['Project Name', 'Package Name', 'Architecture Smell', 'Cause of the Smell']
            if not file == 'ArchitectureSmells.csv':
                continue
        else:
            arch_smell_str = 'Architecture smell'
            columns = ['Architecture smell', 'Project', 'Namespace', 'Cause', 'Responsible Classes',
                       'Participating Classes']
            if not file.endswith('_ArchSmells.csv'):
                continue
        smell_filepath = os.path.join(cur_folder, file)
        if os.path.exists(smell_filepath):
            df = read_file(smell_filepath, columns)
            if not df is None:
                if lang == 'java':
                    ## Filter test/sample packages
                    df = df[df['Package Name'].str.contains('test|sample', flags=re.IGNORECASE,
                                                                 regex=True) == False]

                for smell_item in df.groupby(arch_smell_str):
                    rows, _ = smell_item[1].shape
                    smell_dict[smell_item[0]] += rows
    return smell_dict


def _get_loc(cur_folder, lang):
    total_loc = 0
    for file in os.listdir(cur_folder):
        if lang == 'java':
            if not file == 'TypeMetrics.csv':
                continue
        else:
            if not file.endswith('_ClassMetrics.csv'):
                continue
        metric_filepath = os.path.join(cur_folder, file)
        if os.path.exists(metric_filepath):
            df = read_file(metric_filepath, ['LOC'])
            if not df is None:
                total_loc += df.sum(axis=0)['LOC']
    return total_loc


def _add_arch_smells(cur_repo_smells_dict, total_arch_smells):
    for key in total_arch_smells:
        if key in cur_repo_smells_dict:
            total_arch_smells[key] += cur_repo_smells_dict[key]


def _init_dict():
    smell_dict = dict()
    for item in arch_smells_list:
        smell_dict[item] = 0
    return smell_dict


def _print_output(total_arch_smells, total_loc, lang):
    print('----Results for ' + lang + '-------')
    for item in arch_smells_list:
        print(item + ": " + str(total_arch_smells[item]))
    print("Total LOC: " + str(total_loc))


def analyze_results(designite_out_folderpath, lang='java'):
    total_arch_smells = _init_dict()
    total_loc = 0
    for folder in os.listdir(designite_out_folderpath):
        cur_folder = os.path.join(designite_out_folderpath, folder)
        if os.path.isdir(cur_folder):
            print('processing ' + folder)
            _add_arch_smells(_get_arch_smell_count(cur_folder, lang), total_arch_smells)
            total_loc += _get_loc(cur_folder, lang)
    _print_output(total_arch_smells, total_loc, lang)


if __name__ == "__main__":
    analyze_results(designite_out_folderpath=r'/path/data/designitejava_out', lang='java')
    # analyze_results(designite_out_folderpath=r'/path/data/designite_out', lang='cs')
