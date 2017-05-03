

## Install latest release:
Python 2:
```
$ virtualenv -p /usr/local/Cellar/python/2.7.13/bin/python2.7 venv
$ pip install -r requiements.txt
```



## Usage:
### Basic Public Setup (no api Key/Secret):
```python
from poloniex import Poloniex
polo = Poloniex()
```
Ticker
```python
print(polo('returnTicker')['BTC_ETH'])
# or
print(polo.returnTicker()['BTC_ETH'])
```
Public trade history:
```python
print(polo.marketTradeHist('BTC_ETH'))
```

### Basic Private Setup (ApiKey/Secret required):
```python
import poloniex
polo = poloniex.Poloniex('your-Api-Key-Here-xxxx','yourSecretKeyHere123456789')
# or
polo.key = 'your-Api-Key-Here-xxxx'
polo.secret = 'yourSecretKeyHere123456789'
```
Get all your balances
```python
balance = polo.returnBalances()
print("I have %s ETH!" % balance['ETH'])
# or
balance = polo('returnBalances')
print("I have %s BTC!" % balance['BTC'])
```
### Custom/external coach example:
```python
from poloniex import Poloniex, Coach
myCoach = Coach()

public = Poloniex(coach=myCoach)
private = Poloniex(key, secret, coach=myCoach)
# now make calls using both 'private' and 'public' and myCoach will handle both
```

**Examples of WAMP applications using the websocket push API can be found [here](https://github.com/s4w3d0ff/python-poloniex/tree/master/examples).**
# crypto
