import unittest

from src.lifecycle_templates import PropertyEvent, template_for


class LifecycleTemplateTest(unittest.TestCase):
    def test_inspection_event_selects_reference_fields(self) -> None:
        event = PropertyEvent("inspection_reminder", "Northbridge 12B", "tenant@example.com", "INSP-88")
        result = template_for(event)
        self.assertEqual(result["name"], "inspection-reminder")
        self.assertEqual(result["template_vars"], ["property_name", "reference"])


if __name__ == "__main__":
    unittest.main()

