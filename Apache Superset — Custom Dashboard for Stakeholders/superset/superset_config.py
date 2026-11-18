# Local training-only configuration. Change SECRET_KEY for non-local use.
SECRET_KEY = "replace-this-local-demo-secret-key-before-production"
ENABLE_PROXY_FIX = False
WTF_CSRF_ENABLED = True
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
}
