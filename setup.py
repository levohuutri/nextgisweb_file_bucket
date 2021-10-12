import io
from setuptools import setup, find_packages


with io.open('VERSION', 'r') as fd:
    VERSION = fd.read().rstrip()

requires = (
    'nextgisweb>=4.0.0.dev5',
    'zipstream-new==1.1.7',
)

entry_points = {
    'nextgisweb.packages': [
        'nextgisweb_filebucket = nextgisweb_filebucket:pkginfo',
    ],

    'nextgisweb.amd_packages': [
        'nextgisweb_filebucket = nextgisweb_filebucket:amd_packages',
    ],

}

setup(
    name='nextgisweb_filebucket',
    version=VERSION,
    description="",
    long_description="",
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8.*, <4",
    install_requires=requires,
    entry_points=entry_points,
)
