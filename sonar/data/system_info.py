import re


class SystemInfo(object):

    def __init__(self, sonar):
        self.sonar = sonar
        web, compute, search = get_system_data(sonar)
        self.web = web
        self.compute = compute
        self.search = search

    def get_total_threads(self, obj):
        if obj == 'web':
            return self.web['threads']
        if obj == 'compute':
            return self.compute['threads']
        return 0

    def get_max_memory(self, obj):
        if obj == 'web':
            return self.web['memory']['max']
        if obj == 'compute':
            return self.compute['memory']['max']
        return None

    def get_free_memory(self, obj):
        if obj == 'web':
            return self.web['memory']['free']
        if obj == 'compute':
            return self.compute['memory']['free']
        return None

    def get_disk_available(self):
        return self.search['disk_available']

    def get_max_file_desc(self):
        return self.search['file_descriptors']['max']

    def get_open_file_desc(self):
        return self.search['file_descriptors']['open']


def get_system_data(sonar):
    api = '/api/system/info'
    url = sonar.server + api

    # init result
    web = {}
    compute = {}
    search = {}

    response = sonar.req.do_get(url)

    if response.status_code != 200:
        print(f'Received non-200 status code while requesting {api} : {response.status_code} - {response.text}')
        return web, compute, search

    raw_data = response.json()

    web_source = raw_data['Web JVM State']
    web['memory'] = {}
    web['threads'] = web_source['Threads']
    web['memory']['max'] = web_source['Max Memory (MB)'] \
        * 1024 * 1024
    web['memory']['free'] = web_source['Free Memory (MB)'] \
        * 1024 * 1024

    compute_source = raw_data['Compute Engine JVM State']
    compute['memory'] = {}
    compute['threads'] = compute_source['Threads']
    compute['memory']['max'] = \
        compute_source['Max Memory (MB)'] * 1024 * 1024
    compute['memory']['free'] = \
        compute_source['Free Memory (MB)'] * 1024 * 1024

    search_source = raw_data['Search State']
    search['disk_available'] = convert(search_source['Disk Available'])
    search['file_descriptors'] = {}
    search['file_descriptors']['open'] = \
        search_source['Open File Descriptors']
    search['file_descriptors']['max'] = \
        search_source['Max File Descriptors']

    return web, compute, search


def convert(string):
    value = re.search(r'([0-9]+)', string)
    unit = re.search(r'([A-Z]?B)', string)

    num = int(value.group())
    unit = unit.group()
    if unit == 'B':
        return num
    num *= 1024

    if unit == 'KB':
        return num
    num *= 1024

    if unit == 'MB':
        return num
    num *= 1024

    if unit == 'GB':
        return num
    num *= 1024

    if unit == 'TB':
        return num
