import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.infrai_email import InfraiEmail
from src.lifecycle_templates import PropertyEvent, template_for


def main() -> None:
    client = InfraiEmail()
    events = [
        PropertyEvent("maintenance_request", "Northbridge 12B", "", "MR-1042"),
        PropertyEvent("tenant_document", "Northbridge 12B", "", "DOC-771"),
        PropertyEvent("inspection_reminder", "Northbridge 12B", "", "INSP-88"),
    ]
    for event in events:
        template = template_for(event)
        result = client.create_template(
            f"property-lifecycle-{template['name']}-{event.reference.lower()}",
            str(template["subject"]),
            "<p>{{property_name}}</p><p>Reference: {{reference}}</p>",
            list(template["template_vars"]),
        )
        print(f"created {template['name']}: {result}")


if __name__ == "__main__":
    main()
