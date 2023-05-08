import sys
from pathlib import Path

import semver
from setuptools import find_packages, setup
from setuptools.dist import Distribution as _Distribution

__name__ = "ebe"
vp = Path(__file__).parent / "src" / __name__ / "version.py"
__version__ = semver.VersionInfo.parse(vp.read_text().strip().split('"')[1])


def version():
    if len(sys.argv) > 1 and sys.argv[1] == "bdist_wheel":
        nv = f"{__version__.bump_patch()}"
        vp.write_text(f'__version__ = "{nv}"\n')
        return nv
    return f"{__version__}"


class Distribution(_Distribution):
    def is_pure(self):
        return True


setup(
    name=__name__,
    version=version(),
    author="cacko",
    author_email="alex@cacko.net",
    distclass=Distribution,
    url=f"http://pypi.cacko.net/simple/{__name__}/",
    description="whatever",
    install_requires=[
        "appdirs==1.4.4",
        "autopep8==2.0.2",
        "corefile==0.1.2",
        "corelog==0.0.8",
        "pydantic==1.10.7",
        "semver==3.0.0",
        "pandas==2.0.1",
        "progressor==1.0.16",
        "click==8.1.3",
        "humanfriendly==10.0",
        "pyfiglet",
        "questionary>=1.10.0",
        "emoji>=2.2.0"
    ],
    setup_requires=["wheel"],
    python_requires=">=3.10",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points="""
        [console_scripts]
        ebe=ebe.cli:cli
    """,
)
