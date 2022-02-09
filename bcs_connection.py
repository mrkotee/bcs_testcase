import requests
import json
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_tx, sign_tx, create_signed_tx
from pycoin.coins.Tx import Tx

bcs_ip = "http://45.32.232.25:3669"
bcs_user = "bcs_tester"
bcs_psw = "iLoveBCS"
wallet = "BABwZ2m2egkav6Rdaphw8pddU9hQ1eHKZJ"
w_prv = "Ky55QyyFLFqvr6kvL1gQkZro9FL3R6dr8i1TYncWD7TTHNMzikJt"
"BPqv8d9wup7UeV9XoFFi2qCTNYyYzcQTBw"

"""
Параметры сети BCS Chain (network): 
wif_prefix_hex="80", 
address_prefix_hex="19",
pay_to_script_prefix_hex="32",
bip32_prv_prefix_hex="0488ade4",
bip32_pub_prefix_hex="0488B21E", 
bech32_hrp="bc", 
bip49_prv_prefix_hex="049d7878",
bip49_pub_prefix_hex="049D7CB2", 
bip84_prv_prefix_hex="04b2430c",
bip84_pub_prefix_hex="04B24746", 
magic_header_hex="F1CFA6D3", 
default_port=3666
"""
"""
Скорее всего вам потребуется знать у адреса UTXO для формирования транзакции. Они
доступны по адресу https://bcschain.info/api/address/ваш_адрес/utxo
"""
"""
to: [{'transactionId': 'c90b13e6e6e837ebbcb31c1cadfcd57f5f947b37f0758451654723e187bd9d4c', 
'outputIndex': 0, 'scriptPubKey': 
'76a9143ef3c8c0613993ad14710627f1c2731fe8741a4288ac', 
'address': 'BABwZ2m2egkav6Rdaphw8pddU9hQ1eHKZJ', 'value': 10000000000, 
'isStake': False, 'blockHeight': 458803, 'confirmations': 963}]
"""


class RPCConnect:

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.psw = password

    def _send_request(self, command):
        return requests.post(self.ip, auth=(self.user, self.psw), data={"method": command})

    def check_connection(self):
        response = self._send_request("getblockchaininfo")
        return response.json()['result']

    def get_new_addr(self):
        response = self._send_request("getnewaddress")
        res_json = response.json()
        if res_json['error']:
            return res_json['error']
        return ['result']


class CoinManage:
    @staticmethod
    def create_bcs_network():
        return create_bitcoinish_network(symbol='', network_name='', subnet_name='',
                                         wif_prefix_hex="80", address_prefix_hex="19", pay_to_script_prefix_hex="32",
                                         bip32_prv_prefix_hex="0488ade4", bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",
                                         bip49_prv_prefix_hex="049d7878", bip49_pub_prefix_hex="049D7CB2",
                                         bip84_prv_prefix_hex="04b2430c", bip84_pub_prefix_hex="04B24746",
                                         magic_header_hex="F1CFA6D3", default_port=3666)

    @staticmethod
    def get_utxo(wallet_addr):
        res_json = requests.get(f"https://bcschain.info/api/address/{wallet_addr}/utxo").json()
        return res_json

    @staticmethod
    def create_spendable(coin_value, script, tx_hash, tx_out_index):
        # return Spendable(coin_value, script, tx_hash, tx_out_index)
        return dict(
                    coin_value=coin_value,
                    script_hex=script,
                    tx_hash_hex=tx_hash,
                    tx_out_index=tx_out_index,
                    block_index_available=0,
                    does_seem_spent=False,
                    block_index_spent=0
                )

    @classmethod
    def get_spendables_from_utxo(cls, wallet_addr):
        utxo = cls.get_utxo(wallet_addr)
        spendables = []
        for tx in utxo:
            spendables.append(cls.create_spendable(tx["value"], tx["scriptPubKey"], tx["transactionId"], tx["outputIndex"]))

        return spendables

    @staticmethod
    def create_signed_tx(network, spendables: list, address_to: str, value: int, wifs: list) -> Tx:
        """wifs - list with private keys"""
        return create_signed_tx(network, spendables, [(address_to, value)], wifs)
