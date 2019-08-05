from prometheus_client.core import GaugeMetricFamily

def make_metrics(system_info):

    list_metrics = []

    metric = GaugeMetricFamily('sonar_system_web_memory_max',
                            'Max memory of Web JVM state in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_max_memory('web'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_compute_memory_max',
                            'Max memory of Compute Engine JVM State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_max_memory('compute'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_web_memory_free',
                            'Free memory of Web JVM state in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_free_memory('web'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_compute_memory_free',
                            'Free memory of Compute Engine JVM State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_free_memory('compute'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_web_threads',
                            'Threads of Web JVM state in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_total_threads('web'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_compute_threads',
                            'Threads of Compute Engine JVM State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_total_threads('compute'))
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_search_file_desc_open',
                            'Open File Descriptors of Search State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_open_file_desc())
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_search_file_desc_max',
                            'Max File Descriptors of Search State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_max_file_desc())
    list_metrics.append(metric)

    metric = GaugeMetricFamily('sonar_system_search_disk_available',
                            'Disk Available of Search State in Sonar',
                            labels=None)
    metric.add_metric(labels=[],
                    value=system_info.get_disk_available())
    list_metrics.append(metric)

    return list_metrics
