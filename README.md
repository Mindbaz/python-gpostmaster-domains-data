# Google Postmaster Data

Unofficial tool to download and flatten data from GPT (Google Postmaster Tools API **v2**). The recovered data will offer a simple schema in order to be able to easily save this data in a flat file or in database

## Schema

* user_report_spam_percent : `float|None`
* domain_compliance : `dict|None`
* feedback_loop : `{ nb_row: 0, percent_per_uid: list }`
* auth_use_dkim_percent : `float|None`
* auth_use_spf_percent : `float|None`
* auth_use_dmarc_percent : `float|None`
* tls_inbound_percent : `float|None`
* delivery_errors : `list`
* domain : `str`
* date : `str`

### domain_compliance

Compliance status of the domain, as returned by GPT's `getComplianceStatus`. Unlike the old `domain_reputation` int level, this is not a score and is not tied to a specific date : it reflects the domain's compliance state at the time of the call

```jsonc
{
    'deliverability': {
        'status': 'compliant'|'needs_work'|null,
        'reason': str|null
    },
    'one_click_unsubscribe': {
        'status': 'compliant'|'needs_work'|null,
        'reason': str|null
    },
    'honor_unsubscribe': {
        'status': 'compliant'|'needs_work'|null,
        'reason': str|null
    },
    'checks': [
        { 'check': str, 'status': 'compliant'|'needs_work'|null },
        { 'check': str, 'status': 'compliant'|'needs_work'|null },
        { 'check': str, 'status': 'compliant'|'needs_work'|null },
        ...
    ]
}
```

### feedback_loop

```
percent_per_uid : [ { 'uid': int, 'spam_percent': float } ]
```

### delivery_errors

```
[ { 'class': str, 'type': str, 'percent': float } ]
```

## Migration notes (v1 -> v2)

Google retired the v1/v1beta1 Postmaster Tools API in favor of a metric-query based v2 API (`domains().domainStats().query(...)` and `domains().getComplianceStatus(...)` instead of a single `domains().trafficStats().get(...)` call per domain/date). This changes the schema returned by this library :

* `domain_reputation` (int level 0-4) and `ips_reputations` (per-ip reputation breakdown) no longer have **any** equivalent in v2 : Google removed the reputation bars entirely. `domain_reputation` is replaced by `domain_compliance`, sourced from the new `getComplianceStatus` endpoint. `ips_reputations` has no replacement at all in v2 (no per-ip data is exposed anywhere in the API) and is kept in the schema, always empty, for backward compatibility only
* `feedback_loop` now requires two sequential GPT calls per domain/date (discover the feedback loop ids used that day, then query the spam rate of each id) instead of one
* `delivery_errors` is reconstructed from up to 10 filtered `DELIVERY_ERROR_RATE` metrics (one per known `error_type`/`error_reason` combination) requested in a single `query()` call, to keep the same class/type granularity as before
* `user_report_spam_percent`, `auth_use_*_percent` and `tls_inbound_percent` are sourced from the new `SPAM_RATE`, `AUTH_SUCCESS_RATE` and `TLS_ENCRYPTION_RATE` metrics ; they are assumed to be 0-1 ratios like their v1 counterparts, but this has not been validated against real GPT data
* Requires `google-api-python-client` >= 2.196.0 (bundles the v2 discovery document).

## Domain registration & verification

On top of the read-only stats/compliance calls, `GPostmaster` also exposes domain registration :

* `create_domain ( domain: str ) -> dict` : registers the domain on the GPT account, then fetches its DNS verification token. Returns `{ 'state': True, 'token': str }` on success, `{ 'state': False }` if GPT rejects the creation (e.g. already registered)
* `get_domain_verify_token ( domain: str ) -> str` : (re)fetches the DNS TXT token to post for a domain. Note : GPT returns a token even if the domain hasn't been created yet
* `verify_domain ( domain: str ) -> bool` : triggers DNS-level verification (TXT record) for a domain, once the token has been posted and propagated. Returns `True`/`False`, not detailed state — GPT's `verify` response is always empty ; call `create_domain`/GPT's `domains().get()` afterwards if you need the up to date `verificationState`

These require the `https://www.googleapis.com/auth/postmaster` scope on top of `postmaster.domain`, both included in `GPostmaster.scopes`.

```python
from googlepostmasterapi.gpt import GPostmaster

g = GPostmaster ( token = 'path/to/token.json' )

created = g.create_domain ( domain = 'mkt.mydomain.com' )
# { 'state': True, 'token': 'google-site-verification=...' }
# -> post created['token'] as a DNS TXT record on mkt.mydomain.com, wait for propagation

verified = g.verify_domain ( domain = 'mkt.mydomain.com' )
# True/False
```

# How to use it

```bash
python entry_points_googlepostmasterapi/gpt_create_domain.py -h
usage: gpt_create_domain [-h] [--token [TOKEN]] [--domain [DOMAIN]] [--verbose] [--version]
```

```bash
python entry_points_googlepostmasterapi/gpt_dl_all_data.py -h
usage: gpt_dl_all_data [-h] [--token [TOKEN]] [--pool-size [POOL_SIZE]] [--date [DATE]] [--verbose] [--version]
```

```bash
python entry_points_googlepostmasterapi/gpt_dl_domain_data.py -h
usage: gpt_dl_domain_data [-h] [--token [TOKEN]] [--domain [DOMAIN]] [--date [DATE]] [--verbose] [--version]
```

```bash
python entry_points_googlepostmasterapi/gpt_dl_domains.py -h
usage: gpt_dl_domains [-h] [--token [TOKEN]] [--verbose] [--version]
```

```bash
python entry_points_googlepostmasterapi/gpt_get_domain_verify_token.py -h
usage: gpt_get_domain_verify_token [-h] [--token [TOKEN]] [--domain [DOMAIN]] [--verbose] [--version]
```

```bash
python entry_points_googlepostmasterapi/gpt_verify_domain.py -h
usage: gpt_verify_domain [-h] [--token [TOKEN]] [--domain [DOMAIN]] [--verbose] [--version]
```

# Support version

Python : `>=3.9`
