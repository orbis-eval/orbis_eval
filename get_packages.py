import requests
import re


def collect_packages():
    r = requests.get('https://pypi.org/simple/')

    text = r.text

    regex = r".*?href.*?>(orbis-[addon|plugin].*?)</a>"

    matches = re.finditer(regex, text, re.MULTILINE)

    """
    for match in matches:
        print(f"{match.group(1)} (https://pypi.org/project/{match.group(1)}/)")
    """

    result = [match.group(1) for match in matches]

    return result


def test_maintainer(package):
    r = requests.get(f"https://pypi.org/project/{package}/")
    text = r.text

    regex = (r"<div class=\"sidebar-section\">\n"
    r".*<h3 class=\"sidebar-section__title\">Maintainers</h3>\n"
    r".*\n"
    r".*\n"
    r".*<span class=\"sidebar-section__maintainer\">\n"
    r".*<a href=\"/user/fabod/\" aria-label=\"fabod\">")

    matches = re.finditer(regex, text, re.MULTILINE)

    matches = [match for match in matches]
    print(len(matches))


def quick_verify(packages):
    for package in packages:
        test_maintainer(package)
        print(f"https://pypi.org/project/{package}/")



packages = collect_packages()
quick_verify(packages)
