from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyEvent:
    kind: str
    property_name: str
    recipient: str
    reference: str


def template_for(event: PropertyEvent) -> dict[str, object]:
    if event.kind == "maintenance_request":
        return {"name": "maintenance-request", "subject": f"Maintenance request {event.reference}", "template_vars": ["property_name", "reference"]}
    if event.kind == "tenant_document":
        return {"name": "tenant-document", "subject": f"Document received for {event.property_name}", "template_vars": ["property_name", "reference"]}
    if event.kind == "inspection_reminder":
        return {"name": "inspection-reminder", "subject": f"Inspection reminder for {event.property_name}", "template_vars": ["property_name", "reference"]}
    raise ValueError(f"unsupported lifecycle event: {event.kind}")

