# Planning Framework

## Overview
A plan consists of steps that can include conditional logic to handle different scenarios. Plans should always follow established procedures and policies.

## Core Principles

### Plan Structure
- A plan consists of individual steps
- Each step represents a specific action (tool call)
- Steps can include conditional logic using `<if_block>` tags
- Plans should focus on immediate next steps, not overall goals

### Policy Adherence
- Plans must always follow procedures and rules from policy documents
- Never assume information not explicitly stated in policy
- Always reference authoritative sources when available

## Step Creation Guidelines

### Step Format
Each step should follow this structure:

```xml
<step>
<action_name></action_name>
<description>{reason for taking the action, description of the action to take, which outputs from other tool calls that should be used (if relevant)}</description>
</step>
```

### Step Requirements
- **action_name**: Must be the name of a valid tool
- **description**: Should include:
  - Reason for taking the action
  - Description of the action to take
  - Any variables from other tool calls needed
  - Reference to authoritative sources when applicable

### Important Rules
- Never assume information or variables
- Never guess on information/instructions not explicitly stated in policy
- Always highlight that authoritative sources (like `<helpcenter_result>`) are the source of truth
- Descriptions should reference tool call results using variable notation (e.g., `<helpcenter_result>`)

## Conditional Logic

### If Blocks
- Use `<if_block condition=''>` tags to include different steps based on conditions
- If blocks can be used anywhere in a step or plan
- Always include a condition attribute
- Create multiple if blocks for if/else scenarios

### Example Structure
```xml
<if_block condition='<helpcenter_result> found'>
    <!-- Steps when condition is true -->
</if_block>
<if_block condition='no <helpcenter_result> found'>
    <!-- Steps when condition is false -->
</if_block>
```

## Planning Best Practices

1. **Focus on Next Steps**: Plan only immediate next steps, not the entire workflow
2. **Reference Policy**: Always ensure steps follow established procedures
3. **Use Tool Results**: Reference outputs from other tool calls using variable notation
4. **Include Fallbacks**: Plan for scenarios where primary actions fail
5. **Specify Sources**: Always indicate when information should come from authoritative sources
# Step Creation Guidelines

## Step Structure

### Required Components
Every step must include:
- `<action_name>`: The tool to be called
- `<description>`: Detailed explanation of the action

### Description Content
The description should always include:
1. **Reason**: Why this action is needed
2. **Action**: What action to take
3. **Variables**: Which outputs from other tool calls to use (if relevant)
4. **Goal**: The specific objective of this action

## Formatting Rules

### Action Name
- Must be the name of a valid tool
- Should match exactly with available tool names
- Case-sensitive

### Description Guidelines
- Keep descriptions concise but complete
- Use variable notation for tool results: `<tool_result>`
- Reference policy variables with: `{{policy_variable}}`
- Never assume information not explicitly available
- Always specify source of truth for information

## Variable References

### Tool Call Results
```xml
<description>Reply to the user with instructions from <helpcenter_result></description>
```

### Policy Information
```xml
<description>Ask for {{troubleshooting_info_name_from_policy}} as specified in the policy</description>
```

### Context Variables
```xml
<description>Search helpcenter for information about feature_name and how to resolve error_name</description>
```

## Common Patterns

### Search and Reply Pattern
```xml
<step>
    <action_name>search_helpcenter</action_name>
    <description>Search helpcenter for information about [specific topic]</description>
</step>
<step>
    <action_name>reply</action_name>
    <description>Reply to the user with instructions from <helpcenter_result></description>
</step>
```

### Information Gathering Pattern
```xml
<step>
    <action_name>reply</action_name>
    <description>Ask the user for {{required_info_from_policy}} to better assist with troubleshooting</description>
</step>
```

### Conditional Response Pattern
```xml
<step>
    <action_name>reply</action_name>
    <description>Based on <previous_result>, provide appropriate response using information from policy document</description>
</step>
```

## Best Practices

1. **Be Specific**: Clearly state what information or variables the action needs
2. **Reference Sources**: Always indicate where information should come from
3. **Avoid Assumptions**: Never guess at information not explicitly available
4. **Use Variables**: Reference tool results and policy information properly
5. **State Purpose**: Make the goal of each action clear
6. **Follow Policy**: Ensure all actions align with established procedures
# Conditional Logic Guidelines

## If Block Structure

### Basic Syntax
```xml
<if_block condition='[condition]'>
    <!-- Steps to execute when condition is true -->
</if_block>
```

### Key Requirements
- Every if block MUST have a condition attribute
- Conditions should be clearly defined and testable
- If blocks can be nested within other if blocks
- If blocks can be used anywhere in a step or plan

## Common Condition Patterns

### Tool Result Conditions
```xml
<if_block condition='<helpcenter_result> found'>
    <!-- Execute when search returns results -->
</if_block>

<if_block condition='no <helpcenter_result> found'>
    <!-- Execute when search returns no results -->
</if_block>
```

### State-Based Conditions
```xml
<if_block condition='user_authenticated'>
    <!-- Steps for authenticated users -->
</if_block>

<if_block condition='error_type == critical'>
    <!-- Steps for critical errors -->
</if_block>
```

### Multiple Conditions
```xml
<if_block condition='<helpcenter_result> found AND user_tier == premium'>
    <!-- Steps for premium users with search results -->
</if_block>
```

