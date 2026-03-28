## 0.6.0 (2026-03-28)

### Feat

- refactor permission checks to use dedicated staff role retrieval function
- update announce command to use role mention format
- update announce command to mention the default role instead of the user
- update environment configuration for PostgreSQL integration and remove useless port forwarding
- add karaoke rating command and autocomplete functionality

## 0.5.0 (2026-03-11)

### Feat

- add vote command and related autocomplete functionality
- add karaoke results button handler and view component
- add karaoke close command
- **db**: add registrations relation loading, update unique index in Karaoke model and reinit first migration
- **karaoke**: implement karaoke registration modal and handlers
- **karaoke**: add KaraokePariticipantsListView and global interaction handler for karaoke
- **interaction**: add interaction events module with handling logic
- **bot**: add utility functions for Discord object validation
- **karaoke**: create karaoke feature module with components
- **karaoke**: add registration status management command
- **karaoke**: add karaoke announcement command
- **bot**: add error handling for app commands
- **db**: add karaoke database operations and utilities
- **db**: update karaoke model with localization and new fields
- **migrations**: add initial database migration setup and configuration
- **docker**: update Docker configuration for nightcore-karaoke project

### Fix

- set karaoke state to GOING when opening registration
- **karaoke**: improve setstaff command with localization and UX

### Refactor

- **karaoke**: rename get_karaoke to get_karaoke_by_guild_id and add selectin loading to registrations relationship
- **config**: reorganize imports for better structure
- **config**: remove obsolete RAILWAY_DATABASE_URL alias
- **client**: simplify user property in NightcoreKaraoke class

## 0.4.0 (2026-03-04)

### Feat

- **setup**: integrate karaoke feature into bot
- **karaoke**: add setstaff command for managing karaoke roles
- **db**: add karaoke staff management operations
- **utils**: add ensure_role_exists utility function
- **embed**: add ErrorEmbed and SuccessEmbed classes

## 0.3.0 (2026-03-03)

### Feat

- **db**: add permissions configuration model and operations
- **setup**: integrate config and system features into bot
- **system**: add system configuration commands
- **config**: add karaoke configuration command feature
- **permissions**: implement permission checking decorator system
- **config**: add developer IDs configuration
- **components**: add NoOptionsSuppliedEmbed component
- **bot**: add ClientUser type hint to client user property

### Refactor

- **meta**: simplify meta feature structure

## 0.2.0 (2026-03-02)

### Feat

- **db**: implement database structure

## 0.1.0 (2026-03-01)

### Feat

- **db**: add database configuration

## 0.0.1 (2026-03-01)

### Refactor

- refactor logging to use queue and change bot startup way
