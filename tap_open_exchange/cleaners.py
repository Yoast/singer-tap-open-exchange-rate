"""Open Exchange cleaners."""
# -*- coding: utf-8 -*-

import collections
from types import MappingProxyType
from tap_open_exchange.streams import STREAMS
from typing import Any, Optional
from datetime import datetime, timezone

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


def clean_exchange_rate_EUR(
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
    mapping: Optional[dict] = STREAMS['exchange_rate_EUR'].get(
        'mapping',
    )

    # Create new cleaned Dict
    cleaned_data: dict = {
        'timestamp': response_data.get('timestamp'),
        'base': response_data.get('base'),
        'AED': response_data.get('rates').get('AED'),
        'AFN': response_data.get('rates').get('AFN'),
        'ALL': response_data.get('rates').get('ALL'),
        'AMD': response_data.get('rates').get('AMD'),
        'ANG': response_data.get('rates').get('ANG'),
        'AOA': response_data.get('rates').get('AOA'),
        'ARS': response_data.get('rates').get('ARS'),
        'AUD': response_data.get('rates').get('AUD'),
        'AWG': response_data.get('rates').get('AWG'),
        'AZN': response_data.get('rates').get('AZN'),
        'BAM': response_data.get('rates').get('BAM'),
        'BBD': response_data.get('rates').get('BBD'),
        'BDT': response_data.get('rates').get('BDT'),
        'BGN': response_data.get('rates').get('BGN'),
        'BHD': response_data.get('rates').get('BHD'),
        'BIF': response_data.get('rates').get('BIF'),
        'BMD': response_data.get('rates').get('BMD'),
        'BND': response_data.get('rates').get('BND'),
        'BOB': response_data.get('rates').get('BOB'),
        'BRL': response_data.get('rates').get('BRL'),
        'BSD': response_data.get('rates').get('BSD'),
        'BTN': response_data.get('rates').get('BTN'),
        'BWP': response_data.get('rates').get('BWP'),
        'BYN': response_data.get('rates').get('BYN'),
        'BZD': response_data.get('rates').get('BZD'),
        'CAD': response_data.get('rates').get('CAD'),
        'CDF': response_data.get('rates').get('CDF'),
        'CHF': response_data.get('rates').get('CHF'),
        'CLF': response_data.get('rates').get('CLF'),
        'CLP': response_data.get('rates').get('CLP'),
        'CNH': response_data.get('rates').get('CNH'),
        'CNY': response_data.get('rates').get('CNY'),
        'COP': response_data.get('rates').get('COP'),
        'CRC': response_data.get('rates').get('CRC'),
        'CUC': response_data.get('rates').get('CUC'),
        'CUP': response_data.get('rates').get('CUP'),
        'CVE': response_data.get('rates').get('CVE'),
        'CZK': response_data.get('rates').get('CZK'),
        'DJF': response_data.get('rates').get('DJF'),
        'DKK': response_data.get('rates').get('DKK'),
        'DOP': response_data.get('rates').get('DOP'),
        'DZD': response_data.get('rates').get('DZD'),
        'EGP': response_data.get('rates').get('EGP'),
        'ERN': response_data.get('rates').get('ERN'),
        'ETB': response_data.get('rates').get('ETB'),
        'EUR': response_data.get('rates').get('EUR'),
        'FJD': response_data.get('rates').get('FJD'),
        'FKP': response_data.get('rates').get('FKP'),
        'GBP': response_data.get('rates').get('GBP'),
        'GEL': response_data.get('rates').get('GEL'),
        'GGP': response_data.get('rates').get('GGP'),
        'GHS': response_data.get('rates').get('GHS'),
        'GIP': response_data.get('rates').get('GIP'),
        'GMD': response_data.get('rates').get('GMD'),
        'GNF': response_data.get('rates').get('GNF'),
        'GTQ': response_data.get('rates').get('GTQ'),
        'GYD': response_data.get('rates').get('GYD'),
        'HKD': response_data.get('rates').get('HKD'),
        'HNL': response_data.get('rates').get('HNL'),
        'HRK': response_data.get('rates').get('HRK'),
        'HTG': response_data.get('rates').get('HTG'),
        'HUF': response_data.get('rates').get('HUF'),
        'IDR': response_data.get('rates').get('IDR'),
        'ILS': response_data.get('rates').get('ILS'),
        'IMP': response_data.get('rates').get('IMP'),
        'INR': response_data.get('rates').get('INR'),
        'IQD': response_data.get('rates').get('IQD'),
        'IRR': response_data.get('rates').get('IRR'),
        'ISK': response_data.get('rates').get('ISK'),
        'JEP': response_data.get('rates').get('JEP'),
        'JMD': response_data.get('rates').get('JMD'),
        'JOD': response_data.get('rates').get('JOD'),
        'JPY': response_data.get('rates').get('JPY'),
        'KES': response_data.get('rates').get('KES'),
        'KGS': response_data.get('rates').get('KGS'),
        'KHR': response_data.get('rates').get('KHR'),
        'KMF': response_data.get('rates').get('KMF'),
        'KPW': response_data.get('rates').get('KPW'),
        'KRW': response_data.get('rates').get('KRW'),
        'KWD': response_data.get('rates').get('KWD'),
        'KYD': response_data.get('rates').get('KYD'),
        'KZT': response_data.get('rates').get('KZT'),
        'LAK': response_data.get('rates').get('LAK'),
        'LBP': response_data.get('rates').get('LBP'),
        'LKR': response_data.get('rates').get('LKR'),
        'LRD': response_data.get('rates').get('LRD'),
        'LSL': response_data.get('rates').get('LSL'),
        'LYD': response_data.get('rates').get('LYD'),
        'MAD': response_data.get('rates').get('MAD'),
        'MDL': response_data.get('rates').get('MDL'),
        'MGA': response_data.get('rates').get('MGA'),
        'MKD': response_data.get('rates').get('MKD'),
        'MMK': response_data.get('rates').get('MMK'),
        'MNT': response_data.get('rates').get('MNT'),
        'MOP': response_data.get('rates').get('MOP'),
        'MRU': response_data.get('rates').get('MRU'),
        'MUR': response_data.get('rates').get('MUR'),
        'MVR': response_data.get('rates').get('MVR'),
        'MWK': response_data.get('rates').get('MWK'),
        'MXN': response_data.get('rates').get('MXN'),
        'MYR': response_data.get('rates').get('MYR'),
        'MZN': response_data.get('rates').get('MZN'),
        'NAD': response_data.get('rates').get('NAD'),
        'NGN': response_data.get('rates').get('NGN'),
        'NIO': response_data.get('rates').get('NIO'),
        'NOK': response_data.get('rates').get('NOK'),
        'NPR': response_data.get('rates').get('NPR'),
        'NZD': response_data.get('rates').get('NZD'),
        'OMR': response_data.get('rates').get('OMR'),
        'PAB': response_data.get('rates').get('PAB'),
        'PEN': response_data.get('rates').get('PEN'),
        'PGK': response_data.get('rates').get('PGK'),
        'PHP': response_data.get('rates').get('PHP'),
        'PKR': response_data.get('rates').get('PKR'),
        'PLN': response_data.get('rates').get('PLN'),
        'PYG': response_data.get('rates').get('PYG'),
        'QAR': response_data.get('rates').get('QAR'),
        'RON': response_data.get('rates').get('RON'),
        'RSD': response_data.get('rates').get('RSD'),
        'RUB': response_data.get('rates').get('RUB'),
        'RWF': response_data.get('rates').get('RWF'),
        'SAR': response_data.get('rates').get('SAR'),
        'SBD': response_data.get('rates').get('SBD'),
        'SCR': response_data.get('rates').get('SCR'),
        'SDG': response_data.get('rates').get('SDG'),
        'SEK': response_data.get('rates').get('SEK'),
        'SGD': response_data.get('rates').get('SGD'),
        'SHP': response_data.get('rates').get('SHP'),
        'SLL': response_data.get('rates').get('SLL'),
        'SOS': response_data.get('rates').get('SOS'),
        'SRD': response_data.get('rates').get('SRD'),
        'SSP': response_data.get('rates').get('SSP'),
        'STD': response_data.get('rates').get('STD'),
        'STN': response_data.get('rates').get('STN'),
        'SVC': response_data.get('rates').get('SVC'),
        'SYP': response_data.get('rates').get('SYP'),
        'SZL': response_data.get('rates').get('SZL'),
        'THB': response_data.get('rates').get('THB'),
        'TJS': response_data.get('rates').get('TJS'),
        'TMT': response_data.get('rates').get('TMT'),
        'TND': response_data.get('rates').get('TND'),
        'TOP': response_data.get('rates').get('TOP'),
        'TRY': response_data.get('rates').get('TRY'),
        'TTD': response_data.get('rates').get('TTD'),
        'TWD': response_data.get('rates').get('TWD'),
        'TZS': response_data.get('rates').get('TZS'),
        'UAH': response_data.get('rates').get('UAH'),
        'UGX': response_data.get('rates').get('UGX'),
        'USD': response_data.get('rates').get('USD'),
        'UYU': response_data.get('rates').get('UYU'),
        'UZS': response_data.get('rates').get('UZS'),
        'VES': response_data.get('rates').get('VES'),
        'VND': response_data.get('rates').get('VND'),
        'VUV': response_data.get('rates').get('VUV'),
        'WST': response_data.get('rates').get('WST'),
        'XAF': response_data.get('rates').get('XAF'),
        'XAG': response_data.get('rates').get('XAG'),
        'XAU': response_data.get('rates').get('XAU'),
        'XCD': response_data.get('rates').get('XCD'),
        'XDR': response_data.get('rates').get('XDR'),
        'XOF': response_data.get('rates').get('XOF'),
        'XPD': response_data.get('rates').get('XPD'),
        'XPF': response_data.get('rates').get('XPF'),
        'XPT': response_data.get('rates').get('XPT'),
        'YER': response_data.get('rates').get('YER'),
        'ZAR': response_data.get('rates').get('ZAR'),
        'ZMW': response_data.get('rates').get('ZMW'),
        'ZWL': response_data.get('rates').get('ZWL'),
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
    'exchange_rate_EUR': clean_exchange_rate_EUR,
})