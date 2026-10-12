# Development Status

## OPS-UDA-001 — UDA subpath migration
Status: CI passed on main; live user acceptance outstanding.

The UDA handoff supports automatic sign-in and first-use provisioning with loopback-only header trust and optional aliases. Trusted one-hop forwarded-prefix routing preserves the UDA application mount for generated links and static assets. The backend listener must remain inaccessible directly from untrusted networks.

- [x] UDA compatibility CI green on main (11 October 2026)
- [ ] User validates login, gift creation, image uploads and purchased visibility via authenticated UDA
- [ ] Confirm proxy header configuration and group membership on the live server

## UX-MOBILE-001 — Responsive gift-management pass
Status: implemented on main; device validation outstanding.

- [x] Mobile bottom navigation with desktop navbar retained
- [x] Touch-friendly gift list and edit/delete actions
- [x] Mobile-width form styling and phone photo-picker hint
- [x] Correct pound sign on the user's own gift cards
- [ ] Test Android Chrome and iOS Safari photo picker and upload end-to-end
- [ ] Check accessibility, keyboard navigation, and mobile layout at 320/375/430px
- [ ] Review other gift views and currency formatting consistently
- [ ] Consider dedicated camera capture, client-side image compression and upload preview
- [ ] Add mobile browser screenshot/UI regression coverage

## PRIVACY-001 — Private gift semantics
Status: not implemented. Do not assume that purchase-status hiding is fully invisible private gifts.

- [ ] Specify data ownership and authorisation boundaries
- [ ] Implement filtering across list, count, search, exports, notifications and attachments
- [ ] Add privacy-negative tests for unauthorised identities
