# Customer Support AI Agent Architecture

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Planning System](#planning-system)
3. [Manager Validation Layer](#manager-validation-layer)
4. [Policy Integration](#policy-integration)
5. [Tool Call Management](#tool-call-management)
6. [Memory & Context Systems](#memory--context-systems)
7. [Evaluation & Optimization](#evaluation--optimization)
8. [Implementation Patterns](#implementation-patterns)

---

## Architecture Overview

Based on Parahelp's production system serving companies like Perplexity, Framer, Replit, and ElevenLabs, this architecture achieves high success rates in automated customer support through a combination of structured planning, policy compliance, and quality validation.

### Core Architecture Principles

1. **Token-First Architecture**: Optimized for token efficiency over workflow complexity
2. **Policy-Driven Decisions**: All actions must align with company policies
3. **Progressive Fallback**: Multiple levels of resolution strategies
4. **Variable-Based Planning**: Plans reference tool results without assuming content
5. **Manager Validation**: Secondary layer ensures quality and compliance

### Success Metrics
- **Primary**: % of tickets resolved end-to-end
- **Secondary**: Response accuracy, policy compliance, user satisfaction
- **Technical**: Token efficiency, response time, error rates

### Key Components

```
User Request
     ↓
Planning Agent ────→ Policy Database
     ↓                     ↓
Tool Execution ←──── Manager Validator
     ↓                     ↓
Response ─────────→ Quality Check
     ↓
User Reply
```

---

## Planning System

The Planning System section has been moved to a dedicated document for improved clarity and modularity.

➡️ [See detailed Planning System architecture and prompt patterns in `planning-system.md`](./planning-system.md)

### Variable Reference System

#### Tool Call Results
Use `<>` notation for tool call outputs:
- `<helpcenter_result>`: Results from help center search
- `<subscription_result>`: Results from subscription lookup
- `<user_data_result>`: Results from user data retrieval

#### Policy Variables
Use `{{}}` notation for policy-defined information:
- `{{troubleshooting_info_name_from_policy_1}}`: First level troubleshooting requirements
- `{{troubleshooting_info_name_from_policy_2}}`: Second level troubleshooting requirements
- `{{escalation_procedures}}`: Policy-defined escalation rules

### Planning Challenges & Solutions

#### Challenge 1: Information Completeness
**Problem**: Model has access to some relevant information but rarely all of it
**Solution**: 
- Never assume information availability
- Always reference specific tool results
- Use conditional planning for different information scenarios

#### Challenge 2: Path Complexity ("Model RAM")
**Problem**: Plans must consider all potential paths based on tool call returns
**Solution**:
- Use XML if blocks with explicit conditions
- Leverage model's coding-logic capabilities
- Avoid "else" blocks to force explicit condition definition

### Example Planning Pattern

```xml
<plan>
    <!--
        Documentation Comment

        Priority: ![medium](https://img.shields.io/badge/priority-medium-yellow)

        Clarification Request:
        The document currently references several variables related to tool call results, including `<helpcenter_result>`, `<search_helpcenter_result>`, and `<search_result>`. However, their relationship and intended usage are not explicitly defined, which may cause confusion for readers and implementers.

        1. Relationship Clarification:
            - Please clarify whether `<helpcenter_result>`, `<search_helpcenter_result>`, and `<search_result>` are:
                a) Distinct variables representing different types of tool call results (e.g., specific to helpcenter, general search, or a generic result container), or
                b) Interchangeable terms referring to the same result object, with naming variations used for illustrative or contextual purposes.

        2. Documentation Consistency:
            - If `<search_helpcenter_result>` and `<search_result>` are standard variables within this architecture (not just illustrative), consider explicitly defining them in the "Tool Call Results" section (lines 87-90), alongside `<helpcenter_result>`.
            - Providing clear definitions and intended use cases for each variable will improve clarity and consistency across this document and related files (e.g., `examples-and-templates.md`).

        Recommendation:
        - Add a subsection to the "Tool Call Results" section that lists and defines all standard result variables used throughout the documentation suite.
        - Include a note on whether these variables are interchangeable or have distinct roles, and update references in all relevant sections for consistency.

        This clarification will help ensure that readers understand the correct usage and scope of each result variable, reducing ambiguity and improving maintainability.
    -->
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

---

## Manager Validation Layer

### Purpose
The manager acts as a quality control layer, validating tool calls against policies and best practices before execution. This pattern significantly improves response quality and policy compliance.

### Manager Prompt Architecture

```markdown
# Your instructions as manager
- You are a manager of a customer service agent.
- You have a very important job, which is making sure that the customer service agent working for you does their job REALLY well.
- Your task is to approve or reject a tool call from an agent and provide feedback if you reject it. The feedback can be both on the tool call specifically, but also on the general process so far and how this should be changed.
- You will return either <manager_verify>accept</manager_verify> or <manager_verify>reject</manager_verify><feedback_comment>{{ feedback_comment }}</feedback_comment>

Process:
1) Analyze all <context_customer_service_agent> and <latest_internal_messages> to understand the context of the ticket and you own internal thinking/results from tool calls.
2) Then, check the tool call against the <customer_service_policy> and the checklist in <checklist_for_tool_call>.
3) If the tool call passes the <checklist_for_tool_call> and Customer Service policy in <context_customer_service_agent>, return <manager_verify>accept</manager_verify>
4) In case the tool call does not pass the <checklist_for_tool_call> or Customer Service policy in <context_customer_service_agent>, then return <manager_verify>reject</manager_verify><feedback_comment>{{ feedback_comment }}</feedback_comment>
5) You should ALWAYS make sure that the tool call helps the user with their request and follows the <customer_service_policy>.

Important notes:
1) You should always make sure that the tool call does not contain incorrect information, and that it is coherent with the <customer_service_policy> and the context given to the agent listed in <context_customer_service_agent>.
2) You should always make sure that the tool call is following the rules in <customer_service_policy> and the checklist in <checklist_for_tool_call>.

