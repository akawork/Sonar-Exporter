import os
import sys

sys.path.append(os.path.abspath('.'))

from sonar.data.projects import Projects
from sonar.data.administrator import Administrator
from sonar.data.quality_profiles import QualityProfiles
from sonar.data.system_info import SystemInfo

from sonar.metrics import project_metrics
from sonar.metrics import administrator_metrics
from sonar.metrics import quality_profile_metrics
from sonar.metrics import system_metrics

from sonar.connection.api_connection import APIConnection

class Sonar(object):

    def __init__(self, server, auth, insecure=True):
        self.server = server
        self.auth = auth
        self.req = APIConnection(server, auth)
        self.projects = Projects(self)
        self.administrator = Administrator(self)
        self.quality_profiles = QualityProfiles(self)
        self.system_info = SystemInfo(self)


class SonarCollector(object):

    def __init__(self, server, user, passwd, insecure=True):
        self.server = server
        self.insecure = insecure
        self.auth = (user, passwd)
        

    def collect(self):
        sonar = Sonar(server=self.server,
                        auth=self.auth,
                        insecure=True)

        sonar_metrics = SonarMetrics(sonar)
        metrics = sonar_metrics.make_metrics()

        for metric in metrics:
            yield metric
        


class SonarMetrics(object):

    def __init__(self, sonar):
        self.sonar = sonar
        self.metrics = []

    def make_metrics(self):
        metrics = []

        metrics += project_metrics.make_metrics(self.sonar.projects)
        metrics += administrator_metrics.make_metrics(self.sonar.administrator)
        metrics += quality_profile_metrics.make_metrics(self.sonar.quality_profiles)
        metrics += system_metrics.make_metrics(self.sonar.system_info)

        self.metrics = metrics

        return self.metrics


