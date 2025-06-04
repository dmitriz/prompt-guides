# Complete Prompt Engineering Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Core Principles](#core-principles)
3. [Planning Framework](#planning-framework)
4. [Advanced Techniques](#advanced-techniques)
5. [Quality Control & Validation](#quality-control--validation)
6. [Real-World Applications](#real-world-applications)
7. [Best Practices & Anti-Patterns](#best-practices--anti-patterns)
8. [Templates & Examples](#templates--examples)

---

## Introduction

Prompt engineering is a discipline for developing and optimizing prompts to efficiently use language models (LMs) for a wide variety of applications. As Cursor co-founder Arvid coined in 2023, "Prompt Design" remains the most fitting term for the process of writing and optimizing prompts.

This guide synthesizes knowledge from leading AI companies like Parahelp (serving Perplexity, Framer, Replit, ElevenLabs), Anthropic, OpenAI, and extensive research from the prompt engineering community.

### Key Success Metrics
- **Customer Support**: % of tickets resolved end-to-end
- **Development**: Code quality and task completion rates  
- **General AI**: Accuracy, relevance, and safety of responses

### When to Use Prompt Engineering vs. Fine-tuning

**Prompt Engineering Advantages:**
- **Resource Efficiency**: Only requires text input vs. high-end GPUs and large memory
- **Cost-Effectiveness**: Uses base model pricing vs. expensive fine-tuning costs
- **Model Updates**: Works across versions without retraining
- **Time-Saving**: Instantaneous results vs. hours/days of training
- **Minimal Data**: Works with few-shot or zero-shot learning
- **Flexibility**: Rapid iteration and experimentation
- **Transparency**: Human-readable prompts aid debugging
- **Preserves Knowledge**: No catastrophic forgetting of general capabilities

---

## Core Principles

### 1. Clarity and Directness
- Use clear, specific instructions
- Avoid ambiguous language
- State expectations explicitly
- Define success criteria upfront

### 2. Structure and Organization
- Use consistent formatting (Markdown, XML)
- Organize information hierarchically
- Separate instructions, examples, and context
- Use clear section headers and dividers

### 3. Context and Examples
- Provide relevant examples (few-shot prompting)
- Include edge cases in examples
- Use diverse, representative samples
- Show both correct and incorrect patterns

### 4. Role Assignment
- Assign specific roles to the AI ("You are a...")
- Define responsibilities and limitations
- Establish expertise domains
- Set behavioral expectations

### 5. Iterative Refinement
- Start with basic prompts
- Test systematically
- Refine based on results
- Document improvements

---

## Planning Framework

### Plan Structure Overview

A plan consists of structured steps that can include conditional logic to handle different scenarios. Plans should focus on immediate next steps rather than overall goals.

### Core Components

#### Step Format
```xml
<step>
<action_name>[Name of the tool to be called, e.g., search_helpcenter]</action_name>
<description>[reason] [action_description] [variables_needed]</description>
</step>
```

#### Conditional Logic
```xml
<if_block condition='[specific_condition]'>
    <!-- Steps when condition is true -->
</if_block>
<if_block condition='[alternative_condition]'>
    <!-- Steps when condition is false -->
</if_block>
```

### Variable Reference System

#### Tool Call Results
- Use `<tool_result>` format for outputs from tool calls
- Examples: `<helpcenter_result>`, `<search_result>`, `<api_response>`

#### Policy Information  
- Use `{{policy_variable}}` format for policy-defined information
- Examples: `{{troubleshooting_info_from_policy}}`, `{{escalation_procedures}}`

#### Context Variables
- Use clear, descriptive names for dynamic content
- Examples: `feature_name`, `error_type`, `user_tier`

### Planning Rules

1. **Never Assume Information**: Don't guess at tool results or policy content
2. **Reference Sources**: Always specify where information comes from
3. **Policy Compliance**: Ensure all steps follow established procedures
4. **Explicit Conditions**: Define clear, testable conditions for if_blocks
5. **Progressive Fallback**: Plan from specific to general to information gathering

### Multi-Level Planning Pattern

```xml
<plan>
    <!-- Level 1: Direct solution search -->
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search helpcenter for specific information about [issue_type] and [error_details]</description>
    </step>
    
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Reply to the user with specific solution from <helpcenter_result></description>
        </step>
    </if_block>
    
    <if_block condition='no <helpcenter_result> found'>
        <!-- Level 2: General troubleshooting -->
        <step>
            <action_name>search_helpcenter</action_name>
            <description>Search helpcenter for general [category] troubleshooting information</description>
        </step>
        
        <if_block condition='<helpcenter_result> found'>
            <step>
                <action_name>reply</action_name>
                <description>Reply to the user with general troubleshooting steps from <helpcenter_result></description>
            </step>
        </if_block>
        
        <if_block condition='no <helpcenter_result> found'>
            <!-- Level 3: Information gathering -->
            <step>
                <action_name>reply</action_name>
                <description>Request additional information: ask for {{troubleshooting_details_from_policy}} to better assist with the [issue_type]</description>
            </step>
        </if_block>
    </if_block>
</plan>
```

---

## Advanced Techniques

### 1. Chain-of-Thought (CoT) Prompting
Let the AI show its reasoning process:

```
Think through this step by step:
1. First, identify the key components
2. Then, analyze each component
3. Finally, synthesize your conclusion
```

### 2. XML Tags for Structure
Use XML tags to organize complex prompts:

```xml
<context>
[Background information]
</context>

<instructions>
[Specific tasks]
</instructions>

<examples>
[Relevant examples]
</examples>

<constraints>
[Limitations and rules]
</constraints>
```

### 3. Response Prefilling
Guide the AI's response format:

```
Response format:
Analysis: [Your analysis here]
Recommendation: [Your recommendation]
Confidence: [High/Medium/Low]
```

### 4. Meta-Prompting
Use prompts to improve prompts:

```
You are a prompt engineering expert. Analyze this prompt and suggest improvements:
[Original prompt]

Focus on: clarity, specificity, structure, and potential edge cases.
```

### 5. Self-Consistency
Generate multiple responses and select the most consistent:

```
Provide 3 different approaches to this problem. Then analyze which approach is most reliable and explain why.
```

### 6. Prompt Chaining
Break complex tasks into sequential prompts:

```
Step 1 Prompt: "Analyze the user's request and identify key requirements"
Step 2 Prompt: "Based on the requirements from Step 1, create a detailed plan"
Step 3 Prompt: "Execute the plan from Step 2 and provide the final solution"
```

### 7. Retrieval Augmented Generation (RAG)
Combine external knowledge with prompting:

```
Based on the following retrieved documents:
[Document 1]
[Document 2]

Answer the user's question: [question]
Only use information from the provided documents.
```

---

## Quality Control & Validation

### Manager Prompt Pattern

Use a secondary prompt to validate outputs:

```xml
# Your instructions as manager
- You are a manager of a customer service agent
- Your task is to approve or reject a tool call from an agent and provide feedback
- Return either <manager_verify>accept</manager_verify> or <manager_verify>reject</manager_verify><feedback_comment>{{ feedback_comment }}</feedback_comment>

Process:
1) Analyze the context and tool call
2) Check against policies and checklists  
3) Accept if compliant, reject with specific feedback if not
4) Ensure tool call helps the user and follows policy

<customer_service_policy>
{policy_content}
</customer_service_policy>

<context_customer_service_agent>
{agent_context}
</context_customer_service_agent>

<checklist_for_tool_call>
{verification_checklist}
</checklist_for_tool_call>
```

### Evaluation Framework

1. **Define Success Criteria**
   - Accuracy metrics
   - Relevance scores
   - Safety compliance
   - Task completion rates

2. **Create Test Cases**
   - Edge cases
   - Common scenarios
   - Error conditions
   - Boundary conditions

3. **Systematic Testing**
   - A/B testing of prompt variations
   - Regression testing for changes
   - Performance benchmarking
   - Human evaluation

4. **Continuous Improvement**
   - Monitor real-world performance
   - Collect user feedback
   - Iterate based on results
   - Document lessons learned

---

## Real-World Applications

### Customer Support Agent

**Challenge**: Handle complex customer inquiries with multiple fallback paths

**Solution**: Multi-level planning with policy compliance
- Level 1: Search for specific solutions
- Level 2: General troubleshooting
- Level 3: Information gathering
- Manager validation layer

**Key Features**:
- Variable reference system for tool results
- Policy-driven decision making
- Explicit condition handling
- No assumptions about data availability

### Code Generation Assistant

**Challenge**: Generate reliable, secure code

**Solution**: Structured prompting with validation
```
You are a senior software engineer. Generate code that:

<requirements>
- Follows [language] best practices
- Includes error handling
- Has comprehensive comments
- Is security-conscious
</requirements>

<constraints>
- No deprecated functions
- Maximum 100 lines
- Include unit tests
</constraints>

<format>
```[language]
[code here]
```

Explanation: [brief explanation]
Tests: [test cases]
</format>
```

### Content Analysis Tool

**Challenge**: Analyze content for quality and compliance

**Solution**: Multi-criteria evaluation with scoring
```
Analyze this content across multiple dimensions:

<evaluation_criteria>
1. Clarity (1-10): How clear and understandable is the content?
2. Accuracy (1-10): How factually correct is the information?
3. Completeness (1-10): How thoroughly does it cover the topic?
4. Compliance (Pass/Fail): Does it meet company guidelines?
</evaluation_criteria>

<output_format>
Scores:
- Clarity: [score]/10 - [brief explanation]
- Accuracy: [score]/10 - [brief explanation]  
- Completeness: [score]/10 - [brief explanation]
- Compliance: [Pass/Fail] - [explanation]

Overall Assessment: [summary]
Recommendations: [specific improvements]
</output_format>
```

---

## Best Practices & Anti-Patterns

### Best Practices

#### 1. Clear Structure
```
✅ Good:
# Task: Data Analysis
## Objective: Analyze sales data for Q4 trends
## Requirements:
- Focus on revenue growth
- Identify top-performing products
- Highlight concerning trends
## Output Format:
[Structured format specification]
```

#### 2. Specific Instructions
```
✅ Good:
"Generate a Python function that validates email addresses using regex. Include error handling for invalid inputs and return a boolean value."

❌ Bad:
"Write some code to check emails."
```

#### 3. Proper Variable Usage
```
✅ Good:
"Reply to the user with instructions from <helpcenter_result>"

❌ Bad:
"Reply with the password reset instructions" (assumes content)
```

#### 4. Explicit Conditions
```
✅ Good:
<if_block condition='<search_result> contains solution'>

❌ Bad:
<if_block condition='found something'>
```

### Anti-Patterns to Avoid

#### 1. Ambiguous Instructions
```
❌ Bad: "Make it better"
✅ Good: "Improve readability by adding comments and breaking long functions into smaller ones"
```

#### 2. Assuming Tool Results
```
❌ Bad: "Use the API key from the database lookup"
✅ Good: "Use the API key from <database_result> if available"
```

#### 3. Over-Complex Single Prompts
```
❌ Bad: One massive prompt trying to do everything
✅ Good: Chain of focused prompts with clear handoffs
```

#### 4. Insufficient Examples
```
❌ Bad: No examples or only one example
✅ Good: Multiple diverse examples showing edge cases
```

#### 5. Ignoring Context Windows
```
❌ Bad: Extremely long prompts that exceed model limits
✅ Good: Structured prompts with key information prioritized
```

### Quality Checklist

Before deploying a prompt:
- [ ] Instructions are clear and specific
- [ ] Examples cover common and edge cases
- [ ] Variable references are properly formatted
- [ ] Conditions are explicitly defined
- [ ] Error handling is included
- [ ] Output format is specified
- [ ] Success criteria are measurable
- [ ] Edge cases are considered

---

## Templates & Examples

### Basic Task Template

```
# Role
You are a [specific role with expertise].

# Task
[Clear, specific task description]

# Context
[Relevant background information]

# Requirements
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

# Constraints
- [Limitation 1]
- [Limitation 2]

# Output Format
[Exact format specification]

# Examples
[2-3 diverse examples]
```

### Conditional Planning Template

```xml
<plan>
    <step>
        <action_name>[primary_tool]</action_name>
        <description>[reason] [action] [variables_needed]</description>
    </step>
    
    <if_block condition='[success_condition]'>
        <step>
            <action_name>[success_tool]</action_name>
            <description>[success_action] using <tool_result></description>
        </step>
    </if_block>
    
    <if_block condition='[failure_condition]'>
        <step>
            <action_name>[fallback_tool]</action_name>
            <description>[fallback_action] requesting {{policy_info}}</description>
        </step>
    </if_block>
</plan>
```

## Analysis Template

```
# Analysis Framework

## Input
[Data/content to analyze]

## Analysis Dimensions
1. **[Dimension 1]**: [Specific criteria]
2. **[Dimension 2]**: [Specific criteria]
3. **[Dimension 3]**: [Specific criteria]

## Methodology
[Step-by-step analysis approach]

## Output Structure
### Summary
[High-level findings]

### Detailed Analysis
[Dimension-by-dimension breakdown]

### Recommendations
[Actionable insights]

### Confidence Level
[High/Medium/Low with justification]
```

### Customer Support Template

```xml
<plan>
    <!-- Initial Assessment -->
    <step>
        <action_name>analyze_request</action_name>
        <description>Analyze user request to identify issue_type and available context</description>
    </step>
    
    <!-- Primary Resolution Path -->
    <step>
        <action_name>search_knowledge_base</action_name>
        <description>Search knowledge base for specific solution to issue_type</description>
    </step>
    
    <if_block condition='<search_result> found AND <search_result> confidence high'>
        <step>
            <action_name>provide_solution</action_name>
            <description>Provide solution from <search_result> with clear steps</description>
        </step>
    </if_block>
    
    <!-- Secondary Resolution Path -->
    <if_block condition='<search_result> found AND <search_result> confidence low'>
        <step>
            <action_name>request_clarification</action_name>
            <description>Ask for {{additional_info_from_policy}} to refine solution</description>
        </step>
    </if_block>
    
    <!-- Escalation Path -->
    <if_block condition='no <search_result> found'>
        <step>
            <action_name>escalate</action_name>
            <description>Escalate to {{specialist_team_from_policy}} following escalation procedures</description>
        </step>
    </if_block>
</plan>
```

---

This comprehensive guide synthesizes best practices from leading AI companies and research institutions. It provides both theoretical understanding and practical templates for implementing effective prompt engineering strategies across various domains.

For implementation, start with the basic templates and gradually incorporate advanced techniques based on your specific use case and performance requirements. Remember that prompt engineering is an iterative process requiring systematic testing and refinement.
