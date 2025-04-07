# YellowChangerAPI

`YellowChangerAPI` is a Python library for interacting with the [YellowChanger](https://yellowchanger.com) service API. The library allows you to get exchange rates, create trades, and get information about trades.

## Installation

To install the library, use the following command:

```sh
pip install yellowchangerapi
```

## Usage

### Synchronous Client

Example of using the synchronous client:

```python
from yellow_changer_api import YellowChanger

def main():
    public_api_key = "your_public_api_key"
    secret_api_key = "your_secret_api_key"

    yellow_changer = YellowChanger(public_api_key, secret_api_key)

    # Get all rates
    rates = yellow_changer.all_rates()
    print(rates)

    # Get destinations list
    destinations_list = yellow_changer.destinations_list()
    print(destinations_list)

    # Get rates in direction USDT
    rates_in_direction_USDT = yellow_changer.rates_in_direction('USDT')
    print(rates_in_direction_USDT)

    # Create a trade
    trade = yellow_changer.create_trade(
        send_name='USDT',
        get_name='USDT',
        send_value=100,
        send_network='TRC20',
        get_network='ERC20',
        get_creds='0x4c...'
    )

    trade_uniq_id = trade.get('uniq_id')

    # Get trade information
    trade_info = yellow_changer.get_info(trade_uniq_id)
    print(trade_info)

if __name__ == '__main__':
    main()
```

### Asynchronous Client

Example of using the asynchronous client:

```python
import asyncio
from yellow_changer_api import AsyncYellowChanger

async def main():
    public_api_key = "your_public_api_key"
    secret_api_key = "your_secret_api_key"

    # Each request creates a new httpx session
    yellow_changer = AsyncYellowChanger(public_api_key, secret_api_key)

    # Get all rates
    rates = await yellow_changer.all_rates()
    print(rates)

    # Get destinations list
    destinations_list = await yellow_changer.destinations_list()
    print(destinations_list)

    # Get rates in direction USDT
    rates_in_direction_USDT = await yellow_changer.rates_in_direction('USDT')
    print(rates_in_direction_USDT)

    # Create a trade
    trade = await yellow_changer.create_trade(
        send_name='USDT',
        get_name='USDT',
        send_value=100,
        send_network='TRC20',
        get_network='ERC20',
        get_creds='0x4c...'
    )

    trade_uniq_id = trade.get('uniq_id')

    # Get trade information
    trade_info = await yellow_changer.get_info(trade_uniq_id)
    print(trade_info)

if __name__ == '__main__':
    asyncio.run(main())
```

## Methods

Both clients (synchronous and asynchronous) have the same methods:

### `all_rates()`

Gets all exchange rates.

**Example:**
```python
# Synchronous
rates = yellow_changer.all_rates()

# Asynchronous
rates = await yellow_changer.all_rates()
```

### `destinations_list()`

Gets the list of all destinations.

**Example:**
```python
# Synchronous
destinations = yellow_changer.destinations_list()

# Asynchronous
destinations = await yellow_changer.destinations_list()
```

### `rates_in_direction(direction: str)`

Gets all exchange rates in a specific direction.

**Parameters:**
- `direction` (str): The direction of the rate, for example, 'USDT'.

**Example:**
```python
# Synchronous
rates = yellow_changer.rates_in_direction('USDT')

# Asynchronous
rates = await yellow_changer.rates_in_direction('USDT')
```

### `get_info(uniq_id: str)`

Gets information about a trade by its unique ID.

**Parameters:**
- `uniq_id` (str): The unique ID of the trade.

**Example:**
```python
# Synchronous
info = yellow_changer.get_info('your_unique_id')

# Asynchronous
info = await yellow_changer.get_info('your_unique_id')
```

### `create_trade(*args, **kwargs)`

Creates a new trade based on the provided parameters.

**Example for cryptocurrency:**
```python
# Synchronous
trade = yellow_changer.create_trade(
    send_name='USDT',
    get_name='USDT',
    send_value=100,
    send_network='TRC20',
    get_network='ERC20',
    get_creds='0x4c...'
)

# Asynchronous
trade = await yellow_changer.create_trade(
    send_name='USDT',
    get_name='USDT',
    send_value=100,
    send_network='TRC20',
    get_network='ERC20',
    get_creds='0x4c...'
)
```

**Example for bank:**
```python
# Synchronous
trade = yellow_changer.create_trade(
    send_name="USDT",
    get_name="RUB",
    send_value=100,
    send_network="TRC20",
    get_network="RUB",
    get_creds="1234567890123456",
    sbpBank="sbpsber"
)

# Asynchronous
trade = await yellow_changer.create_trade(
    send_name="USDT",
    get_name="RUB",
    send_value=100,
    send_network="TRC20",
    get_network="RUB",
    get_creds="1234567890123456",
    sbpBank="sbpsber"
)
```
```