How to structure your feedback:
1) If the tool call passes the <checklist_for_tool_call> and Customer Service policy in <context_customer_service_agent>, return <manager_verify>accept</manager_verify>
2) If the tool call does not pass the <checklist_for_tool_call> or Customer Service policy in <context_customer_service_agent>, then return <manager_verify>reject</manager_verify><feedback_comment>{{ feedback_comment }}</feedback_comment>
3) If you provide a feedback comment, know that you can both provide feedback on the specific tool call if this is specifically wrong, but also provide feedback if the tool call is wrong because of the general process so far is wrong e.g. you have not called the {{tool_name}} tool yet to get the information you need according to the <customer_service_policy>. If this is the case you should also include this in your feedback.

<customer_service_policy>
{wiki_system_prompt}
</customer_service_policy>

<context_customer_service_agent>
{agent_system_prompt}
{initial_user_prompt}
</context_customer_service_agent>

<available_tools>
{json.dumps(tools, indent=2)}
</available_tools>

<latest_internal_messages>
{format_messages_with_actions(messages)}
</latest_internal_messages>

<checklist_for_tool_call>
{verify_tool_check_prompt}
</checklist_for_tool_call>

# Your manager response:
- Return your feedback by either returning <manager_verify>accept</manager_verify> or <manager_verify>reject</manager_verify><feedback_comment>{{ feedback_comment }}</feedback_comment>
```

### Manager Validation Process

1. **Context Analysis**: Review ticket history and internal messages
2. **Policy Check**: Verify alignment with customer service policies
3. **Checklist Validation**: Ensure tool call meets all requirements
4. **Decision**: Accept or reject with specific feedback
5. **Feedback Loop**: Provide actionable guidance for improvement

### Key Manager Features

- **Role-Based Authority**: Clear hierarchy with manager oversight
- **Structured Feedback**: XML tags for parseable responses
- **Policy Integration**: Direct reference to service policies
- **Process Awareness**: Considers entire conversation context
- **Quality Assurance**: Prevents incorrect or non-compliant responses

---

## Policy Integration

### Policy-Driven Architecture

All decisions and actions must align with company-specific policies. The system maintains a dynamic policy database that influences both planning and validation.

### Policy Structure

```markdown
# Customer Service Agent Policy

## Troubleshooting Requirements
- Level 1: {{basic_troubleshooting_info}}
- Level 2: {{advanced_troubleshooting_info}}
- Level 3: {{escalation_requirements}}

## Information Gathering Rules
- Required fields: {{required_user_data}}
- Optional fields: {{optional_user_data}}
- Privacy considerations: {{data_handling_policy}}

## Response Guidelines
- Tone: {{company_tone_guidelines}}
- Language: {{approved_language_patterns}}
- Restrictions: {{forbidden_responses}}

## Escalation Procedures
- Criteria: {{escalation_criteria}}
- Teams: {{specialist_teams}}
- Process: {{escalation_workflow}}

## Tool Usage Rules
- Approved tools: {{approved_tools_list}}
- Usage restrictions: {{tool_limitations}}
- Data handling: {{tool_data_policy}}
```

### Policy Reference Patterns

#### In Planning
```xml
<step>
    <action_name>request_information</action_name>
    <description>Ask user for {{required_troubleshooting_info_from_policy}} to proceed with diagnosis</description>
