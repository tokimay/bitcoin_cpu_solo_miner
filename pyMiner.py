import datetime
import random

from bitcoin import bitcoinCore, calculation


isRegTest = True
user = 'user'  # change with your own
password = 'userpass'  # change with your own
myAddress = 'bitcoinAddress'  # change with your own

if isRegTest:
    core = bitcoinCore(user=user, password=password, host="http://127.0.0.1", port=18443)
else:
    core = bitcoinCore(user=user, password=password, host="http://127.0.0.1", port=8332)


""" if your address is generated in bitcoinCore """
addressInfo = core.getAddressInfo(myAddress)
myPubKey = addressInfo['result']['pubkey']
""" if address is generated in third party wallet """
# myPubKey = "insert your pubKey"

newExtraNonce = True
nonce = 0
refreshThreshold = 100_000_000

while True:
    if newExtraNonce:
        nonce = 0
        extraNonce = random.randint(0x0, 0xffff)
        newExtraNonce = False
        refreshThreshold = 100_000_000
        print('extraNonce', extraNonce)
    tempBlock = core.getBlockTemplate()
    print('block template refreshed')
    target = int(tempBlock['result']['target'], 16)

    # if you are on RegTest make it a little harder
    if isRegTest:
        target = int(target / pow(2, 24))

    ver = (tempBlock['result']['version'].to_bytes((tempBlock['result']['version'].bit_length() + 7) // 8, 'little')).hex()
    previousBlockhash = calculation.reverse(tempBlock['result']['previousblockhash'])
    bits = calculation.reverse(tempBlock['result']['bits'])
    nonceRange = int(tempBlock['result']['noncerange'], 16)

    merkleBranch = []
    transactionsRaw = ''
    if len(tempBlock['result']['transactions']) > 0:
        merkleBranch = []
        for trx in tempBlock['result']['transactions']:
            merkleBranch.append(trx['txid'])
            transactionsRaw = transactionsRaw + trx['data']
    scriptPubkeyWitness = tempBlock['result']['default_witness_commitment']

    coinbase, cBiD = calculation.coinbase(version=tempBlock['result']['version'], extraNonce=extraNonce,
                                          height=tempBlock['result']['height'],
                                          coinbaseAmount=tempBlock['result']['coinbasevalue'],
                                          scriptPubkeyWitness=scriptPubkeyWitness,
                                          addressPubKey=myPubKey)

    transactionsRaw = coinbase + transactionsRaw
    # coinBase transaction ID as first transaction ID
    merkleBranch.insert(0, cBiD)
    lenTransactions = calculation.lenVar(len(merkleBranch))
    merkleRoot = calculation.reverse(calculation.merkleRoot(branchList=merkleBranch))
    nTimeNew = calculation.reverse((hex(tempBlock['result']['curtime']))[2:])
    lenNounce = int(len(tempBlock['result']['noncerange']) / 2)
    print('start checking nonce range:')
    while nonce <= nonceRange:
        nonce += 1
        blockHeader = ver + previousBlockhash + merkleRoot + nTimeNew + bits + (hex(nonce)[2:]).zfill(8)
        blockRaw = blockHeader + lenTransactions + transactionsRaw
        solution = calculation.headerHash(blockHeader)
        if nonce % 1_000_000 == 0 and nonce != 0:
            print(f"{int(nonce/1_000_000)} mega nonce number checked {datetime.datetime.now()}")
            if nonce % refreshThreshold == 0 and nonce != 0:
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
