# Releasing a change

Once the code is ready you must do the following:

1. Run this script to update the version number in `module.json`. Provide the argument `[patch|minor|major]` to specify the type of update.
```bash
python3 scripts/bump_version.py [patch|minor|major]
```
2. Commit the changes to the repository.
3. Push the changes to the remote repository.

A new release should be created on GitHub automatically within a minute or two.
