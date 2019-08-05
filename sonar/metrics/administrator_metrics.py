
from prometheus_client.core import GaugeMetricFamily

def make_metrics(admin):

    list_metrics = []
    
    # Total users
    metric = GaugeMetricFamily('sonar_users_total',
                            'Total users in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=admin.get_total_users())
    list_metrics.append(metric)

    # Total groups
    metric = GaugeMetricFamily('sonar_groups_total',
                            'Total groups in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=admin.get_total_groups())
    list_metrics.append(metric)

    # Total users in a group
    metric = GaugeMetricFamily('sonar_group_users_total',
                            'Total user in a group in Sonar',
                            labels=['gr_name'])
    list_groups = admin.get_list_groups()
    for gr_name in list_groups:
        metric.add_metric(labels=[gr_name],
                        value=admin.get_group_total_users(gr_name))

    list_metrics.append(metric)

    #---------------task
    # Total tasks
    metric = GaugeMetricFamily('sonar_tasks_total',
                            'Total tasks in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=admin.get_total_tasks())
    list_metrics.append(metric)

    # task status
    list_status_labels = admin.get_status_labels()
    for status in list_status_labels:
        metric = GaugeMetricFamily('sonar_tasks_{}'.format(status.lower()),
                                'Number {} tasks in Sonar'.format(status),
                                labels=None)
        metric.add_metric(labels=[],
                        value=admin.get_total_status(status))
        list_metrics.append(metric)

    # Execution time of a task
    metric = GaugeMetricFamily('sonar_task_execution_time_second',
                            'Execution time of a task in Sonar',
                            labels=['task_id',
                                    'component_name',
                                    'task_status'])
    list_tasks = admin.get_list_tasks()
    for task_id in list_tasks:
        task_status = admin.get_task_status(task_id)
        exec_time = admin.get_execution_time_seconds(task_id)
        component_name = admin.get_task_component_name(task_id)
        metric.add_metric(labels=[task_id, component_name, task_status], 
                        value=exec_time)

    list_metrics.append(metric)

    return list_metrics


