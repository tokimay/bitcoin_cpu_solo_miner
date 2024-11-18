import datetime
import random
from bitcoin import BitcoinCore, Calculation


isRegTest = False
user = 'user'  # change with your own user name
password = 'userpass'  # change with your own
myAddress = 'YOUR_BTC_ADDRESS'  # change with your own

if isRegTest:
    core = BitcoinCore(user=user, password=password, host="http://127.0.0.1", port=18443)
else:
    core = BitcoinCore(user=user, password=password, host="http://127.0.0.1", port=8332)


""" if your address is generated in bitcoinCore """
addressInfo = core.getAddressInfo(myAddress)
myPubKey = addressInfo['result']['pubkey']
""" if address is generated in third party wallet """
# myPubKey = "insert your pubKey"

newExtraNonce = True
extraNonce = 0
nonce = 0
refreshThreshold = 100_000_000

while True:
    if newExtraNonce:
        nonce = 0
        extraNonce = random.randint(0x0, 0xffff)
        newExtraNonce = False
        refreshThreshold = 100_000_000
        print('extraNonce:', extraNonce)
    tempBlock = core.getBlockTemplate()
    print('block template refreshed.')
    target = int(tempBlock['result']['target'], 16)

    # if you are on RegTest make it a little harder
    if isRegTest:
        target = int(target / pow(2, 24))

    ''' block header '''
    # 4 bytes version
    version = tempBlock['result']['version']
    version = (Calculation.reverse((hex(version))[2:])).zfill(8)

    # 32 bytes previous block hash
    previousBlockhash = Calculation.reverse(tempBlock['result']['previousblockhash'])

    # 32 bytes merkle root
    merkleBranch = []
    transactionsRaw = ''
    if len(tempBlock['result']['transactions']) > 0:
        merkleBranch = []
        for trx in tempBlock['result']['transactions']:
            merkleBranch.append(trx['txid'])
            transactionsRaw = transactionsRaw + trx['data']

    coinbase, cBiD = Calculation.coinbase(version=tempBlock['result']['version'], extraNonce=extraNonce,
                                          height=tempBlock['result']['height'],
                                          coinbaseAmount=tempBlock['result']['coinbasevalue'],
                                          scriptPubkeyWitness=tempBlock['result']['default_witness_commitment'],
                                          addressPubKey=myPubKey)

    merkleBranch.insert(0, cBiD)   # coinBase transaction ID as first transaction ID
    merkleRoot = Calculation.merkleRoot(branchList=merkleBranch)
    merkleRoot = Calculation.reverse(merkleRoot)

    # 4 bytes time
    time = tempBlock['result']['curtime']
    time = (Calculation.reverse((hex(time))[2:])).zfill(8)

    # 4 bytes bits
    bits = tempBlock['result']['bits']
    bits = (Calculation.reverse(bits)).zfill(8)

    # 4 byte nonce
    ''' int loop section will be calculated'''

    lenTransactions = Calculation.lenVar(len(merkleBranch))
    transactionsRaw = coinbase + transactionsRaw

    nonceRange = int(tempBlock['result']['noncerange'], 16)
    print('start checking nonce range:')
    while nonce <= nonceRange:
        nonce += 1
        blockHeader = (version + previousBlockhash + merkleRoot +
                       time + bits + (Calculation.reverse((hex(nonce))[2:].zfill(8))))
        blockRaw = blockHeader + lenTransactions + transactionsRaw
        solution = Calculation.headerHash(blockHeader)
        if nonce % 1_000_000 == 0:
            print(f"{int(nonce/1_000_000)} mega nonce number checked {datetime.datetime.now()}")
            if nonce % refreshThreshold == 0:
                nonce += 1
                refreshThreshold += 100_000_000
                print('going to re-fetch block template')
                break  # exit loop to get new block template
        if int(solution, 16) < target:
            block = core.submitBlock(blockRaw)
            if block['error'] is None:
                b = core.getBlockchainInfo()
                print(f"succeed \nheight  : {b['result']['blocks']} \nhash    :{b['result']['bestblockhash']}")
                exit(0)
    if nonce >= nonceRange:
        print(
            'all nonce range checked.\ntry new extra nounce to change coinbase hash -> merkle root hash -> header hash')
        newExtraNonce = True
