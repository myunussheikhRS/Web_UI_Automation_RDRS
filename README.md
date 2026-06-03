# Web_UI_Automation_RDRS
Web UI automation framework developed using Playwright (Python) following the Page Object Model (POM) approach. Integrated with PyTest for scalable test execution and an extent-style HTML reporting layer for detailed test insights.

## Reporting

- Report file: `reports/extent_style_report.html`
- Screenshot folder: `reports/screenshots`
- Each test row includes module/class, method, assertion counts, and screenshot reference.
- Each test detail section includes validation/assertion table: method, field, expected, actual, and status.

Run tests:

```bash
pytest
```
