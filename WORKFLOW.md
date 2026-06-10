# Maintenance Workflow

This repo keeps hitting the same three issues:

1. Chinese UI text becomes mojibake.
2. A bundle builds but fails to register `gs-scheduler-card`.
3. HACS points at a commit or stale cache instead of the intended release.

Use this workflow every time.

## 1. Edit safely

- Prefer editing files directly in a UTF-8-aware editor.
- If you need scripted text replacement, use:

```bash
python scripts/utf8_replace.py <file> <old> <new>
```

- Avoid shell heredocs for customer-facing Chinese strings.

## 2. Rebuild

```bash
python scripts/build_independent_bundle.py
```

## 3. Verify before release

```bash
node --check assets/scheduler-card.js
node --check gs-scheduler-card.js
node scripts/check_bundle_registration.js gs-scheduler-card.js gs-scheduler-card
```

The third command is mandatory. It catches the exact class of failure that causes:

- `Custom element doesn't exist: gs-scheduler-card`

## 4. Release

Recommended order:

1. Commit to `main`
2. Create tag
3. Push tag
4. Create GitHub Release

## 5. HACS validation

After release:

- Update through HACS
- Close the HA browser tab completely
- Reopen HA
- `Ctrl + Shift + R`

If HACS still shows a commit instead of the tag:

- Check the GitHub Release exists
- Check the tag is pushed
- Check HACS is not pinned to an older installed commit

## 6. Live debugging rule

If the card fails in HA:

- First compare the repo bundle hash with the installed HACS file hash
- Then inspect whether the HA resource path is loading the intended file
- Only after that investigate card logic
