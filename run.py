import os
import shutil
import webbrowser

import pytest

if __name__ == '__main__':
    pytest.main([
        '-s',
        '-v',
        '--alluredir=./report/temp',
        './testcase',
        '--clean-alluredir',
        '--junitxml=./report/results.xml'
    ])

    if os.path.exists('./environment.xml'):
        shutil.copy('./environment.xml', './report/temp')

    html_report_dir = './report/allureReport'
    os.makedirs(html_report_dir, exist_ok=True)
    os.system(f'allure generate ./report/temp -o {html_report_dir} --clean')

    # os.system(f'allure serve ./report/temp')