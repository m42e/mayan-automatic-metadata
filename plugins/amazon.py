# Modified sample taken from https://github.com/m42e/mayan-automatic-metadata/pull/2

import mambase
import utils


def parse_and_format_date_german(datestr):
    return utils.parse_and_format_date(datestr, languages=["de", "en"])


class AmazonThirdParty(mambase.RegexMetaDataCheck):
    __documentclass__ = "G - Rechnung"
    __tags__ = ["Amazon"]
    __filter__ = lambda s, x: ("ASIN" in x and "www.amazon.de/contact-us" in x)
    __meta__ = [
        {"metadata": "invoicer", "regex": "Verkauft von (.*)",},
        {
            "metadata": "invoicedate",
            "regex": "Rechnungsdatum\n/Lieferdatum\n+(.*)",
            "post": parse_and_format_date_german,
        },
        {"metadata": "invoicenumber", "regex": "Rechnungsnummer\n+(.*)",},
        {"metadata": "amount", "regex": "Zahlbetrag\n+(.*) €",},
        {
            "metadata": "orderdate",
            "regex": "Bestelldatum\n+(.*)",
            "post": parse_and_format_date_german,
        },
        {"metadata": "ordernumber", "regex": "Bestellnummer\n+(.*)",},
    ]

__plugin__ = [AmazonThirdParty]
