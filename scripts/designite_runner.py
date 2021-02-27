# -- imports --
import os
import subprocess
from glob import glob


# ----


def _get_all_csharp_projects_paths(folder):
    list = []
    if not os.path.exists(folder):
        return list

    result = [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.csproj'))]
    for prj in result:
        if not _get_repo_name(prj).__contains__("test"):
            list.append(prj)
    return list


def _get_repo_name(folder):
    start_index = folder.rfind(os.path.sep)
    if start_index + 1 < len(folder):
        return folder[start_index + 1:]
    else:
        return folder


def _write_batch_file(repo_name, project_paths, batch_files_folder):
    if not os.path.exists(batch_files_folder):
        os.makedirs(batch_files_folder)
    batch_file_name = os.path.join(batch_files_folder, repo_name + ".batch")
    if os.path.exists(batch_file_name):
        return batch_file_name
    try:
        with open(batch_file_name, "w", errors='ignore') as file:
            file.write("[Projects]\n")
            for line in project_paths:
                file.write(line + "\n")
    except:
        print("Error writing batch file: " + batch_file_name)
    return batch_file_name


def _analyze_projects(batch_file_path, repo_name, result_folder_base, designite_console_path, version=None):
    result_folder = os.path.join(result_folder_base, repo_name)
    if version is not None:
        result_folder = os.path.join(result_folder, version)
    if os.path.exists(result_folder):
        return
    os.makedirs(result_folder)
    subprocess.call([designite_console_path, batch_file_path, "-C", result_folder])


def analyze_repositories(repo_source_folder, batch_files_folder, result_folder_base, designite_console_path):
    for folder in os.listdir(repo_source_folder):
        print("Processing " + folder)

        if os.path.exists(os.path.join(result_folder_base, folder)):
            print("Skipping ...")
            continue
        project_paths = _get_all_csharp_projects_paths(os.path.join(repo_source_folder, folder))
        if len(project_paths) > 0:
            repo_name = _get_repo_name(folder)
            batch_file_path = _write_batch_file(repo_name, project_paths, batch_files_folder)
            _analyze_projects(batch_file_path, repo_name, result_folder_base, designite_console_path)
            print("Done with " + folder)


if __name__ == "__main__":
    analyze_repositories(repo_source_folder=r'/path/data/all_cs_repos',
                         batch_files_folder=r'/path/data/batch_files',
                         result_folder_base=r'/path/data/designite_out',
                         designite_console_path=r'C:\Program Files (x86)\Designite\DesigniteConsole.exe')
