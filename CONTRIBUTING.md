# Contributing to pytest-dash

### Getting started

- Fork and clone the repo
- Create and activate
```
$ python -m venv venv
$ . venv/bin/activate
```
- Install the dependencies
`$ pip install -r requirements.txt`
- The plugin needs to be installed to run the tests locally
`$ pip install -e .`

### Coding style

#### Linters

- [pylint](https://www.pylint.org/): 
`$ pylint pytest_dash tests test_apps`
- [flake8](http://flake8.pycqa.org/en/latest/): 
`$ flake8 pytest_dash tests test_apps`

#### Formatter 

Auto format with [yapf](https://github.com/google/yapf):

`$ yapf pytest_dash tests test_apps -ri`

#### Commit messages

Prefix your commit messages with an emoji according to this list adapted from:
https://gist.github.com/parmentf/035de27d6ed1dce0b36a

|   Commit type              | Emoji                                         |
|:---------------------------|:----------------------------------------------|
| Initial commit             | :tada: `:tada:`                               |
| Version tag                | :bookmark: `:bookmark:`                       |
| New feature                | :sparkles: `:sparkles:`                       |
| Bugfix                     | :bug: `:bug:`                                 |
| Metadata                   | :card_index: `:card_index:`                   |
| Documentation              | :books: `:books:`                             |
| Documenting source code    | :bulb: `:bulb:`                               |
| Performance                | :racehorse: `:racehorse:`                     |
| Cosmetic                   | :lipstick: `:lipstick:`                       |
| Tests                      | :rotating_light: `:rotating_light:`           |
| Adding a test              | :white_check_mark: `:white_check_mark:`       |
| General update             | :construction: `:construction:`               |
| Improve format/structure   | :art: `:art:`                                 |
| Move code                  | :feet: `:feet:`                               |
| Refactor code              | :hammer: `:hammer:`                           |
| DRY up code                | :camel: `:camel:`                             |
| Removing code/files        | :hocho: `:hocho:`                             |
| Continuous Integration     | :green_heart: `:green_heart:`                 |
| Security                   | :lock: `:lock:`                               |
| Upgrading dependencies     | :arrow_up: `:arrow_up:`                       |
| Downgrading dependencies   | :arrow_down: `:arrow_down:`                   |
| Lint                       | :shirt: `:shirt:`                             |
| Translation                | :alien: `:alien:`                             |
| Text                       | :pencil: `:pencil:`                           |
| Critical hotfix            | :ambulance: `:ambulance:`                     |
| Deploying stuff            | :rocket: `:rocket:`                           |
| Fixing on MacOS            | :apple: `:apple:`                             |
| Fixing on Linux            | :penguin: `:penguin:`                         |
| Fixing on Windows          | :checkered_flag: `:checkered_flag:`           |
| Adding CI build system     | :construction_worker: `:construction_worker:` |
| Analytics or tracking code | :chart_with_upwards_trend: `:chart_with_upwards_trend:` |
| Removing a dependency      | :heavy_minus_sign: `:heavy_minus_sign:`       |
| Adding a dependency        | :heavy_plus_sign: `:heavy_plus_sign:`         |
| Docker                     | :whale: `:whale:`                             |
| Configuration files        | :wrench: `:wrench:`                           |
| Bundles update             | :package: `:package:`                         |
| Merging branches           | :twisted_rightwards_arrows: `:twisted_rightwards_arrows:` |
| Bad code / need improv.    | :hankey: `:hankey:`                           |
| Reverting changes          | :rewind: `:rewind:`                           |
| Breaking changes           | :boom: `:boom:`                               |
| Code review changes        | :ok_hand: `:ok_hand:`                         |
| Accessibility              | :wheelchair: `:wheelchair:`                   |
| Move/rename repository     | :truck: `:truck:`                             |
| Other                      | [Be creative](http://www.emoji-cheat-sheet.com/)  |

### Rebase instead of merge

The only option for merging pull requests is [Rebase and merge](https://help.github.com/articles/about-pull-request-merges/#rebase-and-merge-your-pull-request-commits).
As such, it is advisable to rebase when pulling instead of merging.

#### Run the tests

- Make sure a selenium driver is available on your `PATH`
- From the root directory: `$ pytest tests --driver Chrome`

#### Build the docs

- `$ cd docs`
- Generate the autodoc rst files: `$ make rst`
- Generate the static html: `$ make html`
- See the output by opening `docs/_build/html/index.html`
