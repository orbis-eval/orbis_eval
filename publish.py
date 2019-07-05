import io
import re
import os
import shutil
from pathlib import PurePath
from packaging import version
from glob import glob


def remove(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


def get_pkg_name():
    directory = os.path.dirname(os.path.realpath(__file__))
    path_split = PurePath(directory).parts
    pkg_name = path_split[-1]
    return pkg_name


def parse_metadata(target, file_content):

    return re.search(f"^{target} = ['\"]([^'\"]*)['\"]", file_content, re.MULTILINE).group(1)


def load_metadata(pkg_name):
    metadata = {}

    with io.OpenWrapper(f"../{pkg_name}/{pkg_name}/__init__.py", "rt", encoding="utf8") as open_file:
        file_content = open_file.read()

    metadata["version"] = parse_metadata("__version__", file_content)
    metadata["name"] = parse_metadata("__name__", file_content)
    metadata["author"] = parse_metadata("__author__", file_content)
    metadata["description"] = parse_metadata("__description__", file_content)
    metadata["license"] = parse_metadata("__license__", file_content)
    metadata["min_python_version"] = parse_metadata("__min_python_version__", file_content)
    metadata["requirements_file"] = parse_metadata("__requirements_file__", file_content)
    metadata["url"] = parse_metadata("__url__", file_content)
    metadata["year"] = parse_metadata("__year__", file_content)

    return metadata


def read_version(pkg_name):
    with io.OpenWrapper(f"../{pkg_name}/{pkg_name}/__init__.py", "rt", encoding="utf8") as open_file:
        file_content = open_file.read()
    current_version = parse_metadata("__version__", file_content)
    return current_version, file_content


def write_version(pkg_name, next_version):
    current_version, file_content = read_version(pkg_name)
    # result = re.sub(f"^__version__ = ['\"]([^'\"]*)['\"]", f"\\1 {next_version}", file_content)
    file_content = file_content.replace(f'__version__ = "{current_version}"', f'__version__ = "{next_version}"')

    with io.OpenWrapper(f"../{pkg_name}/{pkg_name}/__init__.py", "w", encoding="utf8") as open_file:
        open_file.write(file_content)


def calc_next_version(input_version):
    current_version = version.parse(input_version)

    if current_version.is_devrelease:
        dev = current_version.dev + 1
        next_version = f"{current_version.base_version}.dev{dev}"

    elif current_version.is_prerelease:
        pre = current_version.pre[-1] + 1
        next_version = f"{current_version.base_version}.{current_version.pre[0]}{pre}"

    else:
        parts = [int(part) for part in input_version.split(".")]
        parts[-1] = parts[-1] + 1
        next_version = ".".join([str(part) for part in parts])

    return next_version


def get_next_version(metadata):
    current_version = metadata["version"]
    potential_next_version = calc_next_version(current_version)

    print(f'Current version: {current_version}')
    next_version = input(f"Please enter new version ({potential_next_version}):\n")
    if not next_version:
        next_version = potential_next_version

    print(f"{version.parse(current_version)} < {version.parse(next_version)} {version.parse(current_version) < version.parse(next_version)}")
    if not version.parse(current_version) < version.parse(next_version):
        print("Next version is smaller than current version. Please try again.")
        get_next_version(metadata)

    set_version = input(f"Do you want to set version to {next_version} (y/N)?")

    if set_version != "y":
        get_next_version(metadata)

    return next_version


def test_get_next_version():
    version_tests = [
        "2.1.1.dev",
        "2.1.1.dev2",
        "2.1.1.pre0",
        "2.1.1.pre2",
        "2.1.1",
        "2.1",
        "2",
    ]
    for test in version_tests:
        print(f'{test} -> {calc_next_version(f"{test}")}')


def choose_candidate():
    folders = {}
    for idx, folder in enumerate(glob("../orbis*")):
        folder_name = folder.split("/")[-1]
        folders[str(idx)] = folder_name
        print(f"[{idx}]\t{folder}")

    selection = input("Choose: ")
    publish(folders[selection])


def update_dependencies(publishing_pkg, next_version):
    """
    Update dependencies of target üackage to latest versions of other packages.
    """

    modules = set()
    for folder in glob("../orbis*"):
        pkg = folder.split("/")[-1]
        if pkg != publishing_pkg:
            modules.add(pkg)

    with io.OpenWrapper(f"../{publishing_pkg}/requirements.txt", "rt", encoding="utf8") as open_file:
        file_content = open_file.readlines()

    new_file_content = []
    for line in file_content:
        line = line.strip()
        regex = r"[<>=]{2}"
        subst = "=="
        clean_line = re.sub(regex, subst, line, 0, re.MULTILINE)
        module = clean_line.split("==")[0]

        if module in modules:
            module_version = read_version(module)
            line = f"{module}>={module_version[0]}"
        new_file_content.append(line)

    with io.OpenWrapper(f"../{publishing_pkg}/requirements.txt", "w", encoding="utf8") as open_file:
        open_file.write("\n".join(new_file_content))


def publish(pkg_name):
    pkg_name = pkg_name or get_pkg_name()
    metadata = load_metadata(pkg_name)
    next_version = get_next_version(metadata)
    write_version(pkg_name, next_version)
    update_dependencies(pkg_name, next_version)


def main():
    choose_candidate()


if __name__ == '__main__':
    main()
