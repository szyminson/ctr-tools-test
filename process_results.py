#!/usr/bin/env python

from os import scandir, path
from json import load
import seaborn as sns
from pandas import DataFrame
from slugify import slugify

results_dir = 'results'
host_results_path = 'tmp/ctr-tools-test'
tools = ['docker', 'podman']

def load_host_results(host: str):
    full_result_path = path.join(results_dir, host, host_results_path)
    host_results = {}
    for tool in tools:
        tool_result_file = path.join(full_result_path, tool, 'latest.json')
        with open(tool_result_file) as f:
            host_results[tool] = load(f)
    return host_results

def parse_results(results: dict):
    parsed_data = {}
    for host, host_results in results.items():
        for tool, tool_results in host_results.items():
            for _, test_results in tool_results['results'].items():
                system_key = list(test_results['results'])[0]
                scale = test_results['scale']
                test_name = ' '.join((test_results['title'], test_results['description']))
                if not test_name in parsed_data:
                    parsed_data[test_name] = {
                        'scale': scale,
                        'data': [['host', 'tool', 'value']]
                    }
                system_test_results = test_results['results'][system_key]
                if 'raw_values' in system_test_results:
                    for value in system_test_results['raw_values']:
                        parsed_data[test_name]['data'].append([host, tool, value])
    return parsed_data

def parsed_to_plots(results: dict):
    sns.set_theme(style="whitegrid")
    for test, test_results in results.items():
        df = DataFrame(test_results['data'][1:], columns=test_results['data'][0])
        g = sns.catplot(data=df, kind='bar', x='host', y='value', hue='tool', palette='dark', alpha=0.6)
        g.set_axis_labels('', test_results['scale'])
        g.fig.suptitle(test)
        g.fig.savefig(path.join('plots', slugify(test) + '.png'))



if __name__ == '__main__':
    results = dict((host.name, load_host_results(host.name)) for host in scandir(results_dir))
    parsed = parse_results(results)
    parsed_to_plots(parsed)
