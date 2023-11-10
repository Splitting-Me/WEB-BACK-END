# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from pydash import get
from web3 import Web3
from exceptions.referral import InvalidSignature
from lib import dt_utcnow

w3 = Web3(Web3.HTTPProvider(""))


class WalletHelper:

    @staticmethod
    def get_address_of(signature, msg):

        mesage= encode_defunct(text=msg)
        _address = w3.eth.account.recover_message(mesage,signature=HexBytes(signature))
      
        return _address

    @staticmethod
    def _get_sign_msg(address, nonce):
        return f"I'm signing to Splitting Me using nonce {nonce} at address {address}"

    @staticmethod
    def _get_referral_sign_msg(address, nonce, ref_code):
        return f"I input referral code to Splitting Me with code {ref_code} and nonce {nonce} at address {address}"
        

    @classmethod
    def get_sign_msg(cls, address):
        _nonce = cls.get_nonce()
        return cls._get_sign_msg(address=address, nonce=_nonce), _nonce

    @staticmethod
    def get_nonce():
        return int(dt_utcnow().timestamp())

    @classmethod
    def get_referral_sign_msg(cls, address, ref_code):
        _nonce = cls.get_nonce()
        return cls._get_referral_sign_msg(address=address, nonce=_nonce, ref_code=ref_code), _nonce
        