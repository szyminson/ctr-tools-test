#!/usr/bin/env python

from os import scandir, path, makedirs
from json import load
import seaborn as sns
from pandas import DataFrame
from slugify import slugify
from tabulate import tabulate

results_dir = 'results'
host_results_path = 'tmp/ctr-tools-test'
processed_results_path = 'processed'
tools = ['docker', 'podman']


def load_host_results(host: str) -> dict:
    """Read single host results from files"""
    full_result_path = path.join(results_dir, host, host_results_path)
    host_results = {}
    for tool in tools:
        tool_result_file = path.join(full_result_path, tool, 'latest.json')
        with open(tool_result_file) as f:
            host_results[tool] = load(f)
    return host_results


def parse_results(results: dict) -> dict:
    """Extract needed data from results"""
    parsed_data = {}
    for host, host_results in results.items():
        for tool, tool_results in host_results.items():
            for _, test_results in tool_results['results'].items():
                system_key = list(test_results['results'])[0]
                scale = test_results['scale']
                test_name = ' '.join(
                    (test_results['title'], test_results['description']))
                if not test_name in parsed_data:
                    parsed_data[test_name] = {
                        'scale': scale,
                        'data': [['host', 'tool', 'value']]
                    }
                system_test_results = test_results['results'][system_key]
                if 'raw_values' in system_test_results:
                    for value in system_test_results['raw_values']:
                        parsed_data[test_name]['data'].append(
                            [host, tool, value])
    return parsed_data


def load_results() -> dict:
    """Load and parse all results"""
    results = dict((host.name, load_host_results(host.name))
                   for host in scandir(results_dir))
    return parse_results(results)


def process_results(results: dict):
    """Process loaded results to plots and latex tables"""
    makedirs(processed_results_path, exist_ok=True)
    for test, test_results in results.items():
        df = DataFrame(test_results['data'][1:],
                       columns=test_results['data'][0])
        render_plot(test, test_results['scale'], df)
        render_table(test, test_results['scale'], df.copy(deep=True))


def render_plot(name: str, scale: str, data: DataFrame):
    """Render and save single plot from given data"""
    sns.set_theme(style='whitegrid')
    g = sns.catplot(data=data, kind='bar', x='host', y='value',
                    hue='tool', palette='dark', alpha=0.6)
    g.set_axis_labels('', scale)
    g.fig.suptitle(name)
    g.fig.savefig(path.join(processed_results_path, slugify(name) + '.png'))


def render_table(name: str, scale: str, data: DataFrame):
    """Render and save single table """
    grouped = data.groupby(['host', 'tool'])
    mean = grouped.value.transform('mean')
    std = round((grouped.value.transform('std')/mean) * 100, 2)
    run_count = grouped.value.transform('count')
    data['mean'] = mean
    data['std (%)'] = std
    data['run count'] = run_count
    data = data.drop(columns=['value']).drop_duplicates()
    slugified_name = slugify(name)
    with open(path.join(processed_results_path, slugified_name + '.tex'), 'w') as f:
        f.writelines(['\\centering\\caption{Wynik testu ' + name +
                     ' (' + scale + ')\\label{table:' + slugified_name + '}}\n'])
        f.write(render_tabulate(data, 'latex').replace('llrrr', '|l|l|r|r|r|'))


def render_tabulate(data: DataFrame, format: str = 'psql'):
    return tabulate(data, headers='keys', tablefmt=format, showindex=False)


if __name__ == '__main__':

    results = load_results()
    process_results(results)
