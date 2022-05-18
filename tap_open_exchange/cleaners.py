"""Open Exchange cleaners."""
# -*- coding: utf-8 -*-

import collections
from types import MappingProxyType
from tap_open_exchange.streams import STREAMS
from typing import Any, Optional


class ConvertionError(ValueError):
    """Failed to convert value."""


def to_type_or_null(
    input_value: Any,
    data_type: Optional[Any] = None,
    nullable: bool = True,
) -> Optional[Any]:
    """Convert the input_value to the data_type.

    The input_value can be anything. This function attempts to convert the
    input_value to the data_type. The data_type can be a data type such as str,
    int or Decimal or it can be a function. If nullable is True, the value is
    converted to None in cases where the input_value == None. For example:
    a '' == None, {} == None and [] == None.

    Arguments:
        input_value {Any} -- Input value

    Keyword Arguments:
        data_type {Optional[Any]} -- Data type to convert to (default: {None})
        nullable {bool} -- Whether to convert empty to None (default: {True})

    Returns:
        Optional[Any] -- The converted value
    """
    # If the input_value is not equal to None and a data_type input exists
    if input_value and data_type:
        # Convert the input value to the data_type
        try:
            return data_type(input_value)
        except ValueError as err:
            raise ConvertionError(
                f'Could not convert {input_value} to {data_type}: {err}',
            )

    # If the input_value is equal to None and Nullable is True
    elif not input_value and nullable:
        # Convert '', {}, [] to None
        return None

    # If the input_value is equal to None, but nullable is False
    # Return the original value
    return input_value


def clean_row(row: dict, mapping: dict) -> dict:
    """Clean the row according to the mapping.

    The mapping is a dictionary with optional keys:
    - map: The name of the new key/column
    - type: A data type or function to apply to the value of the key
    - nullable: Whether to convert empty values, such as '', {} or [] to None

    Arguments:
        row {dict} -- Input row
        mapping {dict} -- Input mapping

    Returns:
        dict -- Cleaned row
    """
    cleaned: dict = {}

    key: str
    key_mapping: dict

    # For every key and value in the mapping
    for key, key_mapping in mapping.items():

        # Retrieve the new mapping or use the original
        new_mapping: str = key_mapping.get('map') or key

        # Convert the value
        cleaned[new_mapping] = to_type_or_null(
            row[key],
            key_mapping.get('type'),
            key_mapping.get('null', True),
        )

    return cleaned


