# 🎛️ LLM Parameter Tuning Guide

> **Essential guide for optimizing temperature, top-P, top-K, and other parameters for maximum AI performance**

## 🎯 Quick Reference

### **Google Recommended Starting Point**
- **Temperature**: 0.2
- **Top-P**: 0.95  
- **Top-K**: 30
- *"Relatively coherent results that can be creative but not excessively so"*

### **Task-Specific Optimization**

| Task Type | Temperature | Top-P | Top-K | Use Case |
|-----------|-------------|-------|-------|----------|
| **Factual/Research** | 0.1-0.2 | 0.9 | 10-20 | Data analysis, fact checking |
| **Code Generation** | 0.1 | 0.9 | 10 | Programming, technical tasks |
| **Balanced/Default** | 0.2 | 0.95 | 30 | General purpose interactions |
| **Content Creation** | 0.4-0.7 | 0.95 | 40 | Writing, documentation |
| **Creative Writing** | 0.8-0.9 | 0.99 | 40-50 | Brainstorming, ideation |

## 🔬 Parameter Deep Dive

### 🌡️ Temperature (Randomness Control)

**How it works**: Controls randomness in token selection using softmax-like behavior
- **Low temperature** (0-0.3): Emphasizes highest probability tokens → more deterministic
- **High temperature** (0.8-1.0): Flattens probability distribution → more diverse outputs

**Practical Guidelines**:
```
0.1: Maximum determinism - factual responses, precise code
0.2: Slight creativity with high accuracy - research, analysis  
0.4-0.7: Balanced creativity and coherence - general writing
0.9: High creativity - brainstorming, experimental content
1.0: Maximum randomness - extreme creativity (often incoherent)
```

### 🎯 Top-P (Nucleus Sampling)

**How it works**: Dynamically selects from tokens whose cumulative probability exceeds threshold

**Practical Guidelines**:
- **0.5**: Very focused, predictable outputs
- **0.9**: Good balance for factual tasks
- **0.95**: Recommended default for most tasks
- **0.99**: Maximum vocabulary breadth for creativity

**Key Insight**: Top-P adapts to context - fewer options for predictable text, more for creative contexts

### 🔢 Top-K (Vocabulary Limiting)

**How it works**: Limits token selection to K highest-probability options

**Practical Guidelines**:
- **10**: Very focused, conservative outputs
- **20**: Good for factual, technical tasks
- **30**: Recommended default balance
- **40-50**: More variety for creative tasks

**Mental Model**: Think of top-K as "vocabulary breadth" - higher K = more word choices

## ⚙️ Parameter Interactions

### **Critical Understanding**: Parameters Work Together
1. **Top-K and Top-P filter first**: Only tokens meeting BOTH criteria advance
2. **Temperature applies last**: Sampling from filtered candidates
3. **Extreme settings override others**:
   - Top-K = 1 → Temperature and Top-P irrelevant
   - Top-P = 0 → Only most probable token considered
   - Top-P = 1 → No filtering effect

### **Optimization Strategy**
```
1. Start with task-appropriate base settings
2. Adjust temperature first (biggest impact)
3. Fine-tune Top-P for vocabulary breadth
4. Adjust Top-K for output variety
5. Test and iterate based on results
```

## 🎯 Use Case Optimization

### **📊 Factual Research & Analysis**
```yaml
Settings:
  temperature: 0.1-0.2
  top_p: 0.9
  top_k: 10-20
  max_tokens: Variable based on need

Why: Prioritizes accuracy over creativity
Best for: Data analysis, fact-checking, technical documentation
```

### **💻 Code Generation**
```yaml
Settings:
  temperature: 0.1
  top_p: 0.9
  top_k: 10
  max_tokens: Conservative (avoid hallucination)

Why: Code requires precision, not creativity
Best for: Programming tasks, technical implementation
```

### **✍️ Content Creation**
```yaml
Settings:
  temperature: 0.4-0.7
  top_p: 0.95
  top_k: 40
  max_tokens: Based on content length needs

Why: Balances creativity with coherence
Best for: Articles, documentation, structured writing
```

### **🎨 Creative & Brainstorming**
```yaml
Settings:
  temperature: 0.8-0.9
  top_p: 0.99
  top_k: 50
  max_tokens: Higher for exploration

Why: Maximizes creative potential while maintaining coherence
Best for: Ideation, creative writing, exploration
```

## 🚀 Advanced Optimization

### **Model-Specific Tuning**
- **GPT models**: Generally follow standard recommendations
- **Claude**: Often performs well with slightly lower temperature
- **Gemini**: Temperature behaves like softmax function - fine-tune carefully
- **Open source models**: May require more aggressive parameter tuning

### **Cost Optimization**
```yaml
Efficiency_Strategy:
  routine_tasks: "Lower max_tokens, conservative settings"
  exploration: "Higher creativity settings, accept higher token usage"
  production: "Optimize for consistency and cost"
  experimentation: "Use free/cheaper models for parameter testing"
```

### **Performance Benchmarking**
Track these metrics when optimizing:
- **Accuracy**: Task completion success rate
- **Consistency**: Output variation for identical inputs
- **Relevance**: On-topic response percentage  
- **Cost**: Quality per token spent
- **Speed**: Response time considerations

## 🔧 Practical Implementation

### **A/B Testing Framework**
```python
# Example parameter testing approach
test_configurations = [
    {"temperature": 0.2, "top_p": 0.95, "top_k": 30},  # Baseline
    {"temperature": 0.1, "top_p": 0.9, "top_k": 20},   # Conservative
    {"temperature": 0.7, "top_p": 0.95, "top_k": 40},  # Creative
]

# Test each configuration on sample tasks
# Measure quality, consistency, cost
# Select optimal settings for your use case
```

### **Iterative Optimization Process**
1. **Baseline**: Start with recommended defaults
2. **Task Analysis**: Identify primary needs (accuracy vs creativity)
3. **Single Parameter**: Adjust temperature first
4. **Fine-tune**: Optimize top-P and top-K
5. **Validate**: Test on representative tasks
6. **Document**: Record optimal settings for each task type

## 📋 Troubleshooting Common Issues

### **Too Repetitive/Boring**
- ⬆️ Increase temperature (0.1 → 0.3)
- ⬆️ Increase top-K (20 → 40)
- ⬆️ Increase top-P (0.9 → 0.95)

### **Too Random/Incoherent**
- ⬇️ Decrease temperature (0.8 → 0.5)
- ⬇️ Decrease top-K (50 → 30)
- ⬇️ Decrease top-P (0.99 → 0.95)

### **Inconsistent Results**
- ⬇️ Lower temperature for more determinism
- Consider fixing random seed if available
- Use multiple generations with voting

### **High Costs**
- ⬇️ Reduce max_tokens
- Use cheaper models for experimentation
- Batch similar requests
- Optimize prompt length

## 🔗 Related Resources

- **[Google AI Technical Whitepaper](./google-ai-tech-whitepaper-prompt-engineering.md)**: Detailed technical foundation
- **[Human vs AI Agent Parameters](./google-prompt-engineering-agents-vs-humans.md)**: Specialized parameter guidance
- **[Performance Testing Framework](../../advanced-frameworks/multi-agent-orchestration-guide.md)**: Model evaluation methods

---

*Parameter tuning is both art and science. Start with proven defaults, then systematically optimize for your specific needs. Document what works best for your common tasks.*
