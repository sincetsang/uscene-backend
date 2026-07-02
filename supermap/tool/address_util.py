
class AddressUtil(object):

    @classmethod
    def address_add_0x_and_lower(cls, address):
        if len(address) == 0:
            return address
        if address.startswith('0x'):
            return address.lower()
        return '0x' + address.lower()

    @classmethod
    def add_mark(cls, address):
        if len(address) < 10:
            return address
        return address[:6] + '...' + address[-4:]
