from datetime import datetime
import setuptools
import sys


def load_metadata():
    metadata = {}
    with open("metadata.txt", encoding="utf-8") as open_file:
        for line in open_file.readlines():
            key, value = line.split(" = ")
            metadata[key] = value.replace('"', '').replace("\n", "")
    metadata['year'] = datetime.today().year
    metadata['copyright'] = f"{metadata['year']}, {metadata['author']}"
    metadata['release'] = " ".join([metadata['version'], metadata['version_tag']])
    with open("metadata.txt", "w", encoding="utf-8") as open_file:
        output_list = []
        for key, value in metadata.items():
            output_list.append((key, value))
        for key, value in sorted(output_list):
            open_file.write(f'{key} = "{value}"\n')
    return metadata


def load_requirements_file(metadata):
    requirements = []
    with open(metadata['requirements_file'], encoding="utf8") as open_file:
        for line in open_file.readlines():
            requirements.append(line.replace("\n", ""))
    return requirements


def check_python_version(metadata):
    python_needed = tuple([int(i) for i in metadata['min_python_version'].split(".")])
    if not sys.version_info >= python_needed:
        sys.exit(f"Sorry, Python {metadata['min_python_version']} or newer needed")


def run_setup():
    metadata = load_metadata()
    check_python_version(metadata)
    setuptools.setup(
        name=metadata['project'],
        version=metadata['version'],
        description=metadata['description'],
        url=metadata['url'],
        license=metadata['license'],
        packages=setuptools.find_packages(),
        python_requires=f">={metadata['min_python_version']}",
        install_requires=load_requirements_file(metadata),
        entry_points={
            'console_scripts': [
                'orbis = orbis.main:main'
            ]
        },
    )


if __name__ == '__main__':
    run_setup()
