

USER_PAGE_SIZE = 500
TASK_PAGE_SIZE = 999
STATUS_LABELS_STR_GROUP = {
    'static': 'SUCCESS,FAILED,CANCELED',
    'dynamic': 'PENDING,IN_PROGRESS'
}
STATUS_LABELS_STR = STATUS_LABELS_STR_GROUP['static'] \
                + STATUS_LABELS_STR_GROUP['dynamic']
STATUS_LABELS_LIST_GROUP = {
    'static': [
        'SUCCESS',
        'FAILED',
        'CANCELED'
    ],
    'dynamic': [
        'PENDING',
        'IN_PROGRESS'
    ]
}
STATUS_LABELS_LIST = STATUS_LABELS_LIST_GROUP['static'] \
                + STATUS_LABELS_LIST_GROUP['dynamic']


class Administrator(object):

    def __init__(self, sonar):
        self.sonar = sonar
        list_tasks, \
            task_info, \
            task_status = get_list_tasks(sonar)
        list_users, \
            user_info, \
            list_groups, \
            group_info = get_list_users(sonar)

        self.list_tasks = list_tasks
        self.task_info = task_info
        self.task_status = task_status
        self.list_users = list_users
        self.user_info = user_info
        self.list_groups = list_groups
        self.group_info = group_info

    def get_list_tasks(self):
        return self.list_tasks

    def get_total_tasks(self):
        return len(self.get_list_tasks())

    def get_task(self, task_id):
        return self.task_info[task_id]

    def get_total_status(self, status):
        if status in self.task_status:
            return self.task_status[status]['total']
        return 0

    def get_status_labels(self):
        return STATUS_LABELS_LIST

    def get_status_tasks(self, status='all'):
        if status == 'all':
            res = []
            for stt in STATUS_LABELS_LIST:
                res += self.task_status[stt]['tasks']
            return res
        if status in self.task_status:
            return self.task_status[status]['tasks']
        return []

    def get_task_status(self, task_id):
        task = self.get_task(task_id)
        return task['status']

    def get_task_component_name(self, task_id):
        task = self.get_task(task_id)
        return task['component_name']

    def get_execution_time_seconds(self, task_id):
        task = self.get_task(task_id)
        return task['execution_time']

    def get_list_users(self):
        return self.list_users

    def get_list_groups(self):
        return self.list_groups

    def get_user(self, user_id):
        return self.user_info[user_id]

    def get_group(self, gr_name):
        return self.group_info[gr_name]

    def get_total_users(self):
        return len(self.get_list_users())

    def get_total_groups(self):
        return len(self.get_list_groups())

    def get_group_total_users(self, gr_name):
        return len(self.get_group_users(gr_name))

    def get_group_users(self, gr_name):
        group = self.get_group(gr_name)
        return group['users']


# Get list tasks
def get_list_tasks(sonar):

    list_tasks = []
    task_info = {}
    task_status = {}

    list_tasks_static, \
        task_info_static, \
        task_status_static = get_list_tasks_status(sonar, 'static')
    list_tasks_dynamic, \
        task_info_dynamic, \
        task_status_dynamic = get_list_tasks_status(sonar, 'dynamic')

    list_tasks = list_tasks_static
    list_tasks += list_tasks_dynamic
    task_info = task_info_static
    task_info.update(task_info_dynamic)
    task_status = task_status_static
    task_status.update(task_status_dynamic)

    return list_tasks, task_info, task_status


# Get list tasks had status in status group
def get_list_tasks_status(sonar, status_group):

    list_tasks = []
    task_info = {}
    task_status = {}

    for status in STATUS_LABELS_LIST_GROUP[status_group]:
        task_status[status] = {
            'total': 0,
            'tasks': []
        }

    api = '/api/ce/activity'
    status_components = STATUS_LABELS_STR_GROUP[status_group]
    if status_group == 'static':
        only_currents = 'true'
    else:
        only_currents = 'false'

    params = {
        'ps': TASK_PAGE_SIZE,
        'status': status_components,
        'onlyCurrents': only_currents
    }
    url = sonar.server + api

    response = sonar.req.do_get(url, params=params)
    if response.status_code != 200:
        return list_tasks, task_info, task_status

    raw_data = response.json()
    tasks = raw_data['tasks']

    for task in tasks:
        new_task = standardize_task_info(task, sonar)
        task_id = new_task['id']
        list_tasks.append(task_id)
        task_info[task_id] = new_task
        task_status[new_task['status']]['total'] += 1
        task_status[new_task['status']]['tasks'].append(task_id)

    return list_tasks, task_info, task_status


def standardize_task_info(task, collector):

    new_task = {}

    new_task['id'] = task['id']
    new_task['type'] = task['type']
    new_task['component_id'] = task['componentId'] \
        if 'componentId' in task else 'N/A'
    new_task['component_key'] = task['componentKey'] \
        if 'componentKey' in task else 'N/A'
    new_task['component_name'] = task['componentName'] \
        if 'componentName' in task else 'N/A'
    new_task['component_qualifier'] = task['componentQualifier'] \
        if 'componentQualifier' in task else 'N/A'
    new_task['status'] = task['status']
    if 'executionTimeMs' in task:
        new_task['execution_time'] = task['executionTimeMs'] / 1000
    else:
        new_task['execution_time'] = 0

    return new_task


# Get list user and group
def get_list_users(sonar):

    api = '/api/users/search'
    url = sonar.server + api

    list_users = []
    user_info = {}
    list_groups = []
    group_info = {}

    response = sonar.req.do_get(url)
    if response.status_code != 200:
        return list_users, user_info, list_groups, group_info

    raw_data = response.json()

    paging = raw_data['paging']
    users_total = paging['total']
    page_size = USER_PAGE_SIZE
    page_total = users_total // page_size
    if users_total % page_size > 0:
        page_total += 1

    for page in range(page_total):
        p = page + 1
        params = {'ps': page_size, 'p': p}

        response = sonar.req.do_get(url, params=params)
        if response.status_code != 200:
            continue

        page_data = response.json()

        users = page_data['users']
        for user in users:
            new_user = standardize_user_info(user, sonar)
            user_id = new_user['id']
            user_info[user_id] = new_user
            list_users.append(user_id)

            groups = new_user['groups']
            if groups is None:
                continue
            else:
                for gr_name in groups:
                    if gr_name in group_info:
                        group_info[gr_name]['total'] += 1
                    else:
                        list_groups.append(gr_name)
                        group_info[gr_name] = {}
                        group_info[gr_name]['total'] = 1
                        group_info[gr_name]['users'] = []
                    group_info[gr_name]['users'].append(user_id)
    return list_users, user_info, list_groups, group_info


def standardize_user_info(user, sonar):
    new_user = {}

    new_user['id'] = user['login']
    new_user['name'] = user['name']
    new_user['active'] = user['active'] \
        if 'active' in user else None
    if 'email' in user:
        new_user['email'] = user['email']
    else:
        new_user['email'] = None
    if 'groups' in user:
        new_user['groups'] = user['groups']
    else:
        new_user['groups'] = None

    return new_user
