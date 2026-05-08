# Dogfood QA Report

**Target:** http://localhost:3002 (Frontend), http://localhost:8000 (Backend API)  
**Date:** 2026-05-04  
**Scope:** Full MVP Testing (ArtiSANs NG - Nigeria-first artisan booking platform)  
**Tester:** Hermes Agent (automated exploratory QA)  

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 High | 0 |
| 🟡 Medium | 1 |
| 🔵 Low | 1 |
| **Total** | **3** |

**Overall Assessment:** Core MVP features (registration, login, search, dashboard) are functional, but critical auth state synchronization issue exists in the Navbar component.

---

## Issues

### Issue #1: Navbar does not update after login/logout

| Field | Value |
|-------|-------|
| **Severity** | 🔴 Critical |
| **Category** | Functional / UX |
| **URL** | All pages (global Navbar component) |

**Description:**  
The navigation bar fails to reflect authentication state changes. After successful login, the Navbar still displays "Login / Register" instead of "Dashboard" and "Logout". Similarly, after logout, the Navbar does not immediately update to show "Login / Register".

**Steps to Reproduce:**
1. Navigate to http://localhost:3002/auth
2. Register a new user (any role)
3. Observe the Navbar after redirect to /dashboard
4. Notice Navbar still shows "Login / Register" instead of user-specific links

**Expected Behavior:**  
Navbar should dynamically update to show "Dashboard", "Logout", and username when authenticated.

**Actual Behavior:**  
Navbar shows "Login / Register" even when the user is authenticated (token exists in localStorage).

**Root Cause:**  
The Navbar component uses `useEffect(() => { ... }, [])` which only runs on component mount. It does not listen for auth state changes triggered by login/logout in other components.

---

### Issue #2: Dropdown menus throw CDP errors when clicking options

| Field | Value |
|-------|-------|
| **Severity** | 🟡 Medium |
| **Category** | Functional |
| **URL** | /auth, /search |

**Description:**  
When attempting to click dropdown options (e.g., Role selector in registration, Category filter in search), the browser throws a CDP (Chrome DevTools Protocol) error: "Could not compute box model". This prevents mouse-based selection of dropdown options.

**Steps to Reproduce:**
1. Navigate to http://localhost:3002/auth
2. Click "Register" to open registration form
3. Click the "I am a:" dropdown
4. Attempt to click "Artisan (offering services)" option
5. Observe CDP error in browser tool response

**Expected Behavior:**  
Dropdown options should be clickable and selectable without errors.

**Actual Behavior:**  
Clicking dropdown options throws CDP error; workaround requires keyboard navigation (ArrowDown + Enter).

**Workaround:**  
Use keyboard navigation: click dropdown, press ArrowDown to select option, press Enter to confirm.

---

### Issue #3: Artisan roles can access Post Job page

| Field | Value |
|-------|-------|
| **Severity** | 🔵 Low |
| **Category** | Auth Guard / UX |
| **URL** | http://localhost:3002/jobs/post |

**Description:**  
Users registered as "Artisan" can access the "Post a Job" page, which is intended for clients only. No role-based access control is enforced on this route.

**Steps to Reproduce:**
1. Register as an "Artisan" role user
2. Navigate to http://localhost:3002/jobs/post
3. Observe that the job posting form is fully accessible

**Expected Behavior:**  
Artisan users should be redirected to dashboard or shown an "Unauthorized" message when accessing client-only pages.

**Actual Behavior:**  
Artisan users can view and submit the job posting form (backend may reject based on role, but frontend has no guard).

---

## Issues Summary Table

| # | Title | Severity | Category | URL |
|---|-------|----------|----------|-----|
| 1 | Navbar does not update after login/logout | 🔴 Critical | Functional/UX | All pages |
| 2 | Dropdown CDP errors on click | 🟡 Medium | Functional | /auth, /search |
| 3 | Artisan can access Post Job page | 🔵 Low | Auth Guard | /jobs/post |

---

## Testing Coverage

### Pages Tested
- Homepage (/) - Popular Services, Featured Artisans sections
- Authentication (/auth) - Login, Register flows
- Dashboard (/dashboard) - Job stats, Quick Actions
- Search (/search) - Category/location filters, artisan listing
- Post Job (/jobs/post) - Job form

### Features Tested
- ✅ User registration (artisan role)
- ✅ User login with registered credentials
- ✅ API connectivity (frontend ↔ backend)
- ✅ Artisan search with filters
- ✅ Navigation links (Find Artisans, Post a Job)
- ✅ Protected route access (dashboard requires auth)

### Not Tested / Out of Scope
- ✗ Payment integration (Paystack/Flutterwave) - test keys only
- ✗ Artisan profile editing
- ✗ Job bidding workflow
- ✗ Email notifications
- ✗ Mobile responsive testing
- ✗ Cross-browser testing

### Blockers
- None major; CDP dropdown errors are annoying but have keyboard workaround.

---

## Notes

1. **Resolved During Testing:** Initial API port mismatch (frontend pointed to 8001 instead of 8000) was fixed by starting the ArtiSANs backend server on port 8000.
2. **Backend Status:** Django backend is fully functional, serving categories and handling auth correctly.
3. **Frontend Recommendation:** Implement a global AuthContext to synchronize auth state across all components, replacing the localStorage-only approach in Navbar.
4. **Next Steps:** Fix Navbar auth state issue (Critical), add role-based route guards, then proceed to Deployment setup.

---

**Report Generated By:** Hermes Agent (dogfood skill v1.0.0)  
**Screenshot Evidence:** /home/araoye/.hermes/cache/screenshots/browser_screenshot_96ae63d79b294015a52f82d59eff5451.png
