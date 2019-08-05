from prometheus_client.core import GaugeMetricFamily

def make_metrics(projects):

    list_metrics = []

    # Total projects
    metric = GaugeMetricFamily('sonar_projects_total',
                            'Total projects in Sonar',
                            labels=None)
    metric.add_metric(labels=[], value=projects.get_total_projects())
    list_metrics.append(metric)

    # group metric status
    list_status_label = projects.get_status_labels()
    for status in list_status_label:
        metric = GaugeMetricFamily('sonar_projects_{}'.format(status.lower()),
                            'Number {} project in Sonar'.format(status),
                            labels=None)
        metric.add_metric(labels=[], value=projects.get_total_status(status))
        list_metrics.append(metric)
    
    return list_metrics
