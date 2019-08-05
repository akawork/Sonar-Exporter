

PROJECT_PAGE_SIZE = 500
DEFAULT_TEMPLATE_ID = 'default_template'
PROJECT_STATUS = ['ERROR', 'OK', 'WARN', 'NONE', 'ACCESS_DENIED']


class Projects(object):

    def __init__(self, sonar):
        self.sonar = sonar
        list_projects, project_info, list_status = get_list_projects(sonar)
        self.list_projects = list_projects
        self.project_info = project_info
        self.list_status = list_status

    def get_list_projects(self):
        return self.list_status

    def get_total_projects(self):
        return len(self.list_projects)

    def get_project_info(self, prj_id):
        return self.project_info[prj_id]

    def get_project_status(self, prj_id):
        prj = self.get_project_info(prj_id)
        return prj['status']

    def get_total_status(self, status):
        if status in self.list_status:
            return self.list_status[status]['total']
        return 0
    
    def get_list_status(self, status='all'):
        if status == 'all':
            res = []
            for stt in PROJECT_STATUS:
                res += self.list_status[stt]['projects']
            return res
        if status in self.list_status:
            return list_status[status]['projects']
        return []

    def get_status_labels(self):
        return PROJECT_STATUS

# Get list projects
def get_list_projects(sonar):

    api = '/api/projects/search'
    url = sonar.server + api

    projects = []
    project_info = {}
    list_status = {}

    for status in PROJECT_STATUS:
        list_status[status] = {'total': 0, 'projects': []}

    response = sonar.req.do_get(url)
    if response.status_code != 200:
        return projects, project_info, list_status

    raw_data = response.json()

    paging = raw_data['paging']
    projects_total = paging['total']
    page_size = PROJECT_PAGE_SIZE
    page_total = projects_total // page_size
    if projects_total % page_size > 0:
        page_total += 1

    for page in range(page_total):
        p = page + 1
        params = {'ps': page_size, 'p': p}
        
        response = sonar.req.do_get(url, params=params)
        if response.status_code != 200:
            continue

        page_data = response.json()

        components = page_data['components']
        for project in components:
            new_project = standardize_project_info(project, sonar)
            
            projects.append(new_project['id'])
            project_info[new_project['id']] = new_project
            status = new_project['status']
            list_status[status]['total'] += 1
            list_status[status]['projects'].append(new_project['id'])
    
    return projects, project_info, list_status

def standardize_project_info(project, sonar):

    new_project = {}
    new_project['organization'] = project['organization']
    new_project['id'] = project['id']
    new_project['key'] = project['key']
    new_project['name'] = project['name']
    new_project['qualifier'] = project['qualifier']
    new_project['visibility'] = project['visibility']
    # new_project['lastAnalysisDate'] = project['lastAnalysisDate']
       
    api = '/api/qualitygates/project_status'
    url = sonar.server + api

    project_key = project['key']
    params = {'projectKey': project_key}

    response = sonar.req.do_get(url=url, params=params)
    raw_data = response.json()

    if 'errors' in raw_data:
        new_project['status'] = 'ACCESS_DENIED'
        return new_project
        # apply_permission(sonar, project_id=project['id'])
        
    response = sonar.req.do_get(url=url, params=params)
    raw_data = response.json()

    status = raw_data['projectStatus']['status']
    
    new_project['status'] = status

    return new_project
