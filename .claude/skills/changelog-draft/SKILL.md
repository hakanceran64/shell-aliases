---
name: changelog-draft
description: Git log'undan Keep-a-Changelog formatında değişiklik özeti üretir — Conventional Commit type'larından Added/Changed/Fixed/Removed kategorize eder. Tetikleyiciler: "changelog", "release notes", "ne değişti".
allowed-tools: Read, Bash(git log:*), Bash(git tag:*), Bash(git describe:*)
user-invocable: true
---

# changelog-draft

Son tag'den bu yana olan commit'leri okuyup Keep-a-Changelog formatında taslak üretir.

## Adımlar

1. Son tag'i bul: `git describe --tags --abbrev=0` (yoksa ilk commit'ten).
2. Commit'leri çek: `git log <tag>..HEAD --oneline`.
3. Conventional Commit type'larına göre kategorize et.

## Type → kategori

| Commit type | Changelog bölümü |
|-------------|------------------|
| `feat` | Added |
| `fix` | Fixed |
| `refactor`, `perf`, `style` | Changed |
| `revert` | Removed |
| `docs`, `test`, `build`, `chore` | (girmez, opsiyonel) |

## Çıktı

```markdown
## [Unreleased]

### Added
- ...

### Fixed
- ...
```

SemVer: yalnız `fix` → PATCH · `feat` → MINOR · `BREAKING CHANGE` → MAJOR.

## İlgili

- [03-commit.md](../../rules/03-commit.md)
