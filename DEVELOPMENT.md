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

## AUTH-PROXY-002 — Reverse-proxy identity only
Status: committed, CI/live validation pending.

When UDA_AUTH_ENABLED=true, require a trusted proxy IP, X-UDA-User email, and the configured X-UDA-Groups membership on **every request**. Existing app sessions cannot override failed identity checks. Legacy app login/register/logout/password-reset routes are disabled in proxy mode and the logout link is hidden. The local standalone login mode remains available only when UDA_AUTH_ENABLED=false.

Deployment: set UDA_AUTH_ENABLED=true, UDA_REQUIRED_GROUP to the relevant permitted UDA group, UDA_TRUSTED_PROXY_IPS to the real proxy socket address(es), and optionally UDA_USER_ALIASES to map proxy email to pre-existing GiftList user email and avoid duplicate lists. Restrict the application listener to loopback/firewall; ensure Caddy *overwrites* identity headers and never forwards client-supplied X-UDA-* headers. If these headers are not supplied, access fails closed with HTTP 403.

- [ ] Verify live proxy header forwarding, permitted group and firewall/listener
- [ ] Verify identities and access separation for each user on mobile and desktop
- [ ] Check removal of proxy access immediately blocks existing sessions

## QA-MOBILE-002 — Mobile and proxy regression coverage
Status: implementation committed; CI and real-device validation pending.

- [x] Expand GitHub Actions from the subpath smoke test to the entire pytest suite
- [x] Add authenticated mobile navigation and form-markup tests
- [x] Add authenticated UDA prefix mobile-link test
- [x] Add local image preview on gift form (no image sent until form submission)
- [ ] Android Chrome / iOS Safari browser verification
- [ ] Live proxy login and photo upload acceptance test
- [ ] Run visual viewport tests at 320, 375 and 430 pixels
