# Google Prompt Engineering Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Model Parameters](#model-parameters)
3. [Core Prompting Techniques](#core-prompting-techniques)
4. [Advanced Reasoning Techniques](#advanced-reasoning-techniques)
5. [Output Control Strategies](#output-control-strategies)
6. [Code Prompting Techniques](#code-prompting-techniques)
7. [Best Practices](#best-practices)
8. [Example Templates](#example-templates)
9. [References](#references)

---

## Introduction

This guide synthesizes prompt engineering techniques from Google's official whitepaper by Lee Boonstra and Google Cloud's documentation. It complements the foundational techniques covered in our main prompt engineering guide with Google-specific approaches and recommendations.

### Why Prompt Engineering Matters

Prompt engineering is the process of designing effective instructions for large language models (LLMs) to achieve desired outputs. Well-crafted prompts can dramatically improve:

- Response quality and relevance
- Reasoning capabilities
- Output format consistency
- Code generation accuracy
- Error reduction and handling
- Task completion rates

### Google's Approach to Prompt Engineering

Google's approach emphasizes:
- Structured, clear instructions
- Example-driven learning
- Step-by-step reasoning
- Output format control
- Parameter optimization for different use cases

---

## Model Parameters

### Temperature

Controls randomness in token selection:
- **Low (0-0.3)**: More deterministic, focused responses
- **Medium (0.4-0.7)**: Balanced creativity and coherence
- **High (0.8-1.0)**: More diverse, creative outputs

Best for:
- Low: Factual responses, code generation
- Medium: Content creation, balanced responses
- High: Creative writing, brainstorming

### Top-P (Nucleus Sampling)

Dynamically selects from tokens whose cumulative probability exceeds the threshold:
- **Low (0.5)**: More predictable, limited token choices
- **High (0.95)**: Considers wider range of tokens

Controls how the model samples from the probability distribution.

### Top-K

Limits token selection to the K highest-probability options:
- **Low K (10-20)**: More focused outputs
- **High K (30-50)**: More variability

### Recommended Parameter Combinations

| Use Case | Temperature | Top-P | Top-K |
|----------|-------------|-------|-------|
| Default/Balanced | 0.2 | 0.95 | 30 |
| Creative | 0.9 | 0.99 | 40 |
| Deterministic | 0.1 | 0.9 | 20 |
| Code generation | 0.1 | 0.9 | 10 |

---

## Core Prompting Techniques

### Zero-Shot Prompting

Provide instructions without examples:

```
Generate a summary of this article about climate change.
```

Best for:
- Simple, straightforward tasks
- When model already understands the domain
- Tasks with clear objectives

### One-Shot Prompting

Include a single example alongside your task description:

```
Classify the sentiment of the following reviews:

Example:
Review: "This restaurant exceeded all my expectations. Amazing food!"
Sentiment: Positive

Review: "The service was slow and the food was cold."
Sentiment:
```

Best for:
- Demonstrating specific output formats
- Setting tone and style
- Guiding the model when zero-shot fails

### Few-Shot Prompting

Provide multiple examples (typically 3-5) to establish patterns:

```
Translate English to French:

English: The weather is beautiful today.
French: Le temps est beau aujourd'hui.

English: I would like to order dinner.
French: Je voudrais commander le dîner.

English: Where is the nearest train station?
French:
```

Best for:
- Complex tasks requiring pattern recognition
- Ensuring consistent output formatting
- Teaching specific response styles

### System Prompting

Set high-level instructions about the model's role:

```
You are a helpful AI assistant specializing in cybersecurity. Only answer questions related to cybersecurity best practices, and politely decline to answer questions outside your area of expertise.
```

Best for:
- Establishing guardrails and behavior
- Enforcing output constraints
- Setting consistent tone across interactions

### Contextual Prompting

Embed relevant background information:

```
Context: This is an email to a senior executive at a Fortune 500 company who is not familiar with technical jargon.

Write a summary of the recent data breach incident that explains the impact without using technical terms.
```

Best for:
- Domain-specific tasks
- Tailoring responses to specific audiences
- Providing necessary background knowledge

### Role Prompting

Assign a specific persona to the model:

```
Act as an experienced pediatrician explaining vaccinations to concerned parents.
```

Best for:
- Shaping tone and vocabulary
- Accessing domain expertise
- Creating consistent perspective

---

## Advanced Reasoning Techniques

### Chain-of-Thought (CoT) Prompting

Instruct the model to show its reasoning process step-by-step:

```
Solve this math problem step-by-step:
If a shirt costs $15 with a 20% discount, and I buy 3 shirts, what is my total cost?
```

Example response pattern:
```
Step 1: Calculate the discount amount per shirt: $15 × 0.20 = $3
Step 2: Calculate the discounted price per shirt: $15 - $3 = $12
Step 3: Calculate the total cost for 3 shirts: $12 × 3 = $36
Therefore, the total cost is $36.
```

Best for:
- Complex reasoning tasks
- Math problems
- Multi-step logical deductions
- Debugging potential errors

### Step-Back Prompting

First think abstractly about the problem, then solve the specific task:

```
To solve this problem, I'll first think broadly about the key concepts involved, then tackle the specific question.

Problem: What happens to the acceleration of a falling object as it approaches terminal velocity?

First, let me consider the forces acting on falling objects in general...
```

Best for:
- Complex problems with conceptual foundations
- Questions requiring domain knowledge
- Preventing fixation on incorrect approaches

### Self-Consistency Prompting

Generate multiple reasoning paths and select the most consistent answer:

```
Problem: A ball is thrown up with an initial velocity of 15 m/s. If the acceleration due to gravity is -10 m/s², how high will the ball go?

Let me solve this 3 different ways:

Method 1: Using the formula v² = v₀² + 2a(x - x₀)...
Method 2: Using the formula x = x₀ + v₀t + ½at²...
Method 3: Using energy conservation principles...
```

Best for:
- Problems with potential for calculation errors
- High-stakes situations requiring verification
- Complex reasoning tasks

### Tree of Thoughts (ToT)

Explore multiple reasoning branches simultaneously:

```
Problem: Create the most effective marketing strategy for a new eco-friendly water bottle.

Let me explore multiple approaches:

Branch 1: Sustainability focus
- Step 1.1: Research consumer attitudes toward sustainability...
- Step 1.2: Analyze competitors' sustainability messaging...

Branch 2: Lifestyle/Design focus
- Step 2.1: Consider target demographic lifestyle needs...
- Step 2.2: Examine design-focused marketing campaigns...

Branch 3: Performance/Functionality focus
- Step 3.1: Identify key performance advantages...
- Step 3.2: Compare functional benefits to competitors...
```

Best for:
- Creative problem-solving
- Strategic planning
- Decisions with multiple viable approaches
- Complex problems with interdependent factors

### ReAct Prompting (Reason + Act)

Combine reasoning with concrete actions:

```
Question: What was the GDP growth rate in Japan for 2022?

Thought: I need to find recent economic data for Japan. I should search for Japan's GDP growth in 2022.
Action: Search for "Japan GDP growth rate 2022"
Observation: Japan's GDP grew by 1.0% in 2022 according to World Bank data.
Thought: Now I have the answer. Japan's GDP growth rate was 1.0% in 2022.
Action: Provide the final answer.
Answer: Japan's GDP growth rate in 2022 was 1.0%.
```

Best for:
- Research-based tasks
- Information gathering
- Multi-step processes
- Tool use integration

---

## Output Control Strategies

### Structured Output Formats

Specify the exact format for responses:

```
Create a product review summary in the following JSON format:
{
  "product_name": "",
  "overall_rating": 1-5,
  "pros": ["", "", ""],
  "cons": ["", ""]
}
```

Supported formats:
- JSON
- HTML
- Markdown
- CSV
- XML
- YAML
- Custom structures

### Response Length Control

Control verbosity through explicit instructions:

```
Explain quantum computing in exactly 3 sentences.
```

Or by specifying character/word counts:

```
Write a 50-word biography of Marie Curie.
```

### Output Stylization

Control tone, style, and audience level:

```
Explain how blockchain works. Write at an 8th-grade reading level using simple analogies.
```

Style dimensions to specify:
- Formality (formal vs. casual)
- Complexity (technical vs. simple)
- Tone (serious, lighthearted, enthusiastic)
- Audience knowledge level
- Cultural context

---

## Code Prompting Techniques

### General Coding Best Practices

1. **Be specific about language and framework**:
   ```
   Write a Python function using TensorFlow to perform linear regression.
   ```

2. **Provide context and requirements**:
   ```
   Create a Java method that validates email addresses. It should check for proper format, domain validity, and reject disposable email domains. Performance is a priority as this will be called frequently.
   ```

3. **Request test cases**:
   ```
   Write a JavaScript function to find the longest common substring of two input strings. Include test cases covering edge cases like empty inputs and no common substrings.
   ```

### Debugging Prompts

Provide code with errors and specific debugging objectives:

```
Debug this Python code that's supposed to find the median of a list but returns incorrect results for even-length lists:

def find_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 1:
        return sorted_numbers[n // 2]
    else:
        return sorted_numbers[n // 2]
```

### Code Optimization

Request performance or readability improvements:

```
Optimize this function for performance while maintaining readability:

function findDuplicates(array) {
  let duplicates = [];
  for (let i = 0; i < array.length; i++) {
    for (let j = i + 1; j < array.length; j++) {
      if (array[i] === array[j] && !duplicates.includes(array[i])) {
        duplicates.push(array[i]);
      }
    }
  }
  return duplicates;
}
```

### Code Documentation

Generate or improve documentation:

```
Add comprehensive JSDoc comments to this JavaScript class:

class DataProcessor {
  constructor(sourceData) {
    this.data = sourceData;
    this.processed = false;
  }
  
  normalize() {
    if (!this.data || this.data.length === 0) return [];
    const sum = this.data.reduce((a, b) => a + b, 0);
    const average = sum / this.data.length;
    return this.data.map(val => val / average);
  }
  
  process(options = {}) {
    const { filterOutliers = true, normalizeValues = true } = options;
    let result = [...this.data];
    
    if (filterOutliers) {
      const q1 = this.getQuantile(0.25);
      const q3 = this.getQuantile(0.75);
      const iqr = q3 - q1;
      const lower = q1 - 1.5 * iqr;
      const upper = q3 + 1.5 * iqr;
      result = result.filter(val => val >= lower && val <= upper);
    }
    
    if (normalizeValues) {
      result = this.normalize(result);
    }
    
    this.processed = true;
    return result;
  }
  
  getQuantile(q) {
    const sorted = [...this.data].sort((a, b) => a - b);
    const pos = q * (sorted.length - 1);
    const base = Math.floor(pos);
    const rest = pos - base;
    if (sorted[base + 1] !== undefined) {
      return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
    } else {
      return sorted[base];
    }
  }
}
```

### Unit Test Generation

Request tests for specific code:

```
Generate pytest unit tests for this Python function:

def validate_password(password):
    """
    Validates a password based on the following rules:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character from !@#$%^&*()-_=+
    
    Returns True if valid, False otherwise.
    """
    if len(password) < 8:
        return False
        
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_chars = "!@#$%^&*()-_=+"
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True
    
    return has_upper and has_lower and has_digit and has_special
```

---

## Best Practices

### 1. Start Simple and Iterate

Begin with simple, clear prompts and refine based on results:

1. Write an initial prompt
2. Evaluate the response
3. Identify issues or areas for improvement
4. Refine the prompt
5. Repeat until satisfactory

### 2. Be Specific and Explicit

Provide clear, detailed instructions:

❌ "Write about climate change."  
✅ "Write a 300-word explanation of how rising global temperatures affect marine ecosystems, focusing on coral reefs and ocean acidification."

### 3. Use Positive Instructions Over Constraints

Frame instructions positively rather than as prohibitions:

❌ "Don't use technical jargon."  
✅ "Use simple, everyday language that a high school student would understand."

### 4. Provide High-Quality Examples

Include diverse, representative examples:

```
Classify these customer reviews as positive, neutral, or negative:

Example 1: "The product arrived damaged and customer service was unhelpful." → Negative
Example 2: "Fast shipping and the quality is decent for the price." → Positive
Example 3: "It works as expected, nothing special." → Neutral

Review to classify: "Shipping took longer than promised but the item was well-packaged."
```

### 5. Use Variables for Dynamic Elements

Parameterize prompts for reuse and testing:

```
Summarize this {{content_type}} about {{topic}} in {{number}} bullet points, focusing on {{aspect}}.
```

### 6. Regularly Test Across Model Versions

Re-test prompts when:
- Switching between models
- After model updates
- With different parameter settings

### 7. Document Prompt Versions and Performance

Track prompt iterations:
- Version number
- Changes made
- Performance metrics
- Date tested
- Model version used

### 8. Test Edge Cases

Validate prompts with challenging inputs:
- Empty or minimal inputs
- Extremely long inputs
- Inputs with unusual formatting
- Ambiguous or edge case scenarios

---

## Example Templates

### Product Analysis Template

```
Analyze this product description in detail:

Product: {{product_description}}

Provide an analysis with these sections:
1. Target Audience: Identify the primary and secondary customer segments.
2. Key Benefits: List the top 3 benefits highlighted in the description.
3. Competitive Positioning: How does this product differentiate itself?
4. Improvement Suggestions: Recommend 2-3 ways the description could be enhanced.

Format your response as bullet points under each section heading.
```

### Technical Tutorial Template

```
Create a step-by-step tutorial on how to {{specific_task}} using {{technology/tool}}.

Your tutorial should include:
- Prerequisites (required software, background knowledge)
- Initial setup instructions
- Step-by-step implementation with code examples
- Common errors and troubleshooting tips
- Next steps for building upon this tutorial

Target audience: {{beginner/intermediate/advanced}} developers with {{specific_background}}.
```

### Data Analysis Template

```
Analyze the following data set:

{{data}}

Generate a comprehensive report with these sections:
1. Key Statistics (mean, median, range, etc.)
2. Trends and Patterns
3. Anomalies or Outliers
4. Correlations Between Variables
5. Recommendations Based on Data Insights

Include appropriate visualizations you would recommend creating to highlight key findings.
```

### Code Review Template

```
Conduct a thorough code review of the following {{language}} code:

```{{programming_language}}
{{code_block}}
```

Your review should address:
1. Functionality: Does the code work as intended?
2. Readability: Is the code clear and well-documented?
3. Performance: Are there efficiency concerns?
4. Security: Are there potential vulnerabilities?
5. Best Practices: Does the code follow {{language}} conventions?

For each issue identified:
- Reference the specific line numbers
- Explain the problem
- Suggest a concrete improvement
- Provide sample code for critical fixes
```

---

## References

- Google Cloud (2023). [Prompt Engineering Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design)
- Boonstra, L. (2023). [Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering)
- Wei et al. (2022). [Chain of Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- Google Developers (2023). [Prompt Engineering for Generative AI](https://developers.google.com/machine-learning/resources/prompt-eng)
- PromptHub (2023). [Google's Prompt Engineering Best Practices](https://www.prompthub.us/blog/googles-prompt-engineering-best-practices)
