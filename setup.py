import distutils
from setuptools import setup
from version import VERSION

try:
    distutils.dir_util.remove_tree("dist")
except:
    pass

setup(
    name='kervi-component-library',
    version=VERSION,
    description="""Component library for kervi""",
    packages=[
        "sensors"
    ]
)
