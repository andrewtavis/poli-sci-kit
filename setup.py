try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="poli-sci-kit",
    version="0.1.2",
    author="Andrew Tavis McAllister",
    author_email="andrew.t.mcallister@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    description="Political elections, appointment, analysis and visualization in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    license="new BSD",
    url="https://github.com/andrewtavis/poli-sci-kit",
)

install_requires = ["pytest-cov", "scipy", "numpy", "pandas", "seaborn", "colormath"]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
