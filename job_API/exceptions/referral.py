class InvalidNonce(Exception):
    def __init__(self, msg='Invalid nonce.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 406
        self.msg = msg
        self.errors = kwargs.get('errors', [{
            'nonce': 'Invalid'
        }])
        self.error_code = 'E_NONCE'

    pass
class InvalidSignature(Exception):
    def __init__(self, msg='Invalid signature.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 401
        self.msg = msg
        self.errors = kwargs.get('errors', [{
            'signature': 'Invalid'
        }])
        self.error_code = 'E_SIGNATURE'

    pass