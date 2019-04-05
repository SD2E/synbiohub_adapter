# How to create a release

1. Update [issues](https://github.com/SD2E/synbiohub_adapter/issues) and
   [pull requests](https://github.com/SD2E/synbiohub_adapter/pulls) so they are appropriately
   targeted for this milestone and closed
1. Bump the version number in README.md
   * _Note: Use the standard contribution process by submitting these changes via a pull request, not a direct push to the synbiohub_adapter repository_
   * Call this pull request something like "Prep 1.1 release"
1. Open a pull request to promote the release from develop to master
   * Note that the target branch may have to be manually set to master
1. Merge the promotion pull request opened in the previous step
1. Tag the release using [semantic versioning](http://semver.org)

   ```shell
   cd <synbiohub_adapter>
   git checkout master
   git tag -a v1.X -m "Release 1.X" master
   git push upstream --tags
   ```

1. Update GitHub [milestones](https://github.com/SD2E/synbiohub_adapter/milestones)
   * Close the current milestone
   * Create a new milestone for the next release
1. Build the wheel

    ```shell
    python3 setup.py sdist bdist_wheel
    ```

1. Create a GitHub release, upload the tar file and wheel
   * [Create a release](https://github.com/SD2E/synbiohub_adapter/releases/new) (Releases; Draft a new release)
   * Use the current tag
   * Name it "Major.Minor[.Patch]"
   * Add notes about what changes were made in this release. At a
     minimum, link to the milestone which documents the issues and
     pull requests that are part of the release.
   * Upload the tar file and wheel created above
1. Bump the version numbers on the develop branch
   * _Note: Use the standard contribution process by submitting these changes via a pull request, not a direct push to the synbiohub_adapter repository_
   * Bump version number in `synbiohub_adapter/__init__.py`
   * Bump version number in `setup.py`
