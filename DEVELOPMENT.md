# Development Status

## OPS-UDA-001 — UDA subpath migration
Status: IN PROGRESS

GiftList uses trusted one-hop forwarded-prefix routing to generate navigation/static URLs within UDA's application mount. Existing gift permissions, CSRF and LAN root routes remain unchanged; smoke test runs on isolated in-memory SQLite. Backend ingress must be proxy-restricted; public access unchanged.

- [ ] CI green and merged to main
- [ ] User validates login, gift creation, image uploads and purchased visibility via authenticated UDA
