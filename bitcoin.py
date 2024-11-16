import base64
import binascii
import hashlib
import json
import random
import urllib.request
from pprint import pprint


class BitcoinCore:
    def __init__(self, user: str, password: str, host: str = 'http://127.0.0.1', port: int = 8332):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.RPCurl = self.host + ":" + str(self.port)
        self.id = random.getrandbits(32)
        self.authenticate = base64.b64encode(bytes(self.user + ":" + self.password, "utf8"))

    def setHost(self, host):
        self.host = host

    def setPort(self, port):
        self.port = port

    def setUser(self, user):
        self.user = user

    def setPassword(self, password):
        self.password = password()

    def HOST(self) -> str:
        return self.host

    def PORT(self) -> int:
        return self.port

    def USER(self) -> str:
        return self.user

    def getBlockTemplate(self, templateRequest: dict = None) -> dict:
        """
        :return: It returns data needed to construct a block to work on.
        """
        if templateRequest is None:
            templateRequest = {"rules": ["segwit"]}
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": self.id,
            "method": "getblocktemplate",
            "params": [templateRequest]
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def getMiningInfo(self) -> dict:
        """
        :return: a json object containing mining-related information
        """
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": self.id,
            "method": "getmininginfo",
            "params": []
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        # Send the RPC and parse response.
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def getNetworkHash_ps(self, nBlocks: int = 120, height: int = -1) -> dict:
        """
        nBlocks:
        Type: numeric, optional, default=120
        The number of blocks, or -1 for blocks since last difficulty change.

        height:
        Type: numeric, optional, default=-1
        To estimate at the time of the given height.

        :return: the estimated network hashes per second based on the last n blocks
        """
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": self.id,
            "method": "getnetworkhashps",
            "params": []
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def prioritiseTransaction(self, txId: str, feeDelta: int, dummy: float = 0.0) -> dict:
        """
        txId:
        Type: string, required
        The transaction id.

        feeDelta:
        Type: numeric, required
        The fee value (in satoshis) to add (or subtract, if negative).
        Note, that this value is not a fee rate. It is a value to modify absolute fee of the TX.
        The fee is not actually paid, only the algorithm for selecting transactions into a block considers
        the transaction as it would have paid a higher (or lower) fee.

        dummy:
        Type: numeric, optional
        API-Compatibility for previous API. Must be zero or null.
        DEPRECATED. For forward compatibility use named arguments and omit this parameter.

        :return:Accepts the transaction into mined blocks at a higher (or lower) priority
        """
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": self.id,
            "method": "prioritisetransaction",
            "params": [txId, dummy, feeDelta]
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def submitBlock(self, hexData, dummy: str = 'ignored') -> dict:
        """
        hexData:
        Type: string, required
        the hex-encoded block data to submit

        dummy:
        Type: string, optional, default=ignored
        dummy value, for compatibility with BIP22. This value is ignored.

        :return:
        """
        data = json.dumps({
            "id": self.id,
            "method": "submitblock",
            "params": [hexData]
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        # Send the RPC and parse response.
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def getAddressInfo(self, address: str) -> dict:
        """
        address:
        Type: string, required
        The bitcoin address for which to get information.

        :return: Return information about the given bitcoin address.
        """
        data = json.dumps({
            "id": self.id,
            "method": "getaddressinfo",
            "params": [address]
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        # Send the RPC and parse response.
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response

    def getBlockchainInfo(self) -> dict:
        """
        :return: Returns an object containing various state info regarding blockchain processing.
        """
        data = json.dumps({
            "id": self.id,
            "method": "getblockchaininfo",
            "params": []
        }).encode()
        request = urllib.request.Request(url=self.RPCurl, data=data,
                                         headers={"Authorization": b"Basic " + self.authenticate})
        # Send the RPC and parse response.
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
        if 'result' not in response:
            pprint(response)
            raise response
        else:
            return response


class Calculation:
    def __init__(self):
        pass

    @staticmethod
    def intTarget(bits: str) -> int:
        # return int((temp['result']['bits'][2:] + '00' * (int(temp['result']['bits'][:2], 16) - 3)).zfill(64), 16)
        bits = bytes.fromhex(bits)
        # Extract the parts.
        byte_length = bits[0] - 3
        significand = bits[1:]
        # Scale the significand by byte_length.
        targetBytes = significand + b"\x00" * byte_length
        # Fill in the leading zeros.
        targetBytes = b"\x00" * (32 - len(targetBytes)) + targetBytes
        return int.from_bytes(targetBytes, byteorder='big')

    @staticmethod
    def blockSubsidy(blockHeight: int):
        # halving is every 210,000 blocks
        halving = int(blockHeight / 210000)
        initialSubsidy = 5000000000  # 50 BTC in satoshi
        # calculate the current block subsidy based on the height
        return initialSubsidy >> halving  # bit shift right for every halving

    @staticmethod
    def lenVar(value: int) -> str:
        if value < 253:
            return value.to_bytes(1, byteorder='little').hex()
        if value <= 65535:
            return "fd" + value.to_bytes(2, byteorder='little').hex()
        if value <= 4294967295:
            return "fe" + value.to_bytes(4, byteorder='little').hex()
        return "ff" + value.to_bytes(8, byteorder='little').hex()

    @staticmethod
    def coinbase(
            version: int,
            extraNonce: int,
            height: int,
            coinbaseAmount: int,
            scriptPubkeyWitness: str,
            addressPubKey: str) -> tuple[str, str]:
        version = hex(version)[2:]
        marker = '00'
        flag = '01'
        inputCount = '01'
        txId = '0000000000000000000000000000000000000000000000000000000000000000'  # '0' * 64
        vout = 'ffffffff'
        # scriptSig
        OP_PUSHBYTES_height = str((height.bit_length() + 7) // 8).zfill(2)
        height = (height.to_bytes((height.bit_length() + 7) // 8, 'little')).hex()

        asciiMessage = 'tokimay'.encode('ascii').hex()  # -> your custom data
        OP_PUSHBYTES_asciiMessage = str(len(asciiMessage))

        extraNonce = str((extraNonce.bit_length() + 7) // 8).zfill(16)
        OP_PUSHBYTES_extraNonce = str(len(extraNonce))  # it is 16 in my choice

        scriptSig = (OP_PUSHBYTES_height + height + OP_PUSHBYTES_asciiMessage +
                     asciiMessage + OP_PUSHBYTES_extraNonce + extraNonce)
        scriptSigSize = Calculation.lenVar(len(scriptSig) // 2)
        sequence = 'ffffffff'
        outputCount = '02'
        amount = ''.join(f"{n:02X}" for n in coinbaseAmount.to_bytes(8, byteorder='little'))
        # P2PKH
        scriptPubkey = "76a914" + addressPubKey + "88ac"
        scriptPubkeySize = Calculation.lenVar(len(scriptPubkey) // 2)

        stackItems = '01'
        stackItems_Size = '20'
        stackItemsSize_item = '0000000000000000000000000000000000000000000000000000000000000000'
        lockTime = '00000000'

        scriptPubkeyWitnessSize = Calculation.lenVar(len(scriptPubkeyWitness) // 2)
        amountWitness = '0000000000000000'
        coinbaseRaw = (version + marker + flag + inputCount + txId + vout + scriptSigSize + scriptSig + sequence +
                       outputCount +
                       amount + scriptPubkeySize + scriptPubkey +
                       amountWitness + scriptPubkeyWitnessSize + scriptPubkeyWitness +
                       stackItems + stackItems_Size + stackItemsSize_item + lockTime)
        coinbaseTxId = (version + inputCount + txId + vout + scriptSigSize + scriptSig + sequence + outputCount +
                        amount + scriptPubkeySize + scriptPubkey +
                        amountWitness + scriptPubkeyWitnessSize + scriptPubkeyWitness
                        + lockTime)
        coinbaseTxId = (hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbaseTxId)).digest()).digest())[::-1]

        return coinbaseRaw, coinbaseTxId.hex()

    @staticmethod
    def merkleRoot(branchList: list) -> str:
        if len(branchList) == 1:
            return branchList[0]
        else:
            MerkleRootTemp = []
            for i in range(0, len(branchList) - 1, 2):
                MerkleRootTemp.append(
                    Calculation.doubleSha256Reverse(
                        Calculation.reverse(branchList[i]) + Calculation.reverse(branchList[i + 1]))
                )
            if len(branchList) % 2 == 1:
                MerkleRootTemp.append(
                    Calculation.doubleSha256Reverse(
                        Calculation.reverse(branchList[-1]) + Calculation.reverse(branchList[-1]))
                )
            return Calculation.merkleRoot(MerkleRootTemp)

    @staticmethod
    def headerHash(header: str) -> str:
        solutionHash = (hashlib.sha256(hashlib.sha256(bytearray.fromhex(header)).digest()).digest())[::-1].hex()
        return solutionHash

    @staticmethod
    def reverse(hashString: str) -> str:
        return bytearray.fromhex(hashString)[::-1].hex()

    @staticmethod
    def sha256(data: str) -> str:
        return hashlib.sha256(bytearray.fromhex(data)).hexdigest()

    @staticmethod
    def doubleSha256(data: str) -> str:
        return Calculation.sha256(Calculation.sha256(data))

    @staticmethod
    def doubleSha256Reverse(data: str) -> str:
        return bytearray.fromhex(Calculation.sha256(Calculation.sha256(data)))[::-1].hex()
