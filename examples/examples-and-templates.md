# Customer Service Planning Template

## Scenario: User Error with Feature

**Context**: A user has an error with a feature and has provided basic information about the error

### Complete Plan Structure

```xml
<plan>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search helpcenter for information about feature_name and how to resolve error_name</description>
    </step>
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Reply to the user with instructions from <helpcenter_result></description>
        </step>
    </if_block>
    <if_block condition='no <helpcenter_result> found'>
        <step>
            <action_name>search_helpcenter</action_name>
            <description>Search helpcenter for general information about how to resolve error/troubleshoot</description>
        </step>
        <if_block condition='<helpcenter_result> found'>
            <step>
                <action_name>reply</action_name>
                <description>Reply to the user with relevant instructions from general <search_helpcenter_result> information</description>
            </step>
        </if_block>
        <if_block condition='no <helpcenter_result> found'>
            <step>
                <action_name>reply</action_name>
                <description>If we can't find specific troubleshooting or general troubleshooting, reply to the user that we need more information and ask for a {{troubleshooting_info_name_from_policy_2}} of the error (since we already have {{troubleshooting_info_name_from_policy_1}}, but need {{troubleshooting_info_name_from_policy_2}} for more context to search helpcenter)</description>
            </step>
        </if_block>
    </if_block>
</plan>
```

## Pattern Analysis

### Escalation Path
1. **Primary Search**: Search for specific feature and error information
2. **Specific Solution**: If found, provide direct instructions
3. **Fallback Search**: If not found, search for general troubleshooting
4. **General Solution**: If general info found, provide relevant instructions
5. **Information Gathering**: If no solutions found, request additional troubleshooting information

### Key Elements
- **Tool Variables**: Uses `<helpcenter_result>` and `<search_helpcenter_result>` as variables
- **Policy References**: References `{{troubleshooting_info_name_from_policy_1}}` and `{{troubleshooting_info_name_from_policy_2}}`
- **Conditional Logic**: Nested if blocks for different scenarios
- **Source Attribution**: Always references where information comes from

### Variable Notation
- `<tool_result>`: Results from tool calls
- `{{policy_variable}}`: Information from policy documents
- `feature_name`, `error_name`: Context-specific variables

## Usage Notes

This template demonstrates:
- How to structure multi-level conditional logic
- Progressive fallback strategies
- Proper variable referencing
- Policy compliance in information gathering
# Basic Plan Template

Use this template as a starting point for creating structured plans.

## Simple Plan Structure

```xml
<plan>
    <step>
        <action_name>[tool_name]</action_name>
        <description>[reason] [action_description] [variables_needed]</description>
    </step>
    <if_block condition='[condition]'>
        <step>
            <action_name>[tool_name]</action_name>
            <description>[description_with_variable_reference]</description>
        </step>
    </if_block>
    <if_block condition='[alternative_condition]'>
        <step>
            <action_name>[tool_name]</action_name>
            <description>[fallback_description]</description>
        </step>
    </if_block>
</plan>
```

## Template Variables

Replace these placeholders with actual values:
- `[tool_name]`: Name of the specific tool to call
- `[reason]`: Why this action is needed
- `[action_description]`: What the action should do
- `[variables_needed]`: Any tool results or policy variables required
- `[condition]`: Specific condition to test
- `[description_with_variable_reference]`: Description that references tool results
- `[alternative_condition]`: Alternative condition for else path
- `[fallback_description]`: Description for fallback actions

## Example Usage

```xml
<plan>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search helpcenter for information about login_issues to help resolve user's authentication problem</description>
    </step>
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Reply to the user with login troubleshooting instructions from <helpcenter_result></description>
        </step>
    </if_block>
    <if_block condition='no <helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Ask user for {{additional_login_info_from_policy}} to better diagnose the authentication issue</description>
        </step>
    </if_block>
</plan>
```

## Customization Notes

- Add more steps as needed for complex scenarios
- Nest if_blocks for multi-level conditions
- Include multiple conditions in a single if_block if needed
- Always reference policy variables with `{{variable_name}}`
- Always reference tool results with `<tool_result>`
# Multi-Level Troubleshooting Template

Template for complex troubleshooting scenarios with multiple fallback levels.

## Structure

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

## Template Variables

- `[issue_type]`: Specific type of issue (e.g., "login_error", "payment_failure")
- `[error_details]`: Specific error information provided by user
- `[category]`: Broader category for general troubleshooting (e.g., "authentication", "billing")
- `{{troubleshooting_details_from_policy}}`: Policy-defined information to request

## Usage Examples

