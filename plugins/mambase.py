import re
from typing import Dict
import logging
_logger = logging.getLogger(__name__)


class MetaDataCheck(object):
    def __init__(self):
        pass

    def for_documentclass(self, documentclass: str) -> bool:
        raise NotImplementedError()

    def get_metadata(self, content: str) -> Dict:
        raise NotImplementedError()


class RegexMetaDataCheck(MetaDataCheck):
    __documentclass__ = None
    __tags__ = []
    __meta__ = []

    def __filter__(self, x):
        return True

    def for_documentclass(self, documentclass: str) -> bool:
        if isinstance(self.__documentclass__, list):
            return documentclass in self.__documentclass__
        return documentclass == self.__documentclass__

    def for_content(self, content: str) -> bool:
        return self.__filter__(content)

    def get_tags(self, content: str):
        return self.__tags__.copy()

    def get_metadata(self, content: str) -> Dict:
        if not self.__filter__(content):
            return {}

        metadatas = {}
        for meta_re in self.__meta__:
            if "value" in meta_re:
                if callable(meta_re["value"]):
                    metadatas[meta_re["metadata"]] = meta_re["value"]()
                else:
                    metadatas[meta_re["metadata"]] = meta_re["value"]
                continue
            m = re.findall(meta_re["regex"], content)
            if len(m) == 0:
                _logger.info("%s not found in document", meta_re["metadata"])
                continue
            if "selector" in meta_re:
                if not callable(meta_re["selector"]):
                    _logger.warn("selector not callable")
                    continue
                meta_re["selector"](m)
            else:
                value = m[meta_re.get("slice", 0)]
            if meta_re.get("join", False):
                value = ", ".join(value)
            if "post" in meta_re:
                value = meta_re["post"](value)
            metadatas[meta_re["metadata"]] = value
        return metadatas

