from bitcoinCore import bitcoinCore, calculation

# for RegTest
core = bitcoinCore("tokimay", "r@eza", "http://127.0.0.1", 18443)
# for MainNet
# core = bitcoinCore("tokimay", "r@eza", "http://127.0.0.1", 8332)

addressInfo = core.getAddressInfo('bcrt1qlftz77jay2x0phkfp4hwcswrypvc63d30kas7u')

tempBlock = core.getBlockTemplate()

target = int(tempBlock['result']['target'], 16)
ver = (tempBlock['result']['version'].to_bytes((tempBlock['result']['version'].bit_length() + 7) // 8, 'little')).hex()
previousBlockhash = calculation.reverse(tempBlock['result']['previousblockhash'])
bits = calculation.reverse(tempBlock['result']['bits'])
nonceRange = int(tempBlock['result']['noncerange'], 16)

extra_Nonce = 1

merkleBranch = []
transactionsRaw = ''
if len(tempBlock['result']['transactions']) > 0:
    merkleBranch = []
    for trx in tempBlock['result']['transactions']:
        merkleBranch.append(trx['txid'])
        transactionsRaw = transactionsRaw + trx['data']
scriptPubkeyWitness = tempBlock['result']['default_witness_commitment']

coinbase, cBiD = calculation.coinbase(version=tempBlock['result']['version'], extraNonce=extra_Nonce,
                                      height=tempBlock['result']['height'],
                                      coinbaseAmount=tempBlock['result']['coinbasevalue'],
                                      scriptPubkeyWitness=scriptPubkeyWitness,
                                      addressPubKey=addressInfo['result']['pubkey'])

transactionsRaw = coinbase + transactionsRaw
# coinBase transaction ID as first transaction ID
merkleBranch.insert(0, cBiD)
lenTransactions = calculation.lenVar(len(merkleBranch))
merkleRoot = calculation.reverse(calculation.merkleRoot(branchList=merkleBranch))
nTimeNew = calculation.reverse((hex(tempBlock['curtime']))[2:])
lenNounce = int(len(tempBlock['result']['noncerange']) / 2)

for nonce in range(0, nonceRange):
    blockHeader = ver + previousBlockhash + merkleRoot + nTimeNew + bits + (hex(nonce)[2:]).zfill(8)
    blockRaw = blockHeader + lenTransactions + transactionsRaw
    solution = calculation.headerHash(blockHeader)
    if int(solution, 16) < target:
        block = core.submitBlock(blockRaw)
        if block['error'] is None:
            b = core.getBlockchainInfo()
            print(f"succeed \nheight  : {b['result']['blocks']} \nhash    :{b['result']['bestblockhash']}")
            break
