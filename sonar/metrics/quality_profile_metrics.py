from prometheus_client.core import GaugeMetricFamily


def make_metrics(profiles):

    list_metrics = []

    # Total profiles in Sonar
    metric = GaugeMetricFamily(
        'sonar_profiles_total',
        'Total profiles in  Sonar',
        labels=None
    )

    metric.add_metric(
        labels=[],
        value=profiles.get_total_profiles()
    )

    list_metrics.append(metric)

    # Total languages in Sonar
    metric = GaugeMetricFamily(
        'sonar_languages_total',
        'Total languages in Sonar',
        labels=None
    )

    metric.add_metric(
        labels=[],
        value=profiles.get_total_languages()
    )

    list_metrics.append(metric)

    # Total profiles in each language
    metric = GaugeMetricFamily(
        'sonar_language_profiles_total',
        'Total profiles in each language Sonar',
        labels=['language']
    )

    list_languages = profiles.get_list_languages()
    for lang in list_languages:
        lang_key = lang['key']
        metric.add_metric(
            labels=[lang_key],
            value=profiles.get_language_total_profiles(lang_key)
        )

    list_metrics.append(metric)

    return list_metrics
