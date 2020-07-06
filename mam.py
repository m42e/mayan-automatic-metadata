import argparse
import datetime
import importlib
import inspect
import json
import logging
import mayan
import os
import re
import requests
import sys
from plugins import mambase
from typing import List, Dict
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def get_options():
    config = {}
    config["username"] = os.getenv("MAYAN_USER")
    config["password"] = os.getenv("MAYAN_PASSWORD")
    config["url"] = os.getenv("MAYAN_URL")
    return config


def get_mayan():
    _logger.info("logging in")
    args = get_options()
    m = mayan.Mayan(args["url"])
    m.login(args["username"], args["password"])
    _logger.info("load meta informations")
    m.load()
    return m


def main():
    m = get_mayan()
    _logger.info("load documents")
    process(m, "1204")
    return
    documents = m.all("documents")
    for document in documents:
        _logger.info("Document {}".format(str(document)))
        tags = m.first(m.ep("tags", base=document["url"]))
        if not any(map(lambda x: x["label"] == "MAM", tags)):
            process(m, document)
        else:
            _logger.info(
                "skipping already processed document %s %d",
                document["label"],
                document["id"],
            )


def single(document):
    m = get_mayan()
    _logger.info("load document %s", document)
    process(m, document)


def process(m, document):
    if isinstance(document, str):
        if document.isnumeric():
            document = m.get(m.ep(f"documents/{document}"))
        else:
            _logger.error("document value %s must be numeric", document)
            return

    if not isinstance(document, dict):
        _logger.error("could not retrieve document")
        return

    versions = m.get(document["latest_version"]["url"])
    pages = m.all(m.ep("pages", base=document["latest_version"]["url"]))
    complete_content = ""
    for page in pages:
        content = m.get(m.ep("content", base=page["url"]))
        try:
            complete_content += content["content"]
        except:
            pass
        try:
            content = m.get(m.ep("ocr", base=page["url"]))
            complete_content += content["content"]
        except:
            pass

    original_pythonpath = sys.path
    sys.path.append("plugins")
    _, _, files = next(os.walk("plugins"))
    for file in files:
        if not file.endswith(".py"):
            continue
        modulename = file[:-3]
        try:
            importlib.invalidate_caches()
            mod = importlib.import_module(modulename)
            importlib.reload(mod)
        except:
            _logger.exception("Could not load module %s", modulename)
        if not hasattr(mod, "__plugin__"):
            _logger.warn("skipping %s", modulename)
            continue
        for cls in mod.__plugin__:
            checker = cls()
            _logger.info(
                "Checking content with %s (%s), %s for doc: %s %d",
                checker.__class__.__name__,
                file,
                modulename,
                document["label"],
                document["id"],
            )
            if not checker.for_documentclass(document["document_type"]["label"]):
                _logger.info("Skipping based on document class")
                continue
            if not checker.for_content(complete_content):
                _logger.info("Skipping based on content")
                continue
            metadata = checker.get_metadata(complete_content)
            doc_metadata = {
                x["metadata_type"]["name"]: x
                for x in m.all(m.ep("metadata", base=document["url"]))
            }
            for meta in m.document_types[document["document_type"]["label"]][
                "metadatas"
            ]:
                meta_name = meta["metadata_type"]["name"]
                if meta_name in metadata:
                    if meta_name not in doc_metadata:
                        _logger.info(
                            "Add metadata %s (value: %s) to %s",
                            meta_name,
                            metadata[meta_name],
                            document["url"],
                        )
                        data = {
                            "metadata_type_pk": meta["metadata_type"]["id"],
                            "value": metadata[meta_name],
                        }
                        result = m.post(
                            m.ep("metadata", base=document["url"]), json_data=data
                        )

                    else:
                        data = {"value": metadata[meta_name]}
                        result = m.put(
                            m.ep(
                                "metadata/{}".format(doc_metadata[meta_name]["id"]),
                                base=document["url"],
                            ),
                            json_data=data,
                        )
                        pass

            tags = checker.get_tags(complete_content)
            if len(tags) == 0:
                continue
            tags.append("MAM")
            for t in tags:
                if t not in m.tags:
                    _logger.info("Tag %s not defined in system", t)
                    continue
                data = {"tag_pk": m.tags[t]["id"]}
                result = m.post(m.ep("tags", base=document["url"]), json_data=data)
    sys.path = original_pythonpath


if __name__ == "__main__":
    main()
