# Contributing to synbiohub_adapter

## General Guidelines

* [Create a GitHub Issue](#reporting-issues) for any bug, feature, or
  enhancement you find or intend to address.
* Submit enhancements or bug fixes using pull requests
  (see the [sample workflow below](#sample-contribution-workflow)).
* synbiohub_adapter uses the
  [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching model.

## Reporting Issues ##
* Check [existing issues](https://github.com/SD2E/synbiohub_adapter/issues) first to
  see if the issue has already been reported.
* Review the general [GitHub guidlines on isssues](https://guides.github.com/features/issues/).
* Give specific examples, sample outputs, etc
* Do not include any passwords, private keys, or any information you don't want public.

## Sample Contribution Workflow ##
1. [Report the issue](#reporting-issues) or check issue comments for a suggested solution.
2. Create an issue-specific branch off of the `develop` branch
   * The automated tests/builds cannot be run from forks, so you'll have to push a branch this repository
   * Name your branch with the issue number as a prefix (e.g. `58-gitflow`)
3. Develop your fix.
   * Follow the [code guidelines below](#code-style).
   * Reference the appropriate issue numbers in your commit messages.
4. Test your fix
5. Merge any commits on develop since you branched
6. [Submit a pull request](https://help.github.com/articles/using-pull-requests/)
   against the `develop` branch of the project repository.
   * In your pull request description, note what issue(s) your pull request addresses.

## Code Style ##
* The [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
  is enforced by the unit tests. You can use
  [pycodestyle](https://pypi.org/project/pycodestyle/) to check your code
  before submitting a pull request.

_Thank you for your contributions!_
