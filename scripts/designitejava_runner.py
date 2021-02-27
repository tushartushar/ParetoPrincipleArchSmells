import os
import subprocess
from glob import glob
from subprocess import Popen, PIPE


# java -jar Designite.jar -i <path of the input source folder> -o <path of the output folder>

def _run_designite_java(folder_name, folder_path, designiteJava_jar_path, smells_results_folder):
    out_folder = os.path.join(smells_results_folder, folder_name)
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    # logfile = os.path.join(out_folder, "log.txt")
    proc = Popen(["java", "-jar", designiteJava_jar_path, "-i", folder_path, "-o", out_folder])
    proc.wait()


def _is_class_files_present(dir_path):
    result = [y for x in os.walk(dir_path) for y in glob(os.path.join(x[0], '*.class'))]
    if len(result) > 0:
        return True
    return False


def _build_project(dir, dir_path):
    print("Attempting compilation...")
    var = os.environ['JAVA_HOME']
    is_compiled = False
    pom_path = os.path.join(dir_path, 'pom.xml')
    if os.path.exists(pom_path):
        print("Found pom.xml")
        os.chdir(dir_path)
        proc = Popen([r'C:\Program Files (x86)\apache-maven-3.6.2\bin\mvn.cmd', 'clean', 'install', '-DskipTests'])
        proc.wait()
        is_compiled = True

    gradle_path = os.path.join(dir_path, "build.gradle")
    if os.path.exists(gradle_path):
        print("Found build.gradle")
        os.chdir(dir_path)
        proc = Popen([r'C:\Program Files\Gradle\gradle-5.6.2\bin\gradle.bat', 'compileJava'])
        proc.wait()
        is_compiled = True

    ant_path = os.path.join(dir_path, "build.xml")
    if os.path.exists(ant_path):
        print("Found build.xml")
        os.chdir(dir_path)
        proc = Popen([r'D:\ant\apache-ant-1.10.7\bin\ant.bat', 'compile'])
        proc.wait()
        is_compiled = True
    if not is_compiled:
        print("Did not compile")
        return False
    else:
        if _is_class_files_present(dir_path):
            return True
        return False


def analyze_repositories(repo_source_folder, smells_results_folder, designiteJava_jar_path):
    for dir_item in os.listdir(repo_source_folder):
        print("Processing " + dir_item)
        if os.path.exists(os.path.join(smells_results_folder, dir_item)):
            print("\t.. skipping.")
        else:
            if _build_project(dir_item, os.path.join(repo_source_folder, dir_item)):
                print("Analyzing project ...")
                _run_designite_java(dir_item, os.path.join(repo_source_folder, dir_item), designiteJava_jar_path,
                                    smells_results_folder)
            else:
                os.makedirs(os.path.join(smells_results_folder, dir_item))
                print("Could not compile or missing class files; skipping.")
    print("Done.")


if __name__ == "__main__":
    analyze_repositories(r'/path/data/all_java_repos_new',
                         r'/path/data/designitejava_out',
                         r'/path/DesigniteJava.jar')