</step>
```

#### In Validation
```xml
<if_block condition='user_data_complete'>
    <step>
        <action_name>proceed_with_solution</action_name>
        <description>Proceed using {{solution_approach_from_policy}}</description>
    </step>
</if_block>
```

### Dynamic Policy Updates

- **Version Control**: Track policy changes over time
- **Immediate Effect**: Updates apply to all new conversations
- **Backward Compatibility**: Handle in-flight conversations gracefully
- **Audit Trail**: Log all policy-driven decisions

---

## Tool Call Management

### Tool Call Architecture

Tools are the primary interface between the AI agent and external systems. Each tool call must be validated and properly integrated into the conversation flow.

### Available Tool Categories

#### Information Retrieval
- `search_helpcenter`: Search company knowledge base
- `search_subscription`: Look up user subscription details
- `get_user_data`: Retrieve user account information
- `check_system_status`: Verify system health

#### Communication
- `reply`: Send response to user
- `escalate`: Transfer to human agent
- `schedule_followup`: Set automated follow-up
- `send_notification`: Send system notification

#### Data Management
- `update_ticket`: Modify ticket information
- `log_interaction`: Record conversation details
- `create_case`: Generate support case
- `link_resources`: Attach relevant documentation

### Tool Call Validation Rules

#### Pre-Execution Validation
1. **Tool Exists**: Verify tool is available and properly configured
2. **Parameters Complete**: Ensure all required parameters are provided
3. **Policy Compliance**: Check tool usage against company policies
4. **Context Appropriate**: Verify tool call fits conversation context
5. **Security Check**: Validate data access permissions

#### Post-Execution Validation
1. **Result Verification**: Confirm tool executed successfully
2. **Data Quality**: Validate returned data meets expectations
3. **Error Handling**: Process and respond to tool failures appropriately
4. **Result Integration**: Properly incorporate results into response

### Tool Result Handling

```xml
<step>
    <action_name>search_helpcenter</action_name>
    <description>Search for solution to billing_error</description>
</step>

<if_block condition='<search_result> status success AND <search_result> confidence high'>
    <step>
        <action_name>reply</action_name>
        <description>Provide solution from <search_result> with step-by-step instructions</description>
    </step>
</if_block>

<if_block condition='<search_result> status success AND <search_result> confidence low'>
    <step>
        <action_name>search_helpcenter</action_name>
        <description>Search for general billing troubleshooting information</description>
    </step>
</if_block>

<if_block condition='<search_result> status error'>
    <step>
        <action_name>escalate</action_name>
        <description>Escalate to technical team due to search system unavailability</description>
    </step>
</if_block>
```

---

## Memory & Context Systems

### Context Management Architecture

The system maintains comprehensive context across conversations, including:
- **Conversation History**: Complete message thread
- **Tool Call Results**: Cached results for reference
- **User Profile**: Persistent user information
- **System State**: Current system status and capabilities

### Memory System Integration

#### Dynamic Information Sources
- **Message History**: ~1.5K tokens of recent conversation
- **Memory Learnings**: Relevant insights from previous interactions
- **Company Policies**: Current policy state
- **System Status**: Real-time system health information

#### Context Optimization
```markdown
# Context Priority (High to Low)
1. Current user message and immediate context
2. Recent conversation history (last 10 messages)
3. Relevant policy sections for current issue
4. Previous resolution attempts
5. User profile and preferences
6. System status and limitations
```

### Memory Patterns

#### Learning from Interactions
```xml
<memory_update>
    <user_id>{{user_identifier}}</user_id>
    <interaction_type>billing_inquiry</interaction_type>
    <resolution_method>helpcenter_article_link</resolution_method>
    <effectiveness>high</effectiveness>
    <notes>User prefers detailed step-by-step instructions over summary</notes>
</memory_update>
```

#### Context Retrieval
```xml
<context_query>
    <type>similar_issues</type>
    <parameters>
        <issue_category>billing</issue_category>
        <user_tier>premium</user_tier>
        <time_range>30_days</time_range>
    </parameters>
