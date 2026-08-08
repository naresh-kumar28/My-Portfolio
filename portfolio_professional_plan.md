# Portfolio Website — Professionalization Plan

**Project:** Django Portfolio (`myportfolio/`)
**Stack:** Django 6.0.2, SQLite, Tailwind CSS, Gunicorn + Whitenoise (deploy-ready)
**Goal:** Fix security holes, restructure for production quality, add HTMX for no-reload interactivity, and make it fully mobile responsive.

This file is a self-contained task list. Work through the phases in order — Phase 1 is a security emergency and should be done before anything else. Each task lists the exact file(s) to touch and what "done" looks like.

---

## Current State — Confirmed Issues

Codebase reviewed at `myportfolio/`. Findings:

1. **`portfolio/views.py` → `registerView`** — Public self-registration is open at `/accounts/register/`. Any visitor can create an account.
2. **`portfolio/views.py` → `projectAdd`, `teamAdd`, `addSkill`, `adminDashboard`** — Protected only with `@login_required`. This checks "is logged in", NOT "is authorized". Any registered user (including the ones from issue #1) can create/edit portfolio content.
3. **`website/settings.py`** — `DEBUG = True` is hardcoded, not env-controlled. If deployed as-is, Django's debug error pages leak source code, settings, and stack traces to the public.
4. **`website/settings.py`** — `SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")` — if `.env` fails to load for any reason, the app silently falls back to a publicly-known weak key.
5. **No file upload validation** — `Project.project_image` (`portfolio/models.py`) accepts any file with no extension/MIME/size check.
6. **No brute-force protection** on `/accounts/login/`.
7. **Zero HTMX / AJAX** — every form submission and page navigation is a full server round-trip and full page reload.
8. **Tailwind CSS is already used** (`templates/base.html`) — good foundation, but responsiveness has not been systematically audited across breakpoints.
9. **Real Django admin lives at `/superadmin/`** (in `website/urls.py`) — that part is fine, obscured already. The custom `/admin/` panel (`portfolio` app) is the actual weak point described above.

---

## Phase 1 — Security (do this first, before anything else)

### 1.1 Close public self-registration
- **File:** `portfolio/urls.py`, `portfolio/views.py`, `templates/registration/register.html`
- Remove the `path('accounts/register/', registerView, name='register')` route entirely, or gate it behind `@user_passes_test(lambda u: u.is_superuser)` if you want the option to add teammates later through it.
- Delete/disable `registerView` in `views.py` accordingly.
- Create your own account instead via:
  ```
  python manage.py createsuperuser
  ```

### 1.2 Lock down admin views to staff only
- **File:** `portfolio/views.py`
- Add a reusable decorator and apply it to `adminDashboard`, `projectAdd`, `teamAdd`, `addSkill`:
  ```python
  from django.contrib.auth.decorators import login_required, user_passes_test

  staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='login')
  ```
  Then stack it: `@staff_required` above each admin view (in addition to or replacing `@login_required`).
- Make sure your own superuser account has `is_staff=True` (default `createsuperuser` already sets this).

### 1.3 Fix `settings.py` for production safety
- **File:** `website/settings.py`
- Replace hardcoded `DEBUG = True` with:
  ```python
  DEBUG = os.getenv("DEBUG", "False") == "True"
  ```
- Remove the `"test-secret-key"` fallback — fail loudly instead if missing:
  ```python
  SECRET_KEY = os.environ["SECRET_KEY"]
  ```
- Add (active only when `DEBUG` is `False`, i.e. production/HTTPS):
  ```python
  if not DEBUG:
      SECURE_SSL_REDIRECT = True
      SESSION_COOKIE_SECURE = True
      CSRF_COOKIE_SECURE = True
      SECURE_HSTS_SECONDS = 31536000
      SECURE_HSTS_INCLUDE_SUBDOMAINS = True
  ```
- Confirm `.env` is in `.gitignore` (already checked — it is) and that `SECRET_KEY`, `DEBUG` both live in `.env` locally and in your host's environment variables in production (Render dashboard, etc.).

### 1.4 Validate file uploads
- **File:** `portfolio/models.py`
- Add a validator to `Project.project_image`:
  ```python
  from django.core.validators import FileExtensionValidator

  project_image = models.ImageField(
      upload_to='project/images/',
      blank=True, null=True,
      validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
  )
  ```
- In `projectAdd` view (`portfolio/views.py`), add a manual size check before saving (Pillow is already installed):
  ```python
  image = req.FILES.get('project_image')
  if image and image.size > 5 * 1024 * 1024:  # 5MB
      # re-render form with an error message instead of saving
      ...
  ```
- Run `makemigrations` + `migrate` after the model change.

### 1.5 Basic brute-force protection on login
- **File:** `requirements.txt`, `website/settings.py`, `portfolio/views.py`
- Install `django-axes`:
  ```
  pip install django-axes
  ```
- Add `'axes'` to `INSTALLED_APPS`, `'axes.middleware.AxesMiddleware'` to `MIDDLEWARE` (after `AuthenticationMiddleware`), and `'axes.backends.AxesStandaloneBackend'` first in `AUTHENTICATION_BACKENDS`.
- Default settings will lock out an IP after repeated failed logins — tune `AXES_FAILURE_LIMIT` if needed.

### 1.6 Change the custom admin panel's URL path
- **File:** `portfolio/urls.py`
- Rename the `admin/` prefix used by *your* custom dashboard (not the real Django `/superadmin/`) to something non-obvious, e.g. `dashboard-x7k/`, so it isn't the first thing a bot scans for. Update all `admin/...` paths and any `{% url %}` references in templates accordingly.

**✅ Phase 1 checkpoint:** no anonymous registration, all admin CRUD requires `is_staff`, `DEBUG` is env-controlled and off in prod, uploads are validated, login has lockout protection.

---

## Phase 2 — Code Structure & Cleanup

- **`website/settings.py`** — split into `settings/base.py`, `settings/dev.py`, `settings/prod.py` if the project grows further (optional for a portfolio-sized app, but sets you up well).
- **`portfolio/views.py`** — convert the repeated "grab POST fields → assign → save" pattern into Django `ModelForm`s for `Project`, `Member`, `Skill`, `Contact`. This gets you free server-side validation and cleaner views:
  ```python
  # portfolio/forms.py
  from django import forms
  from .models import Project, Member, Skill, Contact

  class ProjectForm(forms.ModelForm):
      class Meta:
          model = Project
          fields = ['project_image', 'image_url', 'project_name', 'project_about', 'technology', 'project_url', 'github_url']
  ```
  Repeat for the other three models, then simplify each view to `form = ProjectForm(req.POST, req.FILES); if form.is_valid(): form.save()`.
- **`requirements.txt`** — after adding `django-htmx` and `django-axes`, regenerate with `pip freeze > requirements.txt`.
- **Static/media in production** — confirm `whitenoise.middleware.WhiteNoiseMiddleware` is uncommented in `MIDDLEWARE` (it's currently commented out in `settings.py`) and add:
  ```python
  STORAGES = {
      "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
  }
  ```

---

## Phase 3 — HTMX Integration (no full-page reloads)

### 3.1 Install
```
pip install django-htmx
```
Add `'django_htmx'` to `INSTALLED_APPS` and `'django_htmx.middleware.HtmxMiddleware'` to `MIDDLEWARE`.
Add the CDN script once in `templates/base.html`:
```html
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

### 3.2 Contact form → no reload, instant feedback
- **Files:** `portfolio/views.py` (`contact`), `templates/contact.html`
- Create a small partial `templates/includes/contact_form.html` containing just the `<form>`.
- In `contact.html`, wrap it in a target div:
  ```html
  <div id="contact-form-wrapper">
    {% include 'includes/contact_form.html' %}
  </div>
  ```
- On the `<form>` tag: `hx-post="{% url 'contact' %}" hx-target="#contact-form-wrapper" hx-swap="outerHTML"`.
- In the view, check `req.htmx` (from `django-htmx`) — if true, return only the partial (success message or re-rendered form with errors) instead of a full redirect.

### 3.3 Project list filtering (by technology)
- **Files:** `portfolio/views.py` (`project`), `templates/project.html`
- Add filter buttons/tags (`hx-get="{% url 'project' %}?tech=Django" hx-target="#project-list" hx-push-url="true"`).
- Split `templates/project.html` into a shell + `templates/includes/project_list.html` partial containing just the grid.
- In the view, read `req.GET.get('tech')`, filter the queryset, and return the partial if `req.htmx` else the full page.

### 3.4 Admin CRUD forms (project/team/skill add)
- **Files:** `templates/admin/projectAdd.html`, `teamAdd.html`, `add-skills.html`, matching views
- Same pattern: `hx-post` the form, target a result/message div, swap in either a success toast or validation errors — no full page reload after adding a project/member/skill.

### 3.5 "Load more" / pagination (optional nice-to-have)
- If the project list grows long, paginate with Django's `Paginator` and use `hx-get` on a "Load more" button to append the next page into `#project-list` (`hx-swap="beforeend"`).

---

## Phase 4 — Mobile Responsiveness Audit

Tailwind is already the CSS framework in use — this phase is an audit + fix pass, not a rebuild.

- [ ] `templates/includes/header.html` — nav collapses into a hamburger menu below `md:` breakpoint (Alpine.js or a tiny vanilla JS toggle is enough; avoid a heavy JS framework for this).
- [ ] `templates/home.html` — hero section text/image stack vertically on mobile (`flex-col md:flex-row`).
- [ ] `templates/project.html` — grid goes from `grid-cols-1` on mobile → `sm:grid-cols-2` → `lg:grid-cols-3`.
- [ ] `templates/team.html` — same grid treatment as projects.
- [ ] `templates/about.html` — skills grid wraps cleanly at narrow widths.
- [ ] `templates/contact.html` — form inputs full-width on mobile, comfortable tap targets (`py-3` minimum on buttons/inputs).
- [ ] `templates/admin/*.html` — sidebar (`templates/admin/sidebar.html`) collapses or becomes a bottom/top bar on mobile so the dashboard is usable from a phone too.
- [ ] Images — confirm `max-w-full h-auto` (or Tailwind `object-cover` inside a fixed-ratio container) everywhere so nothing overflows on small screens.
- [ ] Test at actual breakpoints: 375px (mobile), 768px (tablet), 1024px+ (desktop) via browser dev tools.

---

## Phase 5 — Deployment Polish

- [ ] Custom `404.html` / `500.html` templates at the project template root.
- [ ] Favicon + basic meta tags (title, description, Open Graph image) in `base.html`.
- [ ] Confirm `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `settings.py` match the live domain (already partially set for `naresh-portfolio-h5oq.onrender.com`).
- [ ] Consider moving from SQLite to PostgreSQL for the production deployment if traffic/data grows (SQLite is fine for a low-traffic personal portfolio).
- [ ] Double-check `.env` is never committed (`.gitignore` already covers it — verify with `git status` after all changes).
- [ ] Run `python manage.py check --deploy` before going live — it will flag any remaining production misconfigurations directly.

---

## Execution Order Summary

1. Phase 1 (all of it) — security first, non-negotiable.
2. Phase 2 — forms/cleanup, makes Phase 3 easier.
3. Phase 3 — HTMX, section by section (contact → project filter → admin forms).
4. Phase 4 — responsive audit, page by page.
5. Phase 5 — final deployment polish, then redeploy.



# Implementation Plan Addendum — Phase 1 Fixes
Additional changes required before executing the original Phase 1 plan, found during review.

## Proposed Changes

### Dependencies
#### [MODIFY] requirements.txt
- Run `pip install django-axes` locally first.
- After all Phase 1 changes are applied and tested, regenerate with `pip freeze > requirements.txt` so `django-axes` (and its version) is captured.

---

### Project Configuration & Settings
#### [MODIFY] [settings.py](file:///d:/Programs/Deploy%20Project/My%20Portfolio/myportfolio/website/settings.py)
- In `MIDDLEWARE`, add `'axes.middleware.AxesMiddleware'` as the **last** entry in the list (after `XFrameOptionsMiddleware`) — order matters for axes to track requests correctly.
- Add near the auth settings:
```python
  AUTHENTICATION_BACKENDS = [
      'axes.backends.AxesStandaloneBackend',
      'django.contrib.auth.backends.ModelBackend',
  ]
  AXES_FAILURE_LIMIT = 5
  AXES_COOLOFF_TIME = 1  # hours
  AXES_RESET_ON_SUCCESS = True
```
  (Default `AXES_FAILURE_LIMIT` is 3, which is easy to trip during your own testing — 5 gives more headroom.)

#### [VERIFY] [.env](file:///d:/Programs/Deploy%20Project/My%20Portfolio/.env)
- Confirm `SECRET_KEY=<value>` already exists in `.env` **before** changing `settings.py` to `SECRET_KEY = os.environ["SECRET_KEY"]`. This line will crash the app at startup if the key is missing — check this first, don't assume it's set.

---

### Templates
#### [SEARCH + MODIFY] templates/ (all files)
- Before deleting the `register` URL route, run:




- Fix every match, not just `login.html` — likely candidates: `templates/base.html`, `templates/includes/header.html`, `templates/includes/footer.html`. Any leftover `{% url 'register' %}` reference will throw `NoReverseMatch` and break that page entirely once the route is removed.

---

## Verification Plan — Additions
- Confirm `.env` contains `SECRET_KEY` before applying the settings.py change (do this check first, ahead of everything else in Phase 1).
- After removing the register route, load every page (`home`, `about`, `project`, `team`, `contact`, `login`) and check none throw `NoReverseMatch`.
- Trigger 5 failed logins intentionally → confirm lockout → wait or reset via `python manage.py axes_reset` → confirm access restored.
- Run `pip freeze > requirements.txt` as the final step, after all Phase 1 code changes are confirmed working, and check the diff only adds `django-axes` (and its sub-dependencies) without touching unrelated pinned versions.