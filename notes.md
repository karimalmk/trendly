# Task List

#### Current branch:
- Start on backtesting page, learning Matplotlib

#### Next branch:
- Incorporate unittest and django testcase
- Wrap deletion view inside atomic transaction (from django.db import transaction) decorator to release locks immediately

#### Future features:
- Add manual JS routing of URLs (from history or otherwise) to enable deep linking, shared links etc., i.e. don't just rely on sessionStorage logic which is currently being implemented to reconstruct the DOM on DOMContentLoad when you navigate to any URL (recall: this is enabled by your SPA fallback view in urls.py)
- Add the recording page and option to add recordings from watchlist
- Add portfolio creation and back-testing
- Add sorting of stocks in watchlist