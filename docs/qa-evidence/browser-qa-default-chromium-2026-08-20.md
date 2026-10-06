# Browser QA — default
**Date:** 2026-08-20  
**URL:** https://nstate.org  
**Scope:** quick  
**Browser:** chromium  
**Status: FAIL**

## Layer 1 — Functional

| Check | Result | Value |
|-------|--------|-------|
| http_status | ✓ | 200 |
| page_not_empty | ✓ | 3137 chars |
| title_present | ✓ | nstate |
| element:h1 | ✓ | 1 found |
| element:nav | ✓ | 1 found |
| element:main, [role=main], #__next, #root | ✓ | 1 found |
| no_console_errors | ✗ | ['Failed to load resource: the server responded with a status of 404 ()', 'Faile |

*Filed: 2026-08-20 by browser-qa (Python Playwright)*