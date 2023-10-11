
# Change Log
All notable changes to this project will be documented in this file.

## [[0.0.2]](https://github.com/oradwastaken/backgammon_trainer/releases/tag/v0.0.2) - 2023-10-10

### Added

- Build action to create portable binaries for windows, macOS and ubuntu.

### Changed

- Colors disabled for windows.
- Removed the "Opening Replies" trainer for now, since it doesn't seem to be working properly.
- Updated out-of-date documentation.

### Fixed
- Explicitly read files with `utf-8` encoding so that Windows users can actually see the board
- Fixed "Relative Pip Count trainer" so that you can see both players' checkers

## [[0.0.1]](https://github.com/oradwastaken/backgammon_trainer/releases/tag/v0.0.1) - 2023-09-19

### Added

- Created a change log!
- Added iSight method game, created `iSight()` function and related tests.
- Added `crossovers()` method/property and tests to `Board` class.

### Changed

- `random_bear_off_position()` can now create a 1-sided or 2-sided bear-off position.
- Absolute pipcount quiz now only tests one player instead of quizzing for both.
