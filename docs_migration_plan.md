# Documentation Migration Plan

## 1. Objective

To consolidate all scattered documentation into a single `docs/` directory at the project root. This will improve discoverability, organization, and maintainability of project documentation without modifying the content of the documents themselves.

## 2. Current State

Project documentation is currently located in various places, making it difficult to find. The identified files for migration are:

- `CONVENTION.md`: Located at the project root.
- `painter/migration_plan.md`: Specific plan for `painter` module refactoring.
- `painter/migration_progress.md`: Progress tracker for the `painter` migration.

## 3. Proposed Structure

All documentation will be moved into a new `docs/` directory. A `dev/` subdirectory will be created to house documents related to development processes and conventions.

```
docs/
└── dev/
    ├── CONVENTION.md
    ├── painter_migration_plan.md
    └── painter_migration_progress.md
```

This file, `docs_migration_plan.md`, will also be moved into `docs/dev/` once the migration is complete.

## 4. Migration Execution Plan

The migration will be performed using `git mv` to preserve file history.

1.  **Create the target directory:**
    ```bash
    mkdir -p docs/dev
    ```

2.  **Move and rename the documentation files:**
    ```bash
    git mv CONVENTION.md docs/dev/CONVENTION.md
    git mv painter/migration_plan.md docs/dev/painter_migration_plan.md
    git mv painter/migration_progress.md docs/dev/painter_migration_progress.md
    ```

3.  **Move this migration plan:**
    After the above steps are complete, this plan should also be moved.
    ```bash
    git mv docs_migration_plan.md docs/dev/docs_migration_plan.md
    ```

## 5. Future-proofing

All new documentation for the project, regardless of its audience (end-user, developer), should be placed within the `docs/` directory in an appropriate subdirectory.
