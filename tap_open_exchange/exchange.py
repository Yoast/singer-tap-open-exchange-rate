"""OpenExchangeRate API Client."""  # noqa: WPS226
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta, timezone, date
from types import MappingProxyType
from typing import Generator, Optional, Callable, List

import requests
import singer
from dateutil.parser import isoparse
from dateutil.rrule import DAILY, rrule

from tap_open_exchange.cleaners import CLEANERS


API_SCHEME: str = 'https://'
API_BASE_URL: str = 'openexchangerates.org/'
API_TYPE: str = 'api/historical/'
API_DATE: str = ':date:'
API_RESPONSE_TYPE: str = '.json'
API_KEY_VAR: str = '?app_id='
API_XCHANGE_VAR: str = '&base='

# HEADERS: MappingProxyType = MappingProxyType({  # Frozen dictionary
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer :accesstoken:',
# })


class OpenExchange(object):  # noqa: WPS230
    """OpenExchange API Client."""

    def __init__(
        self,
        api_key: str,
    ) -> None:
        """Initialize client.

        Arguments:
            api_key {str} -- OpenExchange API key
        """
        self.api_key: str = api_key
        self.logger: logging.Logger = singer.get_logger()

    def exchange_rate_USD(  # noqa: WPS210, WPS213
        self,
        **kwargs: dict,
    ) -> Generator[dict, None, None]:
        """OpenExchangeRate, USD as base currency.

        Raises:
            ValueError: When the parameter start_date is missing

        Yields:
            Generator[dict] -- Yields daily exchange rates
        """
        self.logger.info('Stream exchange rates from base USD')

        base_var = 'USD'

        # Validate the start_date value exists
        start_date_input: str = str(kwargs.get('start_date', ''))

        if not start_date_input:
            raise ValueError('The parameter start_date is required.')

        # Get the Cleaner
        cleaner: Callable = CLEANERS.get('exchange_rate_USD', {})

        # Create Header with Auth Token
        # self._create_headers()

        for date_day in self._start_days_till_now(start_date_input):

            # Replace placeholder in reports path
            from_to_date: str = API_DATE.replace(
                ':date:',
                date_day,
            )

            self.logger.info(
                f'Retreiving exchange rates from {date_day}'
            )

            # Build URL
            url: str = (
                f'{API_SCHEME}{API_BASE_URL}{API_TYPE}{from_to_date}'
                f'{API_RESPONSE_TYPE}{API_KEY_VAR}{self.api_key}{API_XCHANGE_VAR}{base_var}'
            )

            # # Make the call to Postmark API
            # response: httpx._models.Response = self.client.get(  # noqa: WPS437
            #     url
            # )

            response = requests.get(url)

            # # Raise error on 4xx and 5xxx
            # response.raise_for_status()

            # Create dictionary from response
            response_data: dict = response.json()

            date_converted = datetime.fromtimestamp(response_data.get('timestamp'), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')

            response_data.update({'timestamp': date_converted})

            # Yield Cleaned results
            yield cleaner(date_day, response_data)

    def _start_days_till_now(self, start_date: str) -> Generator:
        """Yield YYYY/MM/DD for every day until now.
        Arguments:
            start_date {str} -- Start date e.g. 2020-01-01
        Yields:
            Generator -- Every day until now.
        """
        # Parse input date
        year: int = int(start_date.split('-')[0])
        month: int = int(start_date.split('-')[1].lstrip())
        day: int = int(start_date.split('-')[2].lstrip())

        # Setup start period
        period: date = date(year, month, day)

        # Setup itterator
        dates: rrule = rrule(
            freq=DAILY,
            dtstart=period,
            until=datetime.utcnow(),
        )

        # Yield dates in YYYY-MM-DD format
        yield from (date_day.strftime('%Y-%m-%d') for date_day in dates)

    # def _create_headers(self) -> None:
    #     """Create authenticationn headers for requests."""
    #     headers: dict = dict(HEADERS)
    #     headers['Authorization'] = headers['Authorization'].replace(
    #         ':accesstoken:',
    #         self.token,
    #     )
    #     self.headers = headers