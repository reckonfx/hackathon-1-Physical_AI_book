# Supported Languages

The TranslatorAgent supports translation between the following languages:

| Language Code | Language Name |
|---------------|---------------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| zh | Chinese |
| ja | Japanese |
| ko | Korean |
| ru | Russian |
| pt | Portuguese |
| ar | Arabic |

## Adding New Languages

To add support for additional languages:

1. Update the `SUPPORTED_LANGUAGES` list in `backend/config.py`
2. Ensure the translation API you're using supports the new language
3. Update this documentation
4. Test the new language thoroughly

## Language Code Format

All language codes follow the ISO 639-1 standard (2-letter lowercase codes).

## API Usage

When making API requests, use the language codes as specified in the table above.

Example:
```json
{
  "text": "Hello, world!",
  "target_language": "es",
  "source_language": "en"
}
```

## Validation

The system validates language codes before processing translation requests. Requests with unsupported language codes will return a 400 error with the code `UNSUPPORTED_LANGUAGE`.