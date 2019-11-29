import requests
import re
import json
from typing import Union
import logging

_logger = logging.getLogger(__name__)

BASE_URL = "https://docs.growcoaching.de:443/api/"


class Endpoint(object):
    def __init__(self, endpoint: str, *, params: dict = {}, base: str = None):
        self._paramstring = None
        if "://" in endpoint:
            base, endpoint = endpoint.split("api/", 1)
            base += "api/"
            endpoint, self._paramstring = endpoint.split("?", 1)
        if base is None:
            base = BASE_URL
        if not base.endswith("/"):
            base = base + "/"

        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        if not endpoint.endswith("/"):
            endpoint = endpoint + "/"
        if len(params) == 0:
            params = {}

        self.base = base
        self.params = params
        self.endpoint = endpoint

    @property
    def paramstring(self):
        if self._paramstring != None:
            return self._paramstring
        paramstring = "&".join(map(lambda x: f"{x[0]}={x[1]}", self.params.items()))
        return paramstring

    def __repr__(self):
        https_base = re.sub(r":80", ":443", self.base)
        https_base = re.sub(r"http:", "https:", https_base)
        return f"{https_base}{self.endpoint}?{self.paramstring}"

    __str__ = __repr__


class Mayan(object):
    def __init__(self, baseurl, test=False):
        self.test = test
        self.baseurl = baseurl
        pass

    def ep(self, endpoint: str, *, params: dict = {}, base: str = None):
        if base is None:
            base = self.baseurl
        return Endpoint(endpoint, params=params, base=base)

    def login(self, username, password):
        self.session = requests.Session()
        self.session.auth = (username, password)
        auth_data = {"username": username, "password": password}
        token_response = self.session.post(
            self.ep("auth/token/obtain", params={"format": "json"}), data=auth_data
        )
        _logger.debug("Login returned status: %s", token_response.status_code)
        if token_response.status_code != 200:
            raise Exception("Login Failed")
        _logger.debug("Response: %s", token_response.content)
        token = token_response.json()["token"]
        self.session.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {token}",
        }

    def load(self):
        self.content_types = self.all("content_types")
        self.document_types = {x["label"]: x for x in self.all("document_types")}
        self.metadata_types = self.all("metadata_types")
        self.tags = {x["label"]: x for x in self.all("tags")}
        for dt, document_type in self.document_types.items():
            self.document_types[dt]["metadatas"] = self.all(
                self.ep("metadata_types", base=document_type["url"])
            )

    def all(self, endpoint: Union[str, Endpoint]):
        if isinstance(endpoint, str):
            endpoint = self.ep(endpoint)
        results = []
        page = {"next": endpoint}
        while page["next"] != None:
            if isinstance(page["next"], str):
                page["next"] = self.ep(page["next"])
            result = self.session.get(page["next"])
            page = result.json()
            results += page["results"]
        return results

    def first(self, endpoint: Union[str, Endpoint]):
        page = self.get(endpoint)
        return page["results"]

    def get(self, endpoint: Union[str, Endpoint]):
        if endpoint is str:
            endpoint = self.ep(endpoint)
        result = self.session.get(endpoint)
        if result.status_code != 200:
            _logger.warning(json.dumps(result.json(), indent=2))
        return result.json()

    def post(self, endpoint: Union[str, Endpoint], json_data):
        if endpoint is str:
            endpoint = self.ep(endpoint)
        if self.test:
            print("WOULD POST", str(endpoint), json.dumps(json_data, indent=2))
            return {}
        result = self.session.post(endpoint, json=json_data)
        if result.status_code != 200:
            _logger.warning(json.dumps(result.json(), indent=2))
        return result.json()

    def put(self, endpoint: Union[str, Endpoint], json_data):
        if endpoint is str:
            endpoint = self.ep(endpoint)
        if self.test:
            print("WOULD PUT", str(endpoint), json.dumps(json_data, indent=2))
            return {}
        result = self.session.put(endpoint, json=json_data)
        if result.status_code != 200:
            _logger.warning(json.dumps(result.json(), indent=2))
        return result.json()

    def jp(self, data):
        if type(data) is requests.Response:
            try:
                data = data.json()
            except:
                print(data.content)
        try:
            print(json.dumps(data, indent=2))
        except:
            print(data)
