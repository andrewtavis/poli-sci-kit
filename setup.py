try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='poli-sci-kit',
    version='0.0.1',
    description='Vote, election, and political appointment analysis in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    license='MIT',
    url="https://github.com/andrewtavis/poli-sci-kit",
    author='Andrew Tavis McAllister',
    author_email='andrew.t.mcallister@gmail.com'
)

install_requires = [
    'numpy',
    'pandas',
    'matplotlib',
    'seaborn'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)