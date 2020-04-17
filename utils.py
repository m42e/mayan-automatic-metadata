import dateparser
import datetime
import logging

_logger = logging.getLogger(__name__)


def parse_and_format_date(datestr):
    dt = dateparser.parse(datestr, languages=["de", "en"])
    fmtdate = dt.strftime("%Y-%m-%d")
    _logger.info("Parsing %s result %s", datestr, fmtdate)
    return fmtdate


def parse_and_format_month_year(datestr):
    dt = dateparser.parse(datestr, languages=["de", "en"])
    fmtdate = dt.strftime("%Y-%m")
    _logger.info("Parsing %s result %s", datestr, fmtdate)
    return fmtdate


def parse_and_format_date_german(datestr):
    dt = datetime.datetime.strptime(datestr, "%d.%m.%Y")
    fmtdate = dt.strftime("%Y-%m-%d")
    _logger.info("Parsing %s result %s", datestr, fmtdate)
    return fmtdate

def parse_and_format_date_germanshort(datestr):
    dt = datetime.datetime.strptime(datestr, "%d.%m.%y")
    fmtdate = dt.strftime("%Y-%m-%d")
    _logger.info("Parsing %s result %s", datestr, fmtdate)
    return fmtdate


def select_highest_amount(matches):
    maxval = 0.00
    for m in matches:
        val = float(m.replace(",", "."))
        if val > maxval:
            maxval = val
    _logger.info("selected %s out of %s", maxval, len(matches))
    return str(maxval)
