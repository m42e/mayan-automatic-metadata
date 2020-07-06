import dateparser
import datetime
import logging

_logger = logging.getLogger(__name__)


def parse_and_format_date(datestr, **kwargs):
    dt = dateparser.parse(datestr, **kwargs)
    fmtdate = dt.strftime("%Y-%m-%d")
    _logger.info("Parsing %s result %s", datestr, fmtdate)
    return fmtdate


def parse_and_format_month_year(datestr, **kwargs):
    dt = dateparser.parse(datestr, **kwargs)
    fmtdate = dt.strftime("%Y-%m")
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
