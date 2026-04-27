# StudyStats

## v2.6.1 - Login Page UI Overhaul

### Changes

- Login page now looks like the main site

## v2.6.0 — Reminders + UI update II

### Added
- Reminder System

### Improved
- Overhauled UI

## v2.6.1-beta — Reminders (Pre-release)

### Changed
- just dev testing

### Notes
- Notifications may not work in all environments
- Requires browser permission + HTTPS
- Still under testing

## v2.6.0-beta — Reminders (Pre-release)

### Added
- Browser-based notification reminders
- Streak risk alerts

### Notes
- Notifications may not work in all environments
- Requires browser permission + HTTPS
- Still under testing

## v2.5.1 — Enhanced Insights

### Added
- Weekly study summary
- Consistency percentage tracking
- Week-over-week comparison

### Improved
- Insights now provide deeper behavioral analysis

## v2.5.0 — Insights System

### Added
- Smart insights based on study behavior
- Real-time feedback (streaks, inactivity, subject balance)

### Improved
- UI spacing and layout
- Sidebar animations and readability

### Fixed
- Theme toggle visibility issue

## v2.4.0 — Database Migration (SQLite)

### Added
- Migrated storage system from JSON to SQLite database
- Created persistent sessions table for user data
- Enabled multi-device data synchronization

### Changed
- Replaced file-based data handling with SQL queries
- Updated session add/delete logic to use database
- Updated session IDs (no longer using loop index)

### Improved
- Data reliability and consistency
- Scalability for multiple users
- Performance for data retrieval

### Fixed
- Data corruption issues (e.g. extreme values like 6.37E+89)
- Multi-device sync issues
- Overwriting data bugs from JSON system

### Notes
- `data.db` is now used for storage (excluded from Git)
- Future upgrade: move to PostgreSQL for cloud persistence

## Changelog(v2.3.1):

- more UI tweaks

## Changelog(v2.3.0):

- UI Overhaul
- Added Light and Dark mode
- Removed old background

## Changelog(v2.2.1):

- Added confirmation popup when deleting sessions
- Other bug fixes

## Changelog (v2.2.0):

- Added delete session feature
- Added daily study goal tracker
- Added XP and leveling system
- Added study timer
- UI improvements

## Changelog(v2.1.0):
- Added Weekly study graphs
- Improved UI
- Bug Fixes

## Changelog(v2.0.1):

- Improved the login button visual

A minimal Flask-based study tracking dashboard.

## Changelog(v2.0.0):

- Added no password login system
- Other bug fixes

## Features
- Log study sessions
- View total study time
- Subject breakdown
- Clean dark UI

## Installation

```bash
pip install -r requirements.txt