import numpy as np


class DevData(object):
    def __init__(self, mac, desc, isiot):
        self.mac = mac
        self.desc = desc
        self.isiot = int(isiot)


class DevFeatures(DevData):
    def __init__(self, mac, desc, isiot):
        super(DevFeatures, self).__init__(mac, desc, isiot)
        self.eth = 0
        self.hostname = []
        self.vendor_class = []
        self.req_lst = []
        self.mds = []
        self.msg_t = []
        self.client_id = []


    @staticmethod
    def copy_from_devdata(devs):
        res = {}
        for dev in devs.values():
            df = DevFeatures(dev.mac, dev.desc, dev.isiot)
            res[dev.mac] = df
        return res


def add(st, delim=','):
    return delim + str(st)


def format_lst(lst):
    return str(lst).replace(',', ';').replace('[', '').replace(']', '')


def is_mac_valid(mac):
    bytes = None
    if ':' in mac:
        bytes = mac.split(':')
    elif '-' in mac:
        bytes = mac.split('-')
    else:
        return False
        #raise NotImplementedError('Unsupported MAC address type')

    if len(bytes) != 6:
        return False
        #raise ValueError('Bad MAC format')

    for byte in bytes:
        try:
            int(byte, 16)
        except ValueError as ve:
            return False
            #raise ve
    return True


def sanitize_domain(dom, domain_lables):
    splt = dom.split('.')
    dl = domain_lables + 1  ## include '.'
    if len(splt) > dl:
        dom = '.'.join(splt[-dl:])
    return dom


def get_ua(payload):
    if not (payload[:4] == 'GET ' or payload[:5] == 'POST '):
        return None
    lines = payload.split('\r\n')
    ua = ''
    for ln in lines:
        if 'user-agent' in ln.lower():
            ua_ln = ln.split(' ')
            if len(ua_ln) > 1:
                ua = ' '.join(ln.split(' ')[1:])
    return str(ua)

