
class QualityProfiles(object):

    def __init__(self, sonar):
        self.sonar = sonar
        profiles, profile_info, languages, language_info = \
            get_list_profiles(sonar)
        self.list_profiles = profiles
        self.list_languages = languages
        self.profile_info = profile_info
        self.language_info = language_info

    def get_list_profiles(self):
        return self.list_profiles
    
    def get_total_profiles(self):
        return len(self.get_list_profiles())

    def get_profile(self, prf_key):
        return self.profile_info[prf_key]

    def get_list_languages(self):
        return self.list_languages

    def get_total_languages(self):
        return len(self.get_list_languages())

    def get_language(self, lang_key):
        return self.language_info[lang_key]

    def get_language_total_profiles(self, lang_key):
        return self.language_info[lang_key]['total']

def get_list_profiles(sonar):

    api = '/api/qualityprofiles/search'
    url = sonar.server + api

    profiles = []
    profile_info = {}
    languages = []
    language_info = {}

    response = sonar.req.do_get(url)
    if response.status_code != 200:
        return profiles, profile_info, languages, language_info

    raw_data = response.json()

    list_profiles = raw_data['profiles']
    for profile in list_profiles:
        new_profile = standardize_profile_info(profile, sonar)
        profiles.append(new_profile['key'])
        profile_info[new_profile['key']] = new_profile
        lang = {}
        lang['key'] = profile['language']
        lang['name'] = profile['languageName']
        if lang['key'] in language_info:
            language_info[lang['key']]['total'] += 1
        else:
            # Not yet had this language
            languages.append(lang)
            language_info[lang['key']] = {}
            language_info[lang['key']]['key'] = lang['key']
            language_info[lang['key']]['total'] = 1
            language_info[lang['key']]['profiles'] = []
        language_info[lang['key']]['profiles'].append(new_profile['key'])
    
    return profiles, profile_info, languages, language_info

def standardize_profile_info(profile, sonar):

    new_profile = {}

    new_profile['key'] = profile['key']
    new_profile['name'] = profile['name']
    new_profile['language'] = profile['language']
    

    return new_profile