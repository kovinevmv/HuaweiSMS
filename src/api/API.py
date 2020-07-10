import re

import requests
import xmltodict

from src.cache.logger import Logger
from src.config import connectionConfig

mapAPI = {
    'auth': '/html/index.html',
    'get_token': '/html/smsinbox.html',
    'get_sms': '/api/sms/sms-list',
    'is_new_sms': '/api/monitoring/check-notifications',
    'set_read': '/api/sms/set-read',
    'device': '/api/device/information',
    'status': '/api/monitoring/status',
    'plmn': '/api/net/current-plmn'
}

mapPostData = {
    'get_sms':
        '<?xml version="1.0" encoding="UTF-8"?>\
        <request>\
        <PageIndex>1</PageIndex>\
        <ReadCount>{}</ReadCount>\
        <BoxType>1</BoxType>\
        <SortType>0</SortType>\
        <Ascending>0</Ascending>\
        <UnreadPreferred>0</UnreadPreferred>\
        </request>',
    'send_read':
        '<?xml version="1.0" encoding="UTF-8"?>\
        <request>\
        <Index>{}</Index>\
        </request>'
}

mapSignal = {
    '0': 'no-service',
    '1': 'GSM',
    '2': 'GPRS (2G)',
    '3': 'EDGE (2.5G)',
    '4': 'WCDMA (3G)',
    '5': 'HSDPA (Turbo 3g)',
    '6': 'HSUPA (Turbo 3g plus)',
    '7': 'HSPA',
    '8': 'TDSCDMA',
    '9': 'HSPA+',
    '10': 'EVDO_REV_0',
    '11': 'EVDO_REV_A',
    '12': 'EVDO_REV_B',
    '13': '1xRTT',
    '14': 'UMB',
    '15': '1xEVDV',
    '16': '3xRTT',
    '17': 'HSPA+64QAM',
    '18': 'HSPA+MIMO',
    '19': 'LTE (4G)'
}


class API:
    def __init__(self):
        self.base_url = connectionConfig.HOST_API
        self.cached_messages = []

        self.session = None
        self.token = ''
        self._auth()

    @property
    def headers(self):
        return {'__RequestVerificationToken': self.token}

    def _auth(self):
        self.session = requests.Session()
        self.session.get(self.base_url + mapAPI["auth"])
        self.token = self._get_csrf_token()[0]
        Logger.log(f'Auth end, token: {self.token}')

    def _get_csrf_token(self):
        response = self.session.get(self.base_url + mapAPI['get_token']).text
        regex = re.compile("\"([A-Za-z0-9+=/]{32})\"")
        return re.findall(regex, response)

    def _get_page(self, url):
        Logger.log(f'GET page: {url}')
        xml = self.session.get(url, headers=self.headers).content
        if xml:
            Logger.log('Successful GET')
            return xmltodict.parse(xml)
        Logger.log(f'Return xml: {xml}', 'error')

    def _post_page(self, url, data):
        Logger.log(f'POST page: {url} Data: {data}')
        xml = self.session.post(url, headers=self.headers, data=data).content
        if xml:
            Logger.log('Successful POST')
            return xmltodict.parse(xml)
        Logger.log(f'Return xml: {xml}', 'error')

    def get_sms(self, read_count='50'):
        Logger.log(f'Call GET SMS. Count: {read_count}')

        if self.cached_messages:
            Logger.log(f'Return cached SMS')
            return self.cached_messages

        url = self.base_url + mapAPI['get_sms']
        post_data = mapPostData['get_sms'].format(read_count)

        msgs = self._post_page(url, post_data)

        if 'response' in msgs:
            Logger.log(f'Successfully get new SMS')
            self.cached_messages = self._parse(msgs)
            return self.cached_messages
        else:
            Logger.log(f'No "response" in {msgs}', 'error')

    def is_new_sms_exists(self):
        Logger.log(f'Call check new messages')

        self._auth()
        page = self._get_page(self.base_url + mapAPI['is_new_sms'])
        if 'response' in page:
            if page['response']['UnreadMessage'] != '0':
                return True
        return False

    @staticmethod
    def _parse(data):
        sms_list = []
        msgs = data['response']['Messages']['Message']
        for msg in msgs:
            sms_list.append({
                'id': msg['Index'],
                'read': True if msg['Smstat'] == '1' else False,
                'sender': msg['Phone'],
                'msg': msg['Content'].replace('\n', ''),
                'date': msg['Date']
            })

        return sms_list

    def get_new_sms(self):
        Logger.log(f'Call get new messages')
        new_sms = []
        if self.is_new_sms_exists():
            msgs = self.get_sms()
            for msg in msgs:
                if not msg['read']:
                    new_sms.append(msg)
        return new_sms

    def set_read(self, index):
        Logger.log(f'Call set read message:', index)

        self._auth()
        url = self.base_url + mapAPI['set_read']
        data = mapPostData['send_read'].format(index)
        return self._post_page(url, data)

    def set_read_all(self):
        Logger.log(f'Call read all messages')

        for msg in self.get_new_sms():
            self.set_read(msg['id'])

    def get_device_info(self):
        Logger.log(f'Call get device info')
        url = self.base_url + mapAPI['device']
        return self._get_page(url)

    def _get_status(self):
        Logger.log(f'Call get status inner')
        url = self.base_url + mapAPI['status']
        return self._get_page(url)

    def get_status_network(self):
        Logger.log(f'Call get status')
        response = self._get_status()
        if 'response' in response:
            return {
                'connectionType': mapSignal[response['response']['CurrentNetworkType']],
                'signal': int(response['response']['SignalIcon']) / int(response['response']['maxsignal'])
            }

    def _get_plmn(self):
        Logger.log(f'Call get plmn inner')
        url = self.base_url + mapAPI['plmn']
        return self._get_page(url)

    def get_provider(self):
        Logger.log(f'Call get provider')
        response = self._get_plmn()
        if 'response' in response:
            return {
                'providerName': response['response']['FullName'],
            }

    def get_total_status(self):
        Logger.log(f'Call get total status')
        msgs = {'msgs': self.get_new_sms()}
        provider = self.get_provider()
        network_status = self.get_status_network()

        msgs.update(provider)
        msgs.update(network_status)

        return msgs



if __name__ == '__main__':
    pass
