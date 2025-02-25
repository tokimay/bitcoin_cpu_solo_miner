
# This file is part of https://github.com/tokimay/bitcoin_cpu_solo_miner
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/bitcoin_cpu_solo_miner

import datetime
import random
from bitcoin import BitcoinCore, Calculation


isRegTest = True
user = 'user'  # change with your own
password = 'userpass'  # change with your own
myAddress = 'YOUR_BTC_ADDRESS'  # change with your own

if isRegTest:
    core = BitcoinCore(user=user, password=password, host="http://127.0.0.1", port=18443)
else:
    core = BitcoinCore(user=user, password=password, host="http://127.0.0.1", port=8332)


""" if your address is generated in bitcoinCore """
addressInfo = core.get_address_info(myAddress)
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
    tempBlock = core.get_block_template()
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

    coinbase, cBiD = Calculation.coinbase(version=tempBlock['result']['version'], extra_nonce=extraNonce,
                                          height=tempBlock['result']['height'],
                                          coinbase_amount=tempBlock['result']['coinbasevalue'],
                                          script_pubkey_witness=tempBlock['result']['default_witness_commitment'],
                                          address_pub_key=myPubKey)

    merkleBranch.insert(0, cBiD)   # coinBase transaction ID as first transaction ID
    merkleRoot = Calculation.merkle_root(branch_list=merkleBranch)
    merkleRoot = Calculation.reverse(merkleRoot)

    # 4 bytes time
    time = tempBlock['result']['curtime']
    time = (Calculation.reverse((hex(time))[2:])).zfill(8)

    # 4 bytes bits
    bits = tempBlock['result']['bits']
    bits = (Calculation.reverse(bits)).zfill(8)

    # 4 byte nonce
    ''' int loop section will be calculated'''

    lenTransactions = Calculation.len_var(len(merkleBranch))
    transactionsRaw = coinbase + transactionsRaw

    nonceRange = int(tempBlock['result']['noncerange'], 16)
    print('start checking nonce range:')
    while nonce <= nonceRange:
        nonce += 1
        blockHeader = (version + previousBlockhash + merkleRoot +
                       time + bits + (Calculation.reverse((hex(nonce))[2:].zfill(8))))
        blockRaw = blockHeader + lenTransactions + transactionsRaw
        solution = Calculation.header_hash(blockHeader)
        if nonce % 1_000_000 == 0:
            print(f"{int(nonce/1_000_000)} mega nonce number checked {datetime.datetime.now()}")
            if nonce % refreshThreshold == 0:
                nonce += 1
                refreshThreshold += 100_000_000
                print('going to re-fetch block template')
                break  # exit loop to get new block template
        if int(solution, 16) < target:
            block = core.submit_block(blockRaw)
            if block['error'] is None:
                b = core.get_blockchain_info()
                print(f"succeed \nheight  : {b['result']['blocks']} \nhash    :{b['result']['bestblockhash']}")
                exit(0)
    if nonce >= nonceRange:
        print(
            'all nonce range checked.\ntry new extra nounce to change coinbase hash -> merkle root hash -> header hash')
        newExtraNonce = True
