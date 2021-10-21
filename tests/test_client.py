'''
Test LabArchives python client
'''
import sys
import os
import pytest
import yaml
from labarchivespy.client import Client

# load config file
CONFIG_FILE = 'config.yaml'
if not os.path.isfile(CONFIG_FILE):
    sys.exit('Config file not found. Exiting.')

with open(CONFIG_FILE, 'r', encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        sys.exit(exc)

# set up client
api_url = config['api_url']
access_key_id = config['access_key_id']
access_password = config['access_password']
client = Client(api_url, access_key_id, access_password)

def test_get_eln_epoch_time():
    '''
    Test get_eln_epoch_time function
    '''
    epoch_time = client.get_eln_epoch_time()
    assert isinstance(epoch_time, int)

def test_get_signature():
    '''
    Test get_signature function
    '''
    epoch_time = client.get_eln_epoch_time()
    sig = client.get_signature('institutional_login_urls', epoch_time)
    assert isinstance(sig, str)

def test_get_expires_time():
    '''
    Test get_expires_time function
    '''
    expires = client.get_expires_time()
    assert isinstance(expires, int)

@pytest.mark.parametrize('params,string', [(None, ''),
                                          ({'uid': '123'}, 'uid=123&'),
                                          ({'uid': '123', 'nbid': 'abc'}, 'uid=123&nbid=abc&')])
def test_make_params_string(params, string):
    '''
    Test make_params_string function
    '''
    assert client.make_params_string(params) == string

def test_make_call():
    '''
    Test make_call function
    '''
    response = client.make_call('utilities', 'institutional_login_urls')
    assert response.ok
