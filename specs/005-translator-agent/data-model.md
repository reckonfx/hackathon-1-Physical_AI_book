# Data Model: TranslatorAgent

## Entities

### TranslationRequest
- **text**: string (required) - The source text to be translated (max 1000 characters)
- **target_language**: string (required) - The language code to translate to (e.g., 'en', 'es', 'fr')
- **source_language**: string (optional) - The language code of the source text (if not provided, auto-detect)
- **preserve_formatting**: boolean (optional, default: true) - Whether to attempt to preserve original formatting
- **glossary_ref**: boolean (optional, default: false) - Whether to include glossary references for technical terms

### TranslationResponse
- **translated_text**: string (required) - The translated text content
- **detected_source_language**: string (optional) - The detected source language code
- **target_language**: string (required) - The target language code
- **confidence**: number (optional) - Confidence score of the translation (0-1)
- **technical_terms**: array (optional) - List of technical terms preserved in original form
- **char_count**: number (required) - Character count of original text
- **processing_time**: number (required) - Time taken to process the request in milliseconds

### LanguageDetectionRequest
- **text**: string (required) - The text to analyze for language detection (max 1000 characters)

### LanguageDetectionResponse
- **detected_language**: string (required) - The detected language code (e.g., 'en', 'es', 'fr')
- **confidence**: number (optional) - Confidence score of the detection (0-1)
- **all_matches**: array (optional) - Array of all possible language matches with confidence scores
- **char_count**: number (required) - Character count of input text

## Validation Rules

### TranslationRequest
- `text` must be between 1 and 1000 characters (inclusive)
- `target_language` must be a valid ISO 639-1 language code from supported languages list
- If `source_language` is provided, it must be a valid ISO 639-1 language code
- If `source_language` is not provided, automatic detection will be performed

### LanguageDetectionRequest
- `text` must be between 1 and 1000 characters (inclusive)
- `text` should contain sufficient content for reliable detection (minimum 3 words recommended)

## State Transitions

### Translation Process
1. **Received**: Request received with validation passed
2. **Detecting**: If source language not specified, performing language detection
3. **Translating**: Sending request to translation API
4. **Processing**: Post-processing translation (formatting, term preservation)
5. **Completed**: Response ready with translation and metadata
6. **Failed**: Error occurred during processing

### Language Detection Process
1. **Received**: Request received with validation passed
2. **Detecting**: Performing language detection on text
3. **Completed**: Response ready with detected language and confidence
4. **Failed**: Error occurred during detection