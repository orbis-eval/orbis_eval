import io
import re


def parse_metadata(target, file_content):
    regex = f"^{target} = ['\"](.*?)['\"]"
    metadatum = re.search(regex, file_content, re.MULTILINE).group(1)
    return metadatum


def load_metadata(init_path):
    metadata = {}

    with io.OpenWrapper(init_path, 'rt', encoding='utf8') as open_file:
        file_content = open_file.read()

    metadata['version'] = parse_metadata('__version__', file_content)
    metadata['name'] = parse_metadata('__name__', file_content)
    metadata['author'] = parse_metadata('__author__', file_content)
    metadata['description'] = parse_metadata('__description__', file_content)
    metadata['license'] = parse_metadata('__license__', file_content)
    metadata['min_python_version'] = parse_metadata('__min_python_version__', file_content)
    metadata['requirements_file'] = parse_metadata('__requirements_file__', file_content)
    metadata['url'] = parse_metadata('__url__', file_content)
    metadata['year'] = parse_metadata('__year__', file_content)
    metadata['type'] = parse_metadata('__type__', file_content)

    return metadata
