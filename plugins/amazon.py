import mambase
import utils

class AmazonThirdParty(mambase.RegexMetaDataCheck):
    __documentclass__ = "G - Rechnung"
    __tags__ = ["Amazon"]
    __filter__ = lambda s, x: ("ASIN" in x and "www.amazon.de/contact-us" in x)
    __meta__ = [
        {"metadata": "invoicer", "regex": "Verkauft von (.*)",},
        {
            "metadata": "invoicedate",
            "regex": "Rechnungsdatum\n/Lieferdatum\n+(.*)",
            "post": utils.parse_and_format_date,
        },
        {"metadata": "invoicenumber", "regex": "Rechnungsnummer\n+(.*)",},
        {"metadata": "amount", "regex": "Zahlbetrag\n+(.*) €",},
        {
            "metadata": "orderdate",
            "regex": "Bestelldatum\n+(.*)",
            "post": utils.parse_and_format_date,
        },
        {"metadata": "ordernumber", "regex": "Bestellnummer\n+(.*)",},
    ]

