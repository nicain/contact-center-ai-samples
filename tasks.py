# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for defining maintainence tasks."""


import sys

import yaml
from invoke import task

with open(".github/workflows/linter.yaml", encoding="utf-8") as file:
    _LINTER_ACTIONS_CONFIG = yaml.safe_load(file)
_LINTER_ENV = _LINTER_ACTIONS_CONFIG["jobs"]["build"]["steps"][1]["env"]
_SUPER_LINTER_VERSION = "ghcr.io/github/super-linter:slim-v4.9.7"
_LINTER_PATTERN = (
    "sudo docker run "
    "--workdir /github/workspace "
    "--rm "
    '-e "{validate}" '
    '-e "TERRAFORM_TFLINT_CONFIG_FILE={config}" '
    '-e "RUN_LOCAL=true" '
    f'-e "FILTER_REGEX_EXCLUDE={_LINTER_ENV["FILTER_REGEX_EXCLUDE"]}" '
    f'-e "LINTER_RULES_PATH=./" '
    f"-v $(pwd):/tmp/lint {_SUPER_LINTER_VERSION}"
)
_LINTER_CONFIG = {
    "terraform": {
        "validate": "VALIDATE_TERRAFORM_TFLINT=true",
        "config": _LINTER_ENV["TERRAFORM_TFLINT_CONFIG_FILE"],
    },
    "javascript": {
        "validate": "VALIDATE_JAVASCRIPT_ES=true",
        "config": _LINTER_ENV["JAVASCRIPT_ES_CONFIG_FILE"],
    },
    "black": {
        "validate": "VALIDATE_PYTHON_BLACK=true",
        "config": _LINTER_ENV["PYTHON_BLACK_CONFIG_FILE"],
    },
    "isort": {
        "validate": "VALIDATE_PYTHON_ISORT=true",
        "config": _LINTER_ENV["PYTHON_BLACK_CONFIG_FILE"],
    },
    "jscpd": {
        "validate": "VALIDATE_JSCPD=true",
        "config": _LINTER_ENV["JSCPD_CONFIG_FILE"],
    },
    "flake8": {
        "validate": "VALIDATE_PYTHON_FLAKE8=true",
        "config": _LINTER_ENV["PYTHON_FLAKE8_CONFIG_FILE"],
    },
    "pylint": {
        "validate": "VALIDATE_PYTHON_PYLINT=true",
        "config": _LINTER_ENV["PYTHON_PYLINT_CONFIG_FILE"],
    },
}


def print_result(linter, result, hide):
    """Print result of linter run with pyinvoke."""
    if result.exited:
        print(f'linter "{linter}": FAILURE (code {result.exited})')
        print(result.stderr.strip())
    else:
        if not hide:
            print(f'linter "{linter}": OK')


@task
def lint(ctx, linter="all", warn=False, hide=False):
    """Run a linter(s) using pyinvoke."""
    if linter == "all":
        any_failure = False
        for curr_linter in _LINTER_CONFIG:
            result = lint(ctx, curr_linter, warn=True, hide=True)
            print_result(curr_linter, result, hide)
            if result.exited:
                any_failure = result.exited
        if (not warn) and any_failure:
            sys.exit(result.exited)
        return result

    result = ctx.run(
        _LINTER_PATTERN.format(
            validate=_LINTER_CONFIG[linter]["validate"],
            config=_LINTER_CONFIG[linter]["config"],
        ),
        warn=True,
        hide=True,
    )
    print_result(linter, result, hide)
    if (not warn) and result.exited:
        sys.exit(result.exited)
    return result