## If/Else Pattern

To create if/else logic, use multiple if blocks:

```xml
<if_block condition='<helpcenter_result> found'>
    <step>
        <action_name>reply</action_name>
        <description>Provide solution from <helpcenter_result></description>
    </step>
</if_block>
<if_block condition='no <helpcenter_result> found'>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search for general troubleshooting information</description>
    </step>
</if_block>
```

## Nested Conditions

```xml
<if_block condition='error_reported'>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search for specific error information</description>
    </step>
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Provide specific solution from <helpcenter_result></description>
        </step>
    </if_block>
    <if_block condition='no <helpcenter_result> found'>
        <step>
            <action_name>escalate</action_name>
            <description>Escalate to specialist team due to unknown error</description>
        </step>
    </if_block>
</if_block>
```

## Best Practices

### Condition Design
1. **Be Explicit**: Make conditions clear and unambiguous
2. **Use Variables**: Reference tool results and state properly
3. **Plan Fallbacks**: Always have a path for when conditions aren't met
4. **Avoid Deep Nesting**: Keep nesting levels manageable for readability

### Variable References in Conditions
- Use `<tool_result>` format for tool call outputs
- Reference specific states or values clearly
- Consider both positive and negative conditions

### Common Condition Types
- **Tool Results**: `<helpcenter_result> found`, `<search_result> empty`
- **User State**: `user_authenticated`, `user_tier == premium`
- **Error Types**: `error_type == critical`, `error_resolved`
- **Information Availability**: `troubleshooting_info_provided`, `logs_available`

## Planning with Conditions

When planning with conditional logic:
1. **Identify Decision Points**: Where different paths might be needed
2. **Define Clear Conditions**: What determines which path to take
3. **Plan All Paths**: Ensure every condition has appropriate steps
4. **Consider Edge Cases**: What happens if conditions aren't met as expected
# Planning Best Practices

## Core Principles

### 1. Focus on Immediate Next Steps
- Plan only the goal of next steps, not the overall goal
- Avoid planning too far ahead in a single plan
- Keep plans focused and actionable

### 2. Policy Compliance
- Always follow procedures and rules from policy documents
- Never include or guess information not explicitly stated in policy
- Reference policy documents as the source of truth

### 3. Information Integrity
- Never assume information, variables, or tool call results
- Always specify where information should come from
- Use authoritative sources (like `<helpcenter_result>`) as source of truth

## Variable and Reference Guidelines

### Tool Call Results
```xml
<!-- Good: References variable properly -->
<description>Reply to the user with instructions from <helpcenter_result></description>

<!-- Bad: Assumes content -->
<description>Reply to the user with password reset instructions</description>
```

### Policy References
```xml
<!-- Good: References policy variable -->
<description>Ask for {{troubleshooting_info_from_policy}} to proceed with diagnosis</description>

<!-- Bad: Assumes policy content -->
<description>Ask for system logs and error screenshots</description>
```

## Planning Structure

### Logical Flow
1. **Initial Action**: Start with the most direct approach
2. **Success Path**: Define what happens when primary action succeeds
3. **Fallback Paths**: Plan for when primary actions fail
4. **Information Gathering**: Include steps to gather more context when needed

### Example Structure
```xml
<plan>
    <!-- Primary action -->
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search for specific solution</description>
    </step>
    
    <!-- Success path -->
    <if_block condition='<helpcenter_result> found'>
        <step>
            <action_name>reply</action_name>
            <description>Provide solution from <helpcenter_result></description>
        </step>
    </if_block>
    
    <!-- Fallback path -->
    <if_block condition='no <helpcenter_result> found'>
        <!-- Additional steps for fallback -->
    </if_block>
</plan>
```

## Common Anti-Patterns

### Avoid These Mistakes

1. **Assuming Tool Results**
   ```xml
   <!-- Bad -->
   <description>Reply with the password reset link from the search</description>
   
   <!-- Good -->
   <description>Reply with instructions from <helpcenter_result></description>
   ```

2. **Guessing Policy Content**
   ```xml
   <!-- Bad -->
   <description>Ask for user's email and account ID</description>
   
   <!-- Good -->
   <description>Ask for {{required_user_info_from_policy}}</description>
   ```

3. **Planning Too Far Ahead**
   ```xml
   <!-- Bad: Too many assumptions about future steps -->
   <plan>
       <step>Search for solution</step>
       <step>Send solution to user</step>
       <step>Follow up in 24 hours</step>
       <step>Close ticket if resolved</step>
   </plan>
   
   <!-- Good: Focus on immediate next steps -->
   <plan>
       <step>Search for solution</step>
       <if_block condition='solution found'>
           <step>Send solution to user</step>
       </if_block>
   </plan>
   ```

## Quality Checklist

Before finalizing a plan, verify:
- [ ] All action names are valid tools
- [ ] Descriptions reference variables properly
- [ ] No assumptions about tool results
- [ ] Policy compliance is maintained
- [ ] Fallback paths are included
- [ ] Conditions are clearly defined
- [ ] Source of truth is specified for information

## Documentation Standards

### Step Documentation
- Include rationale for each action
- Specify data dependencies clearly
- Reference authoritative sources
- Use consistent variable notation

### Plan Documentation
- Document the overall strategy
- Explain decision points
- Note any policy requirements
- Include fallback scenarios
