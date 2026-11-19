"""Verify both the deliberate regression and the corrected behavior."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from xml.etree import ElementTree


EXPECTED_FAILURES = {
    ('tests.test_zero', 'test_zero_limit_returns_no_rows'),
    ('tests.test_contract', 'test_selection_contract[0-expected0]'),
}
EXPECTED_TEST_COUNT = 14
SOURCE = Path(__file__).resolve().parent


def verify(work, label, expected_failures):
    report = work / 'pytest.xml'
    env = os.environ.copy()
    env.pop('PYTEST_ADDOPTS', None)
    env.pop('PYTEST_PLUGINS', None)
    env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    result = subprocess.run(
        [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
         f'--junitxml={report.name}', 'tests'],
        cwd=work, env=env, capture_output=True, text=True, timeout=30,
    )
    expected_exit = int(bool(expected_failures))
    if result.returncode != expected_exit or not report.exists():
        raise RuntimeError(f'{label}: unexpected pytest exit {result.returncode}')
    cases = ElementTree.parse(report).findall('.//testcase')
    actual_failures = {
        (case.attrib['classname'], case.attrib['name'])
        for case in cases if case.find('failure') is not None
    }
    if (len(cases) != EXPECTED_TEST_COUNT or actual_failures != expected_failures
            or any(case.find('error') is not None or case.find('skipped') is not None for case in cases)):
        raise RuntimeError(f'{label}: {len(cases)} tests, unexpected results: {sorted(actual_failures)}')
    print(f'{label}: {len(cases) - len(actual_failures)} passed, {len(actual_failures)} failed')
    for group, name in sorted(actual_failures):
        print(f'  Expected failure: {group}::{name}')


def main():
    print(f'Python {sys.version.split()[0]}')
    with TemporaryDirectory() as directory:
        work = Path(directory)
        shutil.copytree(SOURCE / 'app', work / 'app', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(SOURCE / 'tests', work / 'tests', ignore=shutil.ignore_patterns('__pycache__'))
        selection = work / 'app/selection.py'
        fixed = selection.read_bytes()
        selection.write_bytes((work / 'app/selection_original.py').read_bytes())
        verify(work, 'Before fix', EXPECTED_FAILURES)
        selection.write_bytes(fixed)
        verify(work, 'After fix', set())


if __name__ == '__main__':
    main()
