import requests
import json
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_signed_tx
from pycoin.coins.Tx import Tx
from django.conf import settings


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


class RPCConnect:

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.psw = password

    def _send_request(self, command, params: list = None):
        data = {"method": command}
        if params:
            data["params"] = params
        res_json = requests.post(self.ip, auth=(self.user, self.psw), data=json.dumps(data)).json()
        if res_json['error']:
            print(res_json['error'])
            return None
        return res_json['result']

    def check_connection(self):
        response = self._send_request("getblockchaininfo")
        return response.json()['result']

    def get_new_addr(self):
        result = self._send_request("getnewaddress")
        return result

    def send_singned_tx(self, hex_signed_tx):
        result = self._send_request("sendrawtransaction", params=[hex_signed_tx])
        return result


class CoinManage:
    api_endpoint = "https://bcschain.info/api/"

    @staticmethod
    def create_bcs_network():
        return create_bitcoinish_network(symbol='', network_name='', subnet_name='',
                                         wif_prefix_hex="80", address_prefix_hex="19", pay_to_script_prefix_hex="32",
                                         bip32_prv_prefix_hex="0488ade4", bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",
                                         bip49_prv_prefix_hex="049d7878", bip49_pub_prefix_hex="049D7CB2",
                                         bip84_prv_prefix_hex="04b2430c", bip84_pub_prefix_hex="04B24746",
                                         magic_header_hex="F1CFA6D3", default_port=3666)

    @classmethod
    def get_utxo(cls, wallet_addr):
        res_json = requests.get(f"{cls.api_endpoint}address/{wallet_addr}/utxo").json()
        return res_json

    @staticmethod
    def create_spendable(coin_value, script, tx_hash, tx_out_index):
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

    @classmethod
    def create_signed_tx(cls, network, address_from: str, address_to: str, value: int, wifs: list) -> Tx:
        """wifs - list with private keys"""
        spendables = cls.get_spendables_from_utxo(address_from)
        return create_signed_tx(network, spendables, [(address_to, value), address_from], wifs, fee=int(value/1000))

    @classmethod
    def send_tx(cls, hex_signed_tx):  # return 403 Forbidden. Why??
        return requests.post(f"{cls.api_endpoint}tx/send", data=json.dumps({"rawtx": hex_signed_tx}))

    @classmethod
    def get_wallet_transactions(cls, wallet_addr):
        res_json = requests.get(f"{cls.api_endpoint}address/{wallet_addr}").json()
        return res_json['transactions']


def create_and_send_bcs_tx():
    rpc = RPCConnect(bcs_ip, bcs_user, bcs_psw)
    addr_to = rpc.get_new_addr()
    network = CoinManage.create_bcs_network()
    signed_tx = CoinManage.create_signed_tx(network, wallet, addr_to, 1e8, [w_prv])
    sended_tx = rpc.send_singned_tx(signed_tx.as_hex())


if __name__ == '__main__':
    rpc = RPCConnect(bcs_ip, bcs_user, bcs_psw)
    # print(rpc.check_connection())
    addr_to = rpc.get_new_addr()
    print(f"addr_to: {addr_to}")
    network = CoinManage.create_bcs_network()
    print(f"{network=}")
    signed_tx = CoinManage.create_signed_tx(network, wallet, addr_to, 1e8, [w_prv])
    print(f"{signed_tx=}")
    print(f'hex: {signed_tx.as_hex()}')
    sended_tx = rpc.send_singned_tx(signed_tx.as_hex())
    print(f"{sended_tx=}")  # = "aafc06d1c0b8e4658ff3c39b388ffbe05f9a552e9b7de8e668ab38a121194eb9"