</context_query>
```

---

## Evaluation & Optimization

### Evaluation Framework

#### Primary Metrics
- **Resolution Rate**: % of tickets resolved without human intervention
- **Accuracy**: Correctness of provided solutions
- **Policy Compliance**: Adherence to company guidelines
- **User Satisfaction**: Feedback scores and ratings

#### Secondary Metrics
- **Response Time**: Speed of initial and follow-up responses
- **Token Efficiency**: Cost optimization through smart prompting
- **Escalation Rate**: Frequency of human handoffs
- **Error Rate**: Technical and content errors

### Optimization Process

#### 1. Continuous Monitoring
```python
# Evaluation metrics tracking
metrics = {
    'resolution_rate': calculate_resolution_rate(tickets),
    'policy_compliance': check_policy_adherence(responses),
    'user_satisfaction': get_satisfaction_scores(feedback),
    'token_efficiency': measure_token_usage(conversations)
}
```

#### 2. A/B Testing Framework
- **Prompt Variations**: Test different prompt structures
- **Tool Sequences**: Experiment with different action orders
- **Response Styles**: Vary communication approaches
- **Validation Rules**: Test different quality thresholds

#### 3. Model Performance Analysis
```markdown
# Model Evaluation Results
## Current Model: o3-med
- Resolution Rate: 87%
- Policy Compliance: 94%
- Average Tokens: 1,247 per conversation

## Previous Model: o1-med
- Resolution Rate: 78%
- Policy Compliance: 89%
- Average Tokens: 1,456 per conversation

## Key Improvements
- Better handling of complex multi-path scenarios
- Improved policy adherence
- More efficient token usage
```

#### 4. Iterative Refinement
1. **Identify Issues**: Monitor performance metrics
2. **Analyze Patterns**: Find common failure modes
3. **Design Solutions**: Create targeted improvements
4. **Test Changes**: Validate improvements through testing
5. **Deploy Updates**: Roll out successful modifications
6. **Monitor Impact**: Verify improvement effectiveness

---

## Implementation Patterns

### Production Deployment Architecture

#### System Components
```yaml
# Production Architecture
components:
  planning_agent:
    model: "o3-med"
    max_tokens: 4000
    temperature: 0.1
    
  manager_validator:
    model: "o3-med"
    max_tokens: 2000
    temperature: 0.0
    
  policy_database:
    type: "vector_db"
    update_frequency: "real_time"
    
  memory_system:
    type: "graph_db"
    retention: "90_days"
    
  tool_orchestrator:
    timeout: "30s"
    retry_attempts: 3
    circuit_breaker: true
```

#### Scaling Considerations
- **Load Balancing**: Distribute conversations across instances
- **Caching**: Cache frequent tool results and policy lookups
- **Rate Limiting**: Protect against abuse and cost overruns
- **Error Recovery**: Graceful degradation when components fail

### Development Workflow

#### 1. Prompt Development
```python
# Prompt development cycle
def develop_prompt():
    # Start with basic prompt
    prompt = create_base_prompt(role, task, constraints)
    
    # Add examples and structure
    prompt = add_examples(prompt, test_cases)
    prompt = add_xml_structure(prompt)
    
    # Test and iterate
    results = test_prompt(prompt, validation_set)
    prompt = refine_prompt(prompt, results)
    
    return prompt
```

#### 2. Quality Assurance
```python
# QA process
def quality_assurance(prompt):
    # Run automated tests
    test_results = run_test_suite(prompt)
    
    # Human evaluation
    human_scores = human_evaluation(prompt, sample_conversations)
    
    # Policy compliance check
    compliance_check = validate_policy_adherence(prompt)
    
    return aggregate_results(test_results, human_scores, compliance_check)
```

#### 3. Deployment Pipeline
```yaml
# CI/CD Pipeline
stages:
  - validate_syntax
  - run_unit_tests
  - performance_testing
  - security_scanning
  - staging_deployment
  - human_review
  - production_deployment
  - monitoring_setup
```

### Best Practices for Implementation

#### Code Organization
```
project/
├── prompts/
│   ├── planning_agent.md
│   ├── manager_validator.md
│   └── specialized_prompts/
├── policies/
│   ├── current/
│   └── versions/
├── tools/
│   ├── information_retrieval/
│   ├── communication/
│   └── data_management/
├── tests/
│   ├── unit_tests/
│   ├── integration_tests/
│   └── evaluation_suites/
└── config/
    ├── production.yaml
    └── development.yaml
```

#### Version Control
- **Prompt Versioning**: Track all prompt changes
- **Policy Versioning**: Maintain policy history
- **Model Versioning**: Document model updates
- **Performance Tracking**: Log performance across versions

#### Monitoring & Alerting
```python
# Monitoring setup
monitors = {
    'resolution_rate': {
        'threshold': 0.85,
        'window': '1h',
        'alert': 'slack_channel'
    },
    'policy_compliance': {
        'threshold': 0.90,
        'window': '30m',
        'alert': 'email_team'
    },
    'response_time': {
        'threshold': '10s',
        'window': '5m',
        'alert': 'pagerduty'
    }
}
```

This architecture provides a robust foundation for building production-grade AI customer support agents that maintain high quality, policy compliance, and user satisfaction while operating at scale.
