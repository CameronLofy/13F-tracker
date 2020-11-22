import json
import urllib.request
import urllib.parse

'''
See https://www.openfigi.com/api for more information.
'''

openfigi_apikey = ''  # Put API Key here
jobs = [
    {'idType': 'ID_CUSIP', 'idValue': '466367109'},
    {'idType': 'ID_CUSIP', 'idValue': 'N00985106'},
    {'idType': 'ID_CUSIP', 'idValue': '00187Y100'},
    {'idType': 'ID_CUSIP', 'idValue': '049164205'},
    {'idType': 'ID_CUSIP', 'idValue': '88160R101'},
    {'idType': 'ID_NAME', 'idValue': '88160R101'}
]


def map_jobs(jobs):
    '''
    Send an collection of mapping jobs to the API in order to obtain the
    associated FIGI(s).
    Parameters
    ----------
    jobs : list(dict)
        A list of dicts that conform to the OpenFIGI API request structure. See
        https://www.openfigi.com/api#request-format for more information. Note
        rate-limiting requirements when considering length of `jobs`.
    Returns
    -------
    list(dict)
        One dict per item in `jobs` list that conform to the OpenFIGI API
        response structure.  See https://www.openfigi.com/api#response-fomats
        for more information.
    '''
    handler = urllib.request.HTTPHandler()
    opener = urllib.request.build_opener(handler)
    openfigi_url = 'https://api.openfigi.com/v2/mapping'
    request = urllib.request.Request(openfigi_url, data=bytes(json.dumps(jobs), encoding='utf-8'))
    request.add_header('Content-Type','application/json')
    if openfigi_apikey:
        request.add_header('X-OPENFIGI-APIKEY', openfigi_apikey)
    request.get_method = lambda: 'POST'
    connection = opener.open(request)
    if connection.code != 200:
        raise Exception('Bad response code {}'.format(str(response.status_code)))
    return json.loads(connection.read().decode('utf-8'))


def job_results_handler(jobs, job_results):
    '''
    Handle the `map_jobs` results.  See `map_jobs` definition for more info.
    Parameters
    ----------
    jobs : list(dict)
        The original list of mapping jobs to perform.
    job_results : list(dict)
        The results of the mapping job.
    Returns
    -------
        None
    '''
    for job, result in zip(jobs, job_results):
        job_str = '|'.join(job.values())
        figis_str = ','.join([d['ticker'] for d in result.get('data', [])])
        result_str = figis_str or result.get('error')
        output = '%s maps to FIGI(s) ->\n%s\n---' % (job_str, result_str)
        print(output)


def main():
    '''
    Map the defined `jobs` and handle the results.
    Returns
    -------
        None
    '''
    job_results = map_jobs(jobs)
    job_results_handler(jobs, job_results)

main()