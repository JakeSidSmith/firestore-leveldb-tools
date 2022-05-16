# firestore-leveldb-tools

Documentation and tools for converting LevelDB files into JSON files. (eg. for reading Google Firestore and Datastore backups)

For Firestore, instructions for creating these backups can be [seen here](https://stackoverflow.com/a/51783326).

### Setup

1) Make sure Python 2.7 is installed, and present in your `Path` environment variable. (or just supply the absolute path to its `python` executable in usage step 1)
2) Clone/download this repo to disk.

### Usage

1) Run `python to_json.py PATH_TO_FIRESTORE_BACKUP_FOLDER` (pass the direct parent folder of the "output-0", etc. files)
2) A `Data.json` file will be created in the backup folder, with the original database structure. (collections as json objects, their documents as keyed entries underneath)

### SDK Dependencies

The `to_json.py` script relies on some modules within the google-cloud-sdk and appengine-sdk (older versions, since the newest ones are missing some modules we need). Stripped-down versions of these sdks are included in this repo for convenience; however, if you need to use different versions for some reason, you can find them here:
* Google Cloud SDK archive (included: `google-cloud-sdk-180.0.1-windows-x86_64.zip`): https://console.cloud.google.com/storage/browser/cloud-sdk-release
* AppEngine SDK archive (included: `180/google_appengine_1.8.0.zip`): https://console.cloud.google.com/storage/browser/appengine-sdks/deprecated

To use the alternate version downloaded, extract the archives, then replace the corresponding contents within the `vendor` folder.

### Building a Binary

If not already installed, install [pyenv](https://github.com/pyenv/pyenv) for managing python versions.

Install the correct python version:

Note: this must be done with `--enable-shared` for `pyinstaller` to work.

```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 2.7.18
```

Ensure your pyenv install was correct and you are now using the correct python version:

```bash
which python
# Outputs: /Users/user/.pyenv/shims/python
python --version
# Outputs: 2.7.18
```

Install virtualenv:

```bash
pip install virtualenv
```

Create a virtual environment:

```bash
virtualenv venv
```

Install python dependencies:

```bash
venv/bin/pip install -r requirements.txt
```

Build the binary:

Note: If you encounter errors you may also need to reinstall python with `--enable-framework`.

```bash
venv/bin/pyinstaller to_json.spec
```

### Alternatives

* [firestore-export-json](https://github.com/labbots/firestore-export-json): Similar, but using some pip-installed dependencies. (and in Python 3)