### Login Issue Example
```xml
<plan>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search helpcenter for specific information about login_error and authentication_failure</description>
    </step>
    
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Reply to the user with specific solution from <helpcenter_result></description>
        </step>
    </if_block>
    
    <if_block condition='no <helpcenter_result> found'>
        <step>
            <action_name>search_helpcenter</action_name>
            <description>Search helpcenter for general authentication troubleshooting information</description>
        </step>
        
        <if_block condition='<helpcenter_result> found'>
            <step>
                <action_name>reply</action_name>
                <description>Reply to the user with general troubleshooting steps from <helpcenter_result></description>
            </step>
        </if_block>
        
        <if_block condition='no <helpcenter_result> found'>
            <step>
                <action_name>reply</action_name>
                <description>Request additional information: ask for {{login_troubleshooting_info_from_policy}} to better assist with the login_error</description>
            </step>
        </if_block>
    </if_block>
</plan>
```

## Key Features

1. **Progressive Fallback**: Moves from specific to general to information gathering
2. **Consistent Variable Usage**: Uses proper variable notation throughout
3. **Policy Compliance**: References policy for information requirements
4. **Clear Conditions**: Each if_block has explicit conditions
5. **Source Attribution**: Always references where information comes from

## Customization Options

- Add additional levels of fallback
- Include user authentication checks
- Add escalation steps for critical issues
- Include follow-up actions for resolved issues
# Google Prompt Engineering Examples

## Chain-of-Thought Template

```
Solve this problem step-by-step:
{{problem_statement}}

Let me work through this systematically:
Step 1: [First logical step]
Step 2: [Second logical step]
Step 3: [Final reasoning]
Therefore: [Conclusion]
```

## Few-Shot Classification Template

```
Classify the sentiment of these reviews:

Example: "Great product, exceeded expectations!" → Positive
Example: "Poor quality, broke after one use." → Negative
Example: "It's okay, nothing special." → Neutral

Review to classify: {{new_review}}
Sentiment:
```

## Role-Based Code Review Template

```
You are a senior software engineer reviewing code for security vulnerabilities.

Review this {{language}} code:
{{code_block}}

Focus on:
1. Security vulnerabilities
2. Performance issues
3. Best practices compliance

Provide specific recommendations with line references.
```

## Structured Output Template

```
Analyze this data and return JSON:

Data: {{data_input}}

Required format:
{
  "summary": "brief overview",
  "key_insights": ["insight1", "insight2"],
  "confidence": 0.85,
  "recommendations": ["rec1", "rec2"]
}
```

## Tree of Thoughts Template

```
Problem: {{complex_problem}}

Let me explore multiple approaches:

Approach 1: {{strategy_1}}
- Pros: {{pros_1}}
- Cons: {{cons_1}}

Approach 2: {{strategy_2}}
- Pros: {{pros_2}}
- Cons: {{cons_2}}

Best approach: {{chosen_strategy}} because {{reasoning}}
```

---

# Google-Specific Templates

## Human-Focused Templates

### Google's Chain-of-Thought Prompt Template

```
Solve the following problem step-by-step:

Problem: {{problem_description}}

Step 1: Understand what is being asked.
[Think about the problem]

Step 2: Identify the key information.
[List relevant facts and data]

Step 3: Apply appropriate methods.
[Show calculations or reasoning]

Step 4: Verify the solution.
[Check if the answer makes sense]

Step 5: Provide the final answer.
[State the conclusion clearly]
```

### Google's Role-Based Prompt Template

```
You are a {{specific_role}} with expertise in {{domain}}.

Task: {{task_description}}

Consider the following:
- {{key_consideration_1}}
- {{key_consideration_2}}
- {{key_consideration_3}}

Format your response as:
1. Initial assessment
2. Detailed analysis
3. Recommended actions
```

### Google's Product Analysis Template

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

## AI Agent-Focused Templates

### Google's Parameter Configuration Template (for AI Systems)

```json
{
  "task_type": "{{task_category}}",
  "parameters": {
    "temperature": {{temperature_value}},
    "top_p": {{top_p_value}},
    "top_k": {{top_k_value}}
  },
  "model_configuration": {
    "response_length": {{max_tokens}},
    "stop_sequences": ["{{stop_sequence_1}}", "{{stop_sequence_2}}"]
  },
  "structured_output": {
    "format": "{{output_format}}",
    "schema": {{json_schema}}
  },
  "evaluation_metrics": ["{{metric_1}}", "{{metric_2}}"]
}
```

### Google's ReAct Agent Template (for AI Systems)

```json
{
  "task": "{{task_description}}",
  "thinking_framework": "react",
  "steps": [
    {
      "thought": "{{reasoning_about_current_state}}",
      "action": "{{tool_name}}",
      "action_input": "{{tool_parameters}}",
      "observation": "{{tool_output}}"
    }
  ],
  "response_requirements": {
    "include_reasoning_trace": {{boolean}},
    "final_answer_format": "{{format_specification}}"
  }
}
```
