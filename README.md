


# Releasing a change

Once the code is ready you must do the following:

1. Run this script to update the version number in `module.json` and `README.md`, commit the changes, push to the remote repository, create a new release on GitHub, download the module zip file, update the `manifest` and `download` fields in `module.json`, commit the changes, and push to the remote repository.
```bash
python3 scripts/bump_version.py [patch|minor|major]
```
