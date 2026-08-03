---
name: commit-push-pr
description: Değişiklikleri commit'le, push'la ve PR aç. Yan etkili olduğu için yalnız kullanıcı tetikler.
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git checkout:*), Bash(git switch:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*)
---

# commit-push-pr

## Bağlam

- Git durumu: !`git status`
- Diff (staged + unstaged): !`git diff HEAD`
- Mevcut branch: !`git branch --show-current`

## Görev

Yukarıdaki değişikliklere göre:

1. `main`/`master` üzerindeysen önce yeni bir branch oluştur.
2. Conventional Commits formatında **İngilizce** tek bir commit oluştur (bkz. `.claude/rules/03-commit.md`).
   AI atfı **ekleme** (varsayılan kapalı).
3. Branch'i `origin`'e push et.
4. `gh pr create` ile PR aç — başlık + özet İngilizce.

> `git push` ve `gh pr create` `ask` iznindedir; onay sorulacaktır (bkz. `02-guvenlik.md`).
> Mümkünse tüm adımları tek mesajda, ardışık tool çağrılarıyla yap.
