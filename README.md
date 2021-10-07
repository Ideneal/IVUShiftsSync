# IVUShiftsSync
The useful tool to sync your Google Calendar with your IVU shifts.

## Prerequisites

To run the application, you need the following prerequisites:

* Python 3.6 or greater
* The [pip](https://pypi.python.org/pypi/pip) package management tool
* A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
* Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials)
* A Google account with Google Calendar enabled

## Install

Run the following command line to install all requirements:

```bash
pip install -r requirements.txt
```

## Configuration

Run the following command to create the configuration file:

```bash
cp config.yml.dist config.yml
```

Finally, edit the `config.yml` file with your personal credentials.

## Run 

```bash
python app.py
```