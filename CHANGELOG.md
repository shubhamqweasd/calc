# Change Log

All notable changes to this project will be documented in this file,
which uses the format described in
[keepachangelog.com](http://keepachangelog.com/). This project adheres
to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]

## [2.0.0][] - 2017-01-18

### Added

- The new data capture functionality has been added, allowing COs
  to log in (via cloud.gov) and submit their approved Schedule 70
  price lists. Data administrators can then review these price lists and
  add their data into CALC.

- Additionally, data administrators can directly upload Region 10
  bulk data. The uploaded data will then replace all existing Region 10
  data in CALC.

### Changed

- In October 2015, the schedules represented in CALC were consolidated
  into the [Professional Services Schedule][pss] to give federal agency
  acquisition professionals the ability to obtain total contract solutions
  for their professional services requirements using one contract vehicle.

  Consequently, the "Schedule" filter in the data explorer has
  been renamed to the "SIN / Schedule" filter, and allows rates to be
  filtered by SIN number.

- Searching for multiple words in the data explorer's search field
  now produces expected autocompletion results.

- The data explorer is now much more keyboard-accessible and
  screenreader-friendly.

- The "proposed price" field in the data explorer automatically
  updates the histogram on a per-keypress basis; there is no longer
  any need to click the "Go" button.

- Sharing CALC links with the "Education" field filled out now works
  properly.

- The CALC banner has been redesigned to be less confusing and easier
  to read.

- Google Analytics for CALC now properly track new searches in the
  data explorer as page views. We also track clicks on links in the
  "Contract #" column of the data explorer results table.

[pss]: https://www.gsa.gov/portal/content/246403

## [1.2.0][] - 2015-07-21

- filtering empty list items out of query building

## [1.1.2][] - 2015-07-14

- Merge pull request #224 from 18F/ethnio
- Add ethnio screener

## [1.1.1][] - 2015-07-08

- hide proposed price field so that we may deploy to production
  everything but this feature

## [1.1.0][] - 2015-07-07

- Merge pull request #211 from 18F/add-histogram-design
- Updates to histogram

## [1.0.1][] - 2015-06-29

- Merge pull request #205 from 18F/search-bug
- Strip non-alpha numeric or whitespace chars out of search query

## 1.0.0 - 2015-06-24

- adds hidden proposed price starting functionality
- adds standard deviation callouts
- adds icons in header
- workflow documentation
- bug fix for stacked histogram labels
- removing python 2.7 support
- script to run django migrations on cloud foundry
- slider and drop downs to replace single drop down for years experience
- refining header wording
- replace drop down for education with multi select

[unreleased]: https://github.com/18F/calc/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/18F/calc/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/18F/calc/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/18F/calc/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/18F/calc/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/18F/calc/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/18F/calc/compare/v1.0.0...v1.0.1
