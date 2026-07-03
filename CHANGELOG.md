# Changelog

poli-sci-kit tries to follow [semantic versioning](https://semver.org/), a MAJOR.MINOR.PATCH version where increments are made of the:

- MAJOR version when we make incompatible API changes
- MINOR version when we add functionality in a backwards compatible manner
- PATCH version when we make backwards compatible bug fixes

## poli-sci-kit 2.0.1

- Dependencies of the project were updated and the way they're installed was changed to `uv` based groups.

## poli-sci-kit 2.0.0

- Function names were changed to make them more verbose for clearer functionality
- All functions were typed and docstrings were expanded
- `prek` based pre-commit hooks are used to improve package development
- `Ruff` is now used for formatting and import sorting instead of `black`
- Linting is now done with `ty` instead of `mypy`
- Dependency management is now done via `uv`
- All production and development dependencies were updated
- Tests and GitHub workflows were updated given the above changes

## poli-sci-kit 1.1.0

- The assignment of points for semicircle parliament plots now groups points for parties together more appropriately

## poli-sci-kit 1.0.1

- Updates source code files with direct references to the code they're based on

## poli-sci-kit 1.0.0

- Release switches poli-sci-kit over to [semantic versioning](https://semver.org/) and indicates that it is stable

## poli-sci-kit 0.1.2.5

Changes include:

- Package structure has been modified for better testing and a cleaner wheel
- Bug fixes and refactoring for cleaner code
- Checks for code quality have been added
- Examples now function in Google Colab

## poli-sci-kit 0.1.0

First stable release of poli-sci-kit

Changes include:

- Plotting functions for parliament allocations and seat disproportionality
- Full documentation of the package
- Virtual environment files
- Bug fixes
- Extensive testing of all modules with GH Actions and Codecov
- Code of conduct and contribution guidelines

## poli-sci-kit 0.0.2.1

The minimum viable product of poli-sci-kit

- Users are able to do political appointments using a variety of methods including largest remainder and highest averages techniques
- Users are able to analyze the results of appointments
- Usage examples have been created
