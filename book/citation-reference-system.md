# Citation and Reference System for Official Documentation Links

## Purpose
This document establishes the standard approach for citing and referencing official documentation in the Physical AI Book. All technical content must be grounded in official documentation with proper citations to ensure accuracy and avoid hallucination.

## Citation Principles

### 1. Official Sources Only
- Use only official documentation from:
  - ROS 2 official documentation
  - NVIDIA Isaac Sim documentation
  - OpenAI API documentation
  - Docusaurus documentation
  - Python official documentation
  - Other vendor-provided official resources
- Avoid unofficial blogs, forums, or secondary sources
- When possible, cite the specific version of documentation used

### 2. Verification Requirement
- All technical claims must be verified against official documentation
- Include direct links to the official source when available
- Quote directly from official documentation when possible
- Paraphrase accurately when summarizing official content

## Citation Format

### Inline Citations
For inline references to official documentation:
```
According to the ROS 2 documentation [^ros2-actions], action servers provide...
```

[^ros2-actions]: ROS 2 Documentation - Actions, https://docs.ros.org/en/rolling/Concepts/About-Actions.html

### Block Citations
For longer quotes or detailed references:
```
> As stated in the NVIDIA Isaac Sim documentation:
>
> "Isaac Sim is a modular robotics environment software suite that provides a scalable solution for developing, training, and testing AI-based robotics applications." [^isaac-sim-overview]
```

[^isaac-sim-overview]: NVIDIA Isaac Sim Documentation - Overview, https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html

### Code Example Citations
When referencing official code examples:
```
This implementation follows the pattern outlined in the official ROS 2 tutorials [^ros2-publisher-tutorial]:

```python
# Example code here
```

[^ros2-publisher-tutorial]: ROS 2 Publisher Tutorial, https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
```

## Reference Management

### 1. Link Verification
- Regularly verify that cited links remain accessible
- Update broken links when documentation moves
- Maintain a master list of common references for consistency

### 2. Version Tracking
- Include version information when citing documentation that may change significantly
- Note if content is specific to a particular version
- Update references when upgrading to new versions

### 3. Accuracy Checks
- Verify that quoted content matches the original exactly
- Ensure paraphrased content maintains the original meaning
- Double-check technical details against multiple official sources when available

## Prohibited Practices

### 1. No Self-Citation
- Do not cite content created within this book as authoritative
- Only cite external official documentation
- When referring to other parts of this book, use internal linking instead of citations

### 2. No Speculation
- Do not include information not supported by official documentation
- If official documentation is unclear, acknowledge the ambiguity rather than guessing
- When multiple official sources conflict, cite both and explain the discrepancy

## Quality Assurance
- All content must pass citation verification before publication
- Peer reviewers will check for proper citation of technical claims
- Automated tools will verify link accessibility where possible