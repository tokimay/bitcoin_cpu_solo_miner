# Bitcoin solo cpu miner
### Python Bitcoin CPU solo miner

**Notice:** </br>
CPU solo mode is not profitable. I can say it is ***impossible*** with the current network hash rate. </br>
This code works correctly but just for educational purposes. </br>

### Reviewing code teaches you the following topics:

* Communicate with the local bitcoin core.
* Calculate Merkel root.
* Calculate a Coinbase transaction (scriptSig, scriptPubkey, etc.).
* Generate a raw block (block serialization).
* Submit a new block on blockchain.


***[In regtest you first must mine at least 500 blocks. Then start using code. ](https://bitcoin.stackexchange.com/questions/101927/bitcoin-in-regtest-throw-bad-cb-height-at-block-no-500)***

Usage:

+ Clone the source:
````shell 
git clone https://github.com/tokimay/bitcoin_soloMiner
```` 
+ Edit 'pyMiner.py' file in project:

````python 
isRegTest = False
user = 'user'  # change with your own
password = 'userpass'  # change with your own
myAddress = 'YOUR_BTC_ADDRESS'  # change with your own

""" if your address is generated in bitcoinCore """
addressInfo = core.get_address_info(myAddress)
myPubKey = addressInfo['result']['pubkey']
""" if address is generated in third party wallet """
myPubKey = "insert your pubKey"
````
