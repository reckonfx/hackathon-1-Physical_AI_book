/**
 * Test suite for VLA Validation API
 * Basic functionality tests for the VLA validation endpoints
 */

const VLAValidationAPI = require('./vla-validation');

// Create an instance of the API
const vlaAPI = new VLAValidationAPI();

console.log('=== VLA Validation API Test Suite ===\n');

// Test 1: Validate VLA example
async function testValidateVLA() {
  console.log('Test 1: Validate VLA Example');

  const requestBody = {
    simulation_type: 'voice-processing',
    example_path: './examples/vla/voice-processing/basic-command.py',
    validation_criteria: ['syntax', 'structure', 'execution']
  };

  try {
    const result = await vlaAPI.validateVLA(requestBody);
    console.log('✓ Validation successful:', result);
    console.log(`  - Valid: ${result.is_valid}`);
    console.log(`  - Issues: ${result.issues.length}`);
    console.log(`  - Suggestions: ${result.suggestions.length}\n`);
  } catch (error) {
    console.error('✗ Validation failed:', error.message);
  }
}

// Test 2: Get VLA Examples
async function testGetVLAExamples() {
  console.log('Test 2: Get VLA Examples');

  try {
    const allExamples = await vlaAPI.getVLAExamples();
    console.log('✓ Retrieved all examples:', allExamples.length);

    const filteredByEnv = await vlaAPI.getVLAExamples({ environment: 'simulation' });
    console.log('✓ Filtered by environment (simulation):', filteredByEnv.length);

    const filteredByType = await vlaAPI.getVLAExamples({ type: 'voice-processing' });
    console.log('✓ Filtered by type (voice-processing):', filteredByType.length);

    console.log('  Sample example:', allExamples[0]);
    console.log('');
  } catch (error) {
    console.error('✗ Example retrieval failed:', error.message);
  }
}

// Run tests
async function runTests() {
  await testValidateVLA();
  await testGetVLAExamples();

  console.log('=== Test Suite Complete ===');
}

// Execute tests
runTests().catch(console.error);