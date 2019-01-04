# Changelog

Versions follow [Semantic Versioning](https://www.semver.org)

## [1.1.0] 2019-01-01
### Added
- Base exception type: `PytestDashError` [#23](https://github.com/T4rk1n/pytest-dash/pull/23)
- `DashAppLoadingError` [#23](https://github.com/T4rk1n/pytest-dash/pull/23)
  - Display the body html
  - Display console logs
  - Catch common errors early. [#33](https://github.com/T4rk1n/pytest-dash/pull/33)
  - Loop wait_for `#_dash-app-content` and retry the url. [#33](https://github.com/T4rk1n/pytest-dash/pull/33)
  - Added `start_wait_time` and `start_timeout` to `dash_threaded` [#33](https://github.com/T4rk1n/pytest-dash/pull/33)
- Add port option to `dash_threaded` and `dash_subprocess`. [#28](https://github.com/T4rk1n/pytest-dash/pull/28)
- Add `start_wait_time` option to `dash_threadred` for waiting after starting the thread, default to 1 sec. [#28](https://github.com/T4rk1n/pytest-dash/pull/28)
- Add more `wait_for` wrappers [#41](https://github.com/T4rk1n/pytest-dash/pull/41)
  - `wait_for_style_to_equal`
  - `wait_for_property_to_equal`
  - `wait_for_element_by_*`

### Fixed
- `dash_subprocess` uses `_wait_for_client_app_started` instead of polling the output, fix subprocess tests on circle #13, [#43](https://github.com/T4rk1n/pytest-dash/pull/43)

## [1.0.1] 2018-12-05
### Fixed
- Fixed `utils.import_app` imported methods not having access to imports. [#12](https://github.com/T4rk1n/pytest-dash/pull/11)

### Changed
- Syntax for `utils.import_app` changed to dot notation, same as `dash_subprocess`.

## [1.0.0] 2018-12-04

[#8](https://github.com/T4rk1n/pytest-dash/pull/8)

### Added

- Added `dash_subprocess` fixture, runs a dash app in a subprocess waitress-serve command.
- `utils.wait_for_text_to_equal`
- `utils.wait_for_element_by_css_selector`

### Removed
- `dash_app` fixture.

### Renamed
- `start_dash` fixture to `dash_threaded`

## [0.1.3] 2018-10-04
### Fixed

- Ensure the page is loaded after starting the app. [#6](https://github.com/T4rk1n/pytest-dash/pull/6)

## [0.1.2] 2018-10-04
### Fixed

- Better error for missing app in `dash_from_file` fixture. [#5](https://github.com/T4rk1n/pytest-dash/pull/5)

## [0.1.1] 2018-10-04
### Fixed

- Added fixtures usage examples to the README. [#4](https://github.com/T4rk1n/pytest-dash/pull/4)
- Fixed setup.cfg classifiers.

## [0.1.0] 2018-10-03
### Added

- Initial fixtures [#1](https://github.com/T4rk1n/pytest-dash/pull/1).
    - `start_dash`, start a dash app instance in a thread.
    - `dash_from_file`, load a py file and return the dash app.
    - `dash_app`, combine `dash_from_file` and `start_dash`.
    - `percy_snapshot`, take percy snapshot (untested)
