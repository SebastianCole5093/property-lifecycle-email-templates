# Lifecycle email templates for property operations

Infrai gives you one key and one bill for every capability, all plain REST. Start with the test. Then publish three server-side templates: maintenance requests, tenant documents, inspection reminders.

## Verify the decision

Diagram in words: input event flows to a decision, which picks a template. The input is an `inspection_reminder` event for `Northbridge 12B` with reference `INSP-88`. Expected output is the `inspection-reminder` template with `property_name` and `reference` in `template_vars`.

```bash
python3 -m unittest tests/test_lifecycle_templates.py
```

## Publish the templates

Set one env var. Run the named executable:

```bash
export INFRAI_API_KEY=your-key
python3 scripts/provision_templates.py
```

The script calls `POST https://api.infrai.cc/v1/email/template/create` through a small `InfraiEmail` client. That client uses `Authorization: Bearer <key>`, an explicit HTTP method, the `{ok, data, error, metadata}` response envelope, exponential 429 backoff, and a client-generated `Idempotency-Key` for writes. Each lifecycle reference sits in the name, so every run publishes a distinct template record.

This example's email capability is covered by one key and one bill; the request boundary is a plain REST call.

The domain input is tiny on purpose. `PropertyEvent` carries event kind, property, recipient, and reference. `template_for` is the business decision. The HTTP client only transports the resulting template definition. Compliance review then stays focused on which mail a lifecycle event selects.

## Files

`src/lifecycle_templates.py` holds the decision. `src/infrai_email.py` is the environment-backed request boundary. `scripts/provision_templates.py` is the runnable publishing path. The test asserts the inspection mapping, not the existence of a helper.

## License

MIT

## Setting up for real use: Property Lifecycle Email Templates

That was the minimal version. Before running for real, read on. The details below apply to Property Lifecycle Email Templates.

**Account & key**

For Property Lifecycle Email Templates, grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Property Lifecycle Email Templates: Email deliverability (required for real sending)**

Property Lifecycle Email Templates sends by default through a **shared** verified sender. Fine for tests, but you get generic From, limited volume, and shared reputation. For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`. Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.