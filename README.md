# LabArchives API wrapper for Python

A python wrapper for interacting with the [LabArchives API](https://mynotebook.labarchives.com/share/LabArchives%20API/Ny44fDI3LzYvVHJlZU5vZGUvMTE1MzU5MTAyNXwxOS44). This very simple package makes it easier to make arbitrary calls to the LabArchives REST API using python's requests module.

## Installation

Please ensure you have Python 3.3+ installed. Then run:

```
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
pip install .
```

## Configuration

You will now have to make a `config.yaml` file with the following information:

```
api_url: <base URL for the API>
access_key_id: <your LabArchives access key ID>
access_password: <your LabArchives password>
```

`https://api.labarchives.com/api` is the normal base URL for the LabArchives API, however this may vary by region (for Australia, use `https://auapi.labarchives.com/api`).

## Testing

Once you've done this, you can now test the install by running:

```
pytest
```

## Using the API

The `tests/test_client.py` file will give you a good example on how to use the package. A minimal example would look something like:

```python
# import Client from the package
from labarchivespy.client import Client

# load your config file
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

# set up client
api_url = config['api_url']
access_key_id = config['access_key_id']
access_password = config['access_password']
client = Client(api_url, access_key_id, access_password)

response = client.make_call('utilities', 'institutional_login_urls')
assert response.ok
```

You can now parse the response object for the desired information, or check the corroesponding notebook entry if you've made a call that makes some kind of change to your ELN. Note that you will have to look up the API class and method call name from the [LabArchives REST API](https://mynotebook.labarchives.com/share/LabArchives%20API/Ny44fDI3LzYvVHJlZU5vZGUvMTE1MzU5MTAyNXwxOS44). The documentation shows example URLs in the following format:

    https://<baseurl>/api/<api_class>/<api_method>?<Call Authentication Parameters>

You'll need to use the correct `api_class` and `api_method` when using the `make_call` function, and ensure your parameters are correct.

Most calls that do anything useful require a user ID. This will require you to obtain your app authentication token (if you are using SSO). To get this, login to your LabArchives and click on your name (top right) then "LA App authentication". Copy this password. You can now get your user ID:

```python
import xml

login_params = {'login_or_email': <your_username>, 'password': <your password token>}
response = client.make_call('users', 'user_access_info', params=login_params)
uid = xml.etree.ElementTree.fromstring(response.content)[0].text

print(uid)
```

You can now use this in calls, for example:

```python
params = {'uid': uid}
response = client.make_call('users', 'user_info_via_id', params=params)
```
