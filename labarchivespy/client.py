'''
Defines client object for interacting
with the LabArchives REST API.
'''
import time
import base64
import hmac
import urllib.parse
import xml.etree.ElementTree as ET
from hashlib import sha1
import requests

QUERY_STR = '{api_url}/{api_class}/{api_method}?akid={akid}'
QUERY_STR_WSIG = QUERY_STR + '&expires={expires}&sig={sig}'

class Client():
    '''
    LabArchives client used to make API calls
    '''
    def __init__(self, api_url, access_key_id, access_password):
        self.url = api_url
        self.akid = access_key_id
        self.pwd = access_password
        self.eln_epoch = self.get_eln_epoch_time()
        self.local_epoch = time.time() * 1000.0 # need time in milliseconds

    def get_eln_epoch_time(self):
        '''
        Returns the ELN server epoch time in milliseconds
        '''
        api_class = 'utilities'
        api_method = 'epoch_time'

        query_url = QUERY_STR.format(
            api_url=self.url,
            api_class=api_class,
            api_method=api_method,
            akid=self.akid
        )

        response = requests.get(query_url)
        root = ET.fromstring(response.content)
        epoch = int(root[0].text)

        return epoch

    def get_expires_time(self):
        '''
        Calculates the expires time, required when making API calls.
        Adds the time elapsed since initialising to the ELN epoch time.
        '''
        local_time_now = time.time() * 1000.0
        expires = round(self.eln_epoch + (self.local_epoch - local_time_now))
        return expires

    def get_signature(self, api_method, expires):
        '''
        Takes an API method and expiration time and signs the
        concatenated string using the access password.
        The LabArchives API requires most calls to be authenticated
        through a signed string, which concatenates akid + API
        method + call expiration time.
        '''
        string_to_sign = f'{self.akid}{api_method}{str(expires)}'.encode('utf-8')

        secret_key = self.pwd.encode('utf-8')
        signature = base64.encodebytes(
            hmac.new(
                    secret_key, string_to_sign, sha1
                    ).digest()
            ).strip()
        signature = urllib.parse.quote(signature.decode())

        return signature

    @staticmethod
    def make_params_string(params):
        '''
        Takes a dictionary of parameters and formats
        them for use with the LabArchives REST API.
        '''
        if params:
            param_list = []
            for pkey in params:
                param_list.append(
                    '='.join([pkey, str(params[pkey])])
                )

            param_string = '&'.join(param_list) + '&'
            return param_string

        return ''

    def make_call(self, api_class, api_method, params=None):
        '''
        Makes an arbitrary API call to the LabArchives API given
        the API class, method and parameters and returns the response.
        '''
        expires = self.get_expires_time()
        signature = self.get_signature(api_method, expires)
        param_string = self.make_params_string(params)

        query_url = QUERY_STR_WSIG.format(
            api_url=self.url,
            api_class=api_class,
            api_method=api_method,
            params=param_string,
            akid=self.akid,
            expires=expires,
            sig=signature
        )
        if param_string:
            query_url += "&" + param_string
        response = requests.get(query_url)

        return response
