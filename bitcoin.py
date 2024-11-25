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

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def set_user(self, user):
        self.user = user

    def set_password(self, password):
        self.password = password()

    def host(self) -> str:
        return self.host

    def port(self) -> int:
        return self.port

    def user(self) -> str:
        return self.user

    def get_block_template(self, template_request: dict = None) -> dict:
        """
        :return: It returns data needed to construct a block to work on.
        """
        if template_request is None:
            template_request = {"rules": ["segwit"]}
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": self.id,
            "method": "getblocktemplate",
            "params": [template_request]
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

    def get_mining_info(self) -> dict:
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

    def get_network_hash_ps(self, n_blocks: int = 120, height: int = -1) -> dict:
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

    def prioritise_transaction(self, tx_id: str, fee_delta: int, dummy: float = 0.0) -> dict:
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
            "params": [tx_id, dummy, fee_delta]
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

    def submit_block(self, hex_data, dummy: str = 'ignored') -> dict:
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
            "params": [hex_data]
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

    def get_address_info(self, address: str) -> dict:
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

    def get_blockchain_info(self) -> dict:
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
    def int_target(bits: str) -> int:
        # return int((temp['result']['bits'][2:] + '00' * (int(temp['result']['bits'][:2], 16) - 3)).zfill(64), 16)
        bits = bytes.fromhex(bits)
        # Extract the parts.
        byte_length = bits[0] - 3
        significand = bits[1:]
        # Scale the significand by byte_length.
        target_bytes = significand + b"\x00" * byte_length
        # Fill in the leading zeros.
        target_bytes = b"\x00" * (32 - len(target_bytes)) + target_bytes
        return int.from_bytes(target_bytes, byteorder='big')

    @staticmethod
    def block_subsidy(block_height: int):
        # halving is every 210,000 blocks
        halving = int(block_height / 210000)
        initial_subsidy = 5000000000  # 50 BTC in satoshi
        # calculate the current block subsidy based on the height
        return initial_subsidy >> halving  # bit shift right for every halving

    @staticmethod
    def len_var(value: int) -> str:
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
            extra_nonce: int,
            height: int,
            coinbase_amount: int,
            script_pubkey_witness: str,
            address_pub_key: str) -> tuple[str, str]:
        version = hex(version)[2:]
        marker = '00'
        flag = '01'
        input_count = '01'
        tx_id = '0000000000000000000000000000000000000000000000000000000000000000'  # '0' * 64
        vout = 'ffffffff'
        # script_sig
        OP_PUSHBYTES_height = str((height.bit_length() + 7) // 8).zfill(2)
        height = (height.to_bytes((height.bit_length() + 7) // 8, 'little')).hex()

        ascii_message = 'tokimay'.encode('ascii').hex()  # -> your custom data
        OP_PUSHBYTES_ascii_message = str(len(ascii_message))

        extra_nonce = hex(extra_nonce)[2:].zfill(16)
        OP_PUSHBYTES_extra_nonce = str(len(extra_nonce))  # it is 16 in my choice

        script_sig = (OP_PUSHBYTES_height + height + OP_PUSHBYTES_ascii_message +
                     ascii_message + OP_PUSHBYTES_extra_nonce + extra_nonce)
        script_sig_size = Calculation.len_var(len(script_sig) // 2)
        sequence = 'ffffffff'
        output_count = '02'
        amount = ''.join(f"{n:02X}" for n in coinbase_amount.to_bytes(8, byteorder='little'))
        # P2PKH
        script_pubkey = "76a914" + address_pub_key + "88ac"
        script_pubkey_size = Calculation.len_var(len(script_pubkey) // 2)

        stack_items = '01'
        stack_items_size = '20'
        stack_items_size_item = '0000000000000000000000000000000000000000000000000000000000000000'
        lock_time = '00000000'

        script_pubkey_witness_size = Calculation.len_var(len(script_pubkey_witness) // 2)
        amount_witness = '0000000000000000'
        coinbase_raw = (version + marker + flag + input_count + tx_id + vout + script_sig_size + script_sig + sequence +
                       output_count +
                       amount + script_pubkey_size + script_pubkey +
                       amount_witness + script_pubkey_witness_size + script_pubkey_witness +
                       stack_items + stack_items_size + stack_items_size_item + lock_time)
        coinbase_tx_id = (version + input_count + tx_id + vout + script_sig_size + script_sig + sequence + output_count +
                        amount + script_pubkey_size + script_pubkey +
                        amount_witness + script_pubkey_witness_size + script_pubkey_witness
                        + lock_time)
        coinbase_tx_id = (hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase_tx_id)).digest()).digest())[::-1]

        return coinbase_raw, coinbase_tx_id.hex()

    @staticmethod
    def merkle_root(branch_list: list) -> str:
        if len(branch_list) == 1:
            return branch_list[0]
        else:
            merkle_root_temp = []
            for i in range(0, len(branch_list) - 1, 2):
                merkle_root_temp.append(
                    Calculation.double_sha256_reverse(
                        Calculation.reverse(branch_list[i]) + Calculation.reverse(branch_list[i + 1]))
                )
            if len(branch_list) % 2 == 1:
                merkle_root_temp.append(
                    Calculation.double_sha256_reverse(
                        Calculation.reverse(branch_list[-1]) + Calculation.reverse(branch_list[-1]))
                )
            return Calculation.merkle_root(merkle_root_temp)

    @staticmethod
    def header_hash(header: str) -> str:
        solution_hash = (hashlib.sha256(hashlib.sha256(bytearray.fromhex(header)).digest()).digest())[::-1].hex()
        return solution_hash

    @staticmethod
    def reverse(hash_string: str) -> str:
        return bytearray.fromhex(hash_string)[::-1].hex()

    @staticmethod
    def sha256(data: str) -> str:
        return hashlib.sha256(bytearray.fromhex(data)).hexdigest()

    @staticmethod
    def double_sha256(data: str) -> str:
        return Calculation.sha256(Calculation.sha256(data))

    @staticmethod
    def double_sha256_reverse(data: str) -> str:
        return bytearray.fromhex(Calculation.sha256(Calculation.sha256(data)))[::-1].hex()
