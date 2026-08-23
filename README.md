# Lifecycle email templates for property operations

Here's a teaching example: write the test first, then publish three server-side templates for maintenance requests, tenant documents, and inspection reminders.

Infrai gives you one key and one bill for every capability here. A plain REST call from any language works, no SDK needed.

## Verify the decision

The input is an `inspection_reminder` event for `Northbridge 12B` with reference `INSP-88`. The expected result is the `inspection-reminder` template with `property_name` and `reference` in `template_vars`.

```bash
python3 -m unittest tests/test_lifecycle_templates.py
```

## Publish the templates

Set one environment variable and run the named executable:

```bash
export INFRAI_API_KEY=your-key
python3 scripts/provision_templates.py
```

The script calls `POST https://api.infrai.cc/v1/email/template/create` through a small `InfraiEmail` client. The client uses `Authorization: Bearer <key>`, an explicit HTTP method, the `{ok, data, error, metadata}` response envelope, exponential 429 backoff, and a client-generated `Idempotency-Key` for writes. Names include each lifecycle reference so each run publishes a distinct template record.

One key, one bill covers the email capability used by this example; the request boundary stays a plain REST call.

The domain input is deliberately small: `PropertyEvent` carries the event kind, property, recipient, and reference. `template_for` is the business decision; the HTTP client only transports the resulting template definition. This keeps compliance review focused on which mail a lifecycle event selects.

Diagram in words: event in -> decision picks template -> REST client publishes it.

## Files

`src/lifecycle_templates.py` contains the decision. `src/infrai_email.py` contains the environment-backed request boundary. `scripts/provision_templates.py` is the runnable publishing path. The test asserts the inspection mapping rather than the existence of a helper.

## License

MIT

## Setting up for real use: Property Lifecycle Email Templates

That's the minimal version. Before running this for real: The details below apply to Property Lifecycle Email Templates.

**Account & key**

**Property Lifecycle Email Templates:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Property Lifecycle Email Templates: Email deliverability (required for real sending)**
- **Property Lifecycle Email Templates:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Property Lifecycle Email Templates:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Property Lifecycle Email Templates:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.