def clean_exchange_rate_USD(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean exchange rate data with base USD.

    Arguments:
        response_data {dict} -- input response_data

    Returns:
        dict -- cleaned response_data
    """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['exchange_rate_USD'].get(
        'mapping',
    )

    # Create Unique ID
    # id = int(date_day.replace('-', ''))

    # Create new cleaned Dict
    cleaned_data: dict = {
        'timestamp': response_data.get('timestamp'),
        'base': response_data.get('base'),
        'AED': response_data['rates']['AED'],
        'AFN': response_data['rates']['AFN'],
        'ALL': response_data['rates']['ALL'],
        'AMD': response_data['rates']['AMD'],
        'ANG': response_data['rates']['ANG'],
        'AOA': response_data['rates']['AOA'],
        'ARS': response_data['rates']['ARS'],
        'AUD': response_data['rates']['AUD'],
        'AWG': response_data['rates']['AWG'],
        'AZN': response_data['rates']['AZN'],
        'BAM': response_data['rates']['BAM'],
        'BBD': response_data['rates']['BBD'],
        'BDT': response_data['rates']['BDT'],
        'BGN': response_data['rates']['BGN'],
        'BHD': response_data['rates']['BHD'],
        'BIF': response_data['rates']['BIF'],
        'BMD': response_data['rates']['BMD'],
        'BND': response_data['rates']['BND'],
        'BOB': response_data['rates']['BOB'],
        'BRL': response_data['rates']['BRL'],
        'BSD': response_data['rates']['BSD'],
        'BTN': response_data['rates']['BTN'],
        'BWP': response_data['rates']['BWP'],
        'BYN': response_data['rates']['BYN'],
        'BZD': response_data['rates']['BZD'],
        'CAD': response_data['rates']['CAD'],
        'CDF': response_data['rates']['CDF'],
        'CHF': response_data['rates']['CHF'],
        'CLF': response_data['rates']['CLF'],
        'CLP': response_data['rates']['CLP'],
        'CNH': response_data['rates']['CNH'],
        'CNY': response_data['rates']['CNY'],
        'COP': response_data['rates']['COP'],
        'CRC': response_data['rates']['CRC'],
        'CUC': response_data['rates']['CUC'],
        'CUP': response_data['rates']['CUP'],
        'CVE': response_data['rates']['CVE'],
        'CZK': response_data['rates']['CZK'],
        'DJF': response_data['rates']['DJF'],
        'DKK': response_data['rates']['DKK'],
        'DOP': response_data['rates']['DOP'],
        'DZD': response_data['rates']['DZD'],
        'EGP': response_data['rates']['EGP'],
        'ERN': response_data['rates']['ERN'],
        'ETB': response_data['rates']['ETB'],
        'EUR': response_data['rates']['EUR'],
        'FJD': response_data['rates']['FJD'],
        'FKP': response_data['rates']['FKP'],
        'GBP': response_data['rates']['GBP'],
        'GEL': response_data['rates']['GEL'],
        'GGP': response_data['rates']['GGP'],
        'GHS': response_data['rates']['GHS'],
        'GIP': response_data['rates']['GIP'],
        'GMD': response_data['rates']['GMD'],
        'GNF': response_data['rates']['GNF'],
        'GTQ': response_data['rates']['GTQ'],
        'GYD': response_data['rates']['GYD'],
        'HKD': response_data['rates']['HKD'],
        'HNL': response_data['rates']['HNL'],
        'HRK': response_data['rates']['HRK'],
        'HTG': response_data['rates']['HTG'],
        'HUF': response_data['rates']['HUF'],
        'IDR': response_data['rates']['IDR'],
        'ILS': response_data['rates']['ILS'],
        'IMP': response_data['rates']['IMP'],
        'INR': response_data['rates']['INR'],
        'IQD': response_data['rates']['IQD'],
        'IRR': response_data['rates']['IRR'],
        'ISK': response_data['rates']['ISK'],
        'JEP': response_data['rates']['JEP'],
        'JMD': response_data['rates']['JMD'],
        'JOD': response_data['rates']['JOD'],
        'JPY': response_data['rates']['JPY'],
        'KES': response_data['rates']['KES'],
        'KGS': response_data['rates']['KGS'],
        'KHR': response_data['rates']['KHR'],
        'KMF': response_data['rates']['KMF'],
        'KPW': response_data['rates']['KPW'],
        'KRW': response_data['rates']['KRW'],
        'KWD': response_data['rates']['KWD'],
        'KYD': response_data['rates']['KYD'],
        'KZT': response_data['rates']['KZT'],
        'LAK': response_data['rates']['LAK'],
        'LBP': response_data['rates']['LBP'],
        'LKR': response_data['rates']['LKR'],
        'LRD': response_data['rates']['LRD'],
        'LSL': response_data['rates']['LSL'],
        'LYD': response_data['rates']['LYD'],
        'MAD': response_data['rates']['MAD'],
        'MDL': response_data['rates']['MDL'],
        'MGA': response_data['rates']['MGA'],
        'MKD': response_data['rates']['MKD'],
        'MMK': response_data['rates']['MMK'],
        'MNT': response_data['rates']['MNT'],
        'MOP': response_data['rates']['MOP'],
        'MRU': response_data['rates']['MRU'],
        'MUR': response_data['rates']['MUR'],
        'MVR': response_data['rates']['MVR'],
        'MWK': response_data['rates']['MWK'],
        'MXN': response_data['rates']['MXN'],
        'MYR': response_data['rates']['MYR'],
        'MZN': response_data['rates']['MZN'],
        'NAD': response_data['rates']['NAD'],
        'NGN': response_data['rates']['NGN'],
        'NIO': response_data['rates']['NIO'],
        'NOK': response_data['rates']['NOK'],
        'NPR': response_data['rates']['NPR'],
        'NZD': response_data['rates']['NZD'],
        'OMR': response_data['rates']['OMR'],
        'PAB': response_data['rates']['PAB'],
        'PEN': response_data['rates']['PEN'],
        'PGK': response_data['rates']['PGK'],
        'PHP': response_data['rates']['PHP'],
        'PKR': response_data['rates']['PKR'],
        'PLN': response_data['rates']['PLN'],
        'PYG': response_data['rates']['PYG'],
        'QAR': response_data['rates']['QAR'],
        'RON': response_data['rates']['RON'],
        'RSD': response_data['rates']['RSD'],
        'RUB': response_data['rates']['RUB'],
        'RWF': response_data['rates']['RWF'],
        'SAR': response_data['rates']['SAR'],
        'SBD': response_data['rates']['SBD'],
        'SCR': response_data['rates']['SCR'],
        'SDG': response_data['rates']['SDG'],
        'SEK': response_data['rates']['SEK'],
        'SGD': response_data['rates']['SGD'],
        'SHP': response_data['rates']['SHP'],
        'SLL': response_data['rates']['SLL'],
        'SOS': response_data['rates']['SOS'],
        'SRD': response_data['rates']['SRD'],
        'SSP': response_data['rates']['SSP'],
        'STD': response_data['rates']['STD'],
        'STN': response_data['rates']['STN'],
        'SVC': response_data['rates']['SVC'],
        'SYP': response_data['rates']['SYP'],
        'SZL': response_data['rates']['SZL'],
        'THB': response_data['rates']['THB'],
        'TJS': response_data['rates']['TJS'],
        'TMT': response_data['rates']['TMT'],
        'TND': response_data['rates']['TND'],
        'TOP': response_data['rates']['TOP'],
        'TRY': response_data['rates']['TRY'],
        'TTD': response_data['rates']['TTD'],
        'TWD': response_data['rates']['TWD'],
        'TZS': response_data['rates']['TZS'],
        'UAH': response_data['rates']['UAH'],
        'UGX': response_data['rates']['UGX'],
        'USD': response_data['rates']['USD'],
        'UYU': response_data['rates']['UYU'],
        'UZS': response_data['rates']['UZS'],
        'VES': response_data['rates']['VES'],
        'VND': response_data['rates']['VND'],
        'VUV': response_data['rates']['VUV'],
        'WST': response_data['rates']['WST'],
        'XAF': response_data['rates']['XAF'],
        'XAG': response_data['rates']['XAG'],
        'XAU': response_data['rates']['XAU'],
        'XCD': response_data['rates']['XCD'],
        'XDR': response_data['rates']['XDR'],
        'XOF': response_data['rates']['XOF'],
        'XPD': response_data['rates']['XPD'],
        'XPF': response_data['rates']['XPF'],
        'XPT': response_data['rates']['XPT'],
        'YER': response_data['rates']['YER'],
        'ZAR': response_data['rates']['ZAR'],
        'ZMW': response_data['rates']['ZMW'],
        'ZWL': response_data['rates']['ZWL'],
    }

    return clean_row(cleaned_data, mapping)

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Collect all cleaners
CLEANERS: MappingProxyType = MappingProxyType({
    'exchange_rate_USD': clean_exchange_rate_USD,
})