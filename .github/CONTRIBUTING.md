<!-- 
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 
-->

# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Code Reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).

## Adding a new sample

### Policies

Samples in this repository are expected to:

* Adhere to best practices
* Be up to date
* Demonstrate a clear Contact Center AI use-case or integration
* Have a clear focus and goal
* Have owners that respond to issues and questions
* Pass tests (if present)

Samples repeatedly failing to meet this criteria will be moved or removed.

The purpose of these expectations are to ensure quality, up to date code for
others. If you need help keeping your sample in line with these expectations
please reach out to the `@GoogleCloudPlatform/ml-apis`.

### How to add a new sample

If you would like to add a new sample to this repository please follow these
instructions. If your sample is large, complex, or you would like feedback
before adding a sample to this repository please open a issue with your question or
request and assign it to `@GoogleCloudPlatform/ml-apis`

1. Determine the name for your sample.

    Generally the name of your sample should be a few words that briefly
    describe, the purpose or function of your sample code. For example:
    `dialogflow-webhook-python`. Here are a few guidelines:

    * Do not include `Contact Center AI`, `contactcenterai`,
        `contact-center-ai` or `ccai` in the name of your sample
    * The name of your sample must be hyphenated and only contain letters,
        numbers, and hyphens.
    * If the sample is primarily one language the name for your sample must
        end in `-language-name` e.g. `-nodejs`, `-python`, etc.

1. Create a new folder in the root of the repository or in the community folders

    To add a new samples to this repository you must add a new folder to either the
    root of the repository or in the `community` folder. The name of the folder must
    correspond to the name of your sample.

1. Create a README.md for your sample

    Each sample must have its own README.md file in the root of the sample
    folder. This sample must include:

    * The name of the sample
    * A description of what the sample does
    * Detailed instructions on how to setup and run the sample
    * [Community samples only] Add the following disclaimer to your sample's
        README.md file:
        ```bash
        ## Disclaimer
        This community sample is not officially maintained by Google.
        ```
    * Detail instructions on how to run tests (if present)

1. Update the repo's README with a link to your sample

    Edit the repo's README.md file to with the name of your sample, a link to
    the sample repository and a brief description. If your sample is in the
    `community` folder add your sample's name, link and description to the
    "Community" section of the repo's README.md.

1. [non-community samples only] Setup testing and GitHub Actions

    This step is not required for samples located in the `community` folder. All
    samples in the root of the repository must have tests and those tests must be
    setup to run on new pull requests that edit files in your sample folder.

    1. Create a GitHub Actions YAML configuration file for your sample To add
        enable testing for your sample create a new YAML file in the
        `.github/workflows` folder of this repository with the name of your sample
        with the `.yaml` file extension. For example:
        `.github/workflows/dialogflow-webhook-python.yaml`

    1. Configure when your tests run

        Use GitHub Action's triggers to run your tests on a pull request for the
        `main` branch and use `path` config to scope your tests to run only on
        pull requests that change your sample's code. For example:
        ```yaml
        name: Dialogflow Webhook Python Sample
        on:
            pull_request:
                branches:
                    - main
                paths:
                    - 'dialogflow-webhook-python/**'
        jobs:
            ...
        ```
        See
        [GitHub's Actions trigger documentation](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)
        for more information.

    1. Connect your tests to GitHub Actions Use GitHub Actions' `jobs` feature
        to define a test environment and run your tests. For example:
        ```yaml
        ...
        jobs:
            unit:
                runs-on: ubuntu-latest
                defaults:
                    run:
                        working-directory: ./dialogflow-webhook-python
                strategy:
                    matrix:
                       python: ['3.6', '3.7', '3.8', '3.9', '3.10']
                steps:
                    - name: Checkout
                    uses: actions/checkout@v2
                    - name: Setup Python
                    uses: actions/setup-python@v3
                    with:
                        python-version: ${{ matrix.python }}
                    - name: Install requirements.txt
                    run: |
                        python -m pip install -U -r requirements.txt
                    - name: Run unit tests
                    run |
                        python main_test.py
         ```
        See
        [GitHub's Actions job documentation](https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow)
        for more information.

1. Add a code owners entry for your sample

    Add an entry in the `.github/CODEOWNERS` file (`community/CODEOWNERS` for
    community samples) for your sample folder and add the GitHub usernames of
    the owners. Please include a comment indicating the owner of the sample. For
    example:
    ```bash
    # @matthewayne is the default owner for PDF splitter sample changes
    /dialogflow-webhook-python/ @matthewayne
    ```

1. Start a review for your sample

    [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    and add
    [@GoogleCloudPlatform/ml-apis](https://github.com/orgs/GoogleCloudPlatform/teams/ml-apis)
    as a reviewer
