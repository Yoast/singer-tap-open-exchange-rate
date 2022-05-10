# tap-open-exchange-rate

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [PayPal](https://developer.paypal.com/docs/api/overview/)
- Extracts the following resources:
  - [Transactions](https://developer.paypal.com/docs/api/transaction-search/v1)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

### Step 1: Make an account with Open Exchange Rate and get a key


### Step 2: Install and Run

Create a virtual Python environment for this tap. This tap has been tested with Python 3.7, 3.8 and 3.9 and might run on future versions without problems.
```
python -m venv singer-open-exchange
singer-open-exchange/bin/python -m pip install --upgrade pip
singer-open-exchange/bin/pip install git+https://github.com/Yoast/singer-tap-open-exchange-rate.git
```

This tap can be tested by piping the data to a local JSON target. For example:

Create a virtual Python environment with `singer-json`
```
python -m venv singer-json
singer-json/bin/python -m pip install --upgrade pip
singer-json/bin/pip install target-json
```

Test the tap:

```
singer-open-exchange/bin/tap-open-exchange --state state.json -c open-exchange_config.json | singer-json/bin/target-json >> state_result.json
```

Copyright &copy; 2021 Yoast