# ENPM611 Project Application Template

This is the template for the ENPM611 class project. Use this template in conjunction with the provided data to implement an application that analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates interesting insights.

This application template implements some of the basic functions:

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration paramters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate intersting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.

## Setup

To get started, your team should create a fork of this repository. Then, every team member should clone your repository to their local computer. 


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```

That will output basic information about the issues to the command line.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

## Program Description

To run our program use these lines:
```
python run.py --feature 0
python run.py --feature 1
python run.py --feature 2
python run.py --feature 3
```

- Feature 0 runs the example analysis which counts the top 50 users who have submitted issues.
- Feature 1 counts the label used in the issues and plots them in descending order.
- Feature 2 runs our resolution time analysis.
- Feature 3 visualizes issue dependency and events dependency using a tree.
- Feature 4 Frequency off the issues are created 
plotted against time

## TESTING

## Install dependencies


pip install coverage



## Running unit test case
To run the unit tests:


python -m coverage run -m unittest discover -s tests



## Generating Test Coverage Report
After running the tests, to generate a coverage report :


python -m coverage report --omit="test_*"



## Test Feature 1 - Usage Analysis
Unit tests for UsageAnalysis were made using unittest with mock data. Test scenarios that were tried included standard uses, large data sets, duplicate labels, issues with no labels, and completely empty issues. Tests passed at 95% coverage and proved the accuracy of label counts and the robustness in the handling of edge cases.

## Test Feature 2 - Resolution time Analysis
Unit tests for the ResolutionTimeAnalysis module were run using the unittest framework for scenarios such as standard use cases with valid dates, empty datasets, all open issues, and malformed date formats. These tests cover the different ways data may be handled; how errors can be managed; and that resolution times are plotted correctly, with 100% code coverage. 

## Test Feature 3 - Issue Tree Visualizer
This test file validates the functionality of the IssueTreeVisualizer class using mock issue data to simulate realistic scenarios. It thoroughly tests core methods such as load_issues, filter_by_date, build_graph, and draw_graph for various valid, edge, and error cases. Additionally, the run method is tested to ensure the end-to-end workflow operates as expected. Current tests achieve 95% code coverage.

## Test Feature 4 - Frequency of Issue Creation
Unit tests were provided for the module frequencyOfIssueCreation using mock issues to test that it works as intended. Tests of processing dates when issues were created and calling the correct functions to plot were performed. Tests covered code with 100% for Issues that were mocked with specific dates were analyzed, confirming frequency and plotting workflows worked as expected.