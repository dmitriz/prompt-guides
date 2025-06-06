# API Integration for Prompt Management

## Overview

Comprehensive guide for integrating prompt engineering capabilities into applications through APIs. Includes examples for major LLM providers, prompt management systems, and automated optimization workflows.

## Provider-Specific API Integration

### 1. OpenAI API Integration

**Basic Prompt Execution with Optimization**:

```python
import openai
from typing import Dict, List, Optional
import json
import time

class OpenAIPromptManager:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.prompt_templates = {}
        self.performance_cache = {}
    
    def execute_prompt(self, prompt: str, model: str = "gpt-4", **kwargs) -> Dict:
        """Execute prompt with performance tracking"""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0)
            )
            
            execution_time = time.time() - start_time
            
            result = {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "execution_time": execution_time,
                "model": model,
                "cost": self._calculate_cost(response.usage, model)
            }
            
            # Cache performance data
            self._cache_performance(prompt, result)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "execution_time": time.time() - start_time,
                "model": model
            }
    
    def optimize_parameters(self, prompt: str, test_cases: List[Dict]) -> Dict:
        """Optimize parameters for specific prompt and test cases"""
        parameter_combinations = [
            {"temperature": 0.3, "top_p": 0.8},
            {"temperature": 0.7, "top_p": 0.9},
            {"temperature": 0.9, "top_p": 1.0},
            {"temperature": 0.5, "top_p": 0.85}
        ]
        
        results = []
        
        for params in parameter_combinations:
            scores = []
            total_cost = 0
            
            for test_case in test_cases:
                result = self.execute_prompt(
                    prompt.format(**test_case["input"]),
                    **params
                )
                
                if "error" not in result:
                    score = self._evaluate_response(
                        result["content"], 
                        test_case["expected"]
                    )
                    scores.append(score)
                    total_cost += result["cost"]
            
            if scores:
                results.append({
                    "parameters": params,
                    "average_score": sum(scores) / len(scores),
                    "total_cost": total_cost,
                    "test_cases_passed": len(scores)
                })
        
        # Return best performing parameters
        best_params = max(results, key=lambda x: x["average_score"])
        return best_params
    
    def _calculate_cost(self, usage, model: str) -> float:
        """Calculate API cost based on usage and model"""
        cost_per_1k = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-3.5-turbo": {"prompt": 0.001, "completion": 0.002}
        }
        
        rates = cost_per_1k.get(model, cost_per_1k["gpt-3.5-turbo"])
        
        prompt_cost = (usage.prompt_tokens / 1000) * rates["prompt"]
        completion_cost = (usage.completion_tokens / 1000) * rates["completion"]
        
        return prompt_cost + completion_cost
```

### 2. Anthropic Claude API Integration

```python
import anthropic
from typing import Dict, List

class ClaudePromptManager:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.performance_tracker = {}
    
    def execute_with_system_prompt(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        model: str = "claude-3-sonnet-20240229"
    ) -> Dict:
        """Execute prompt with system message for Claude"""
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return {
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "model": model,
                "stop_reason": response.stop_reason
            }
            
        except Exception as e:
            return {"error": str(e), "model": model}
    
    def batch_execute(self, prompt_requests: List[Dict]) -> List[Dict]:
        """Execute multiple prompts efficiently"""
        results = []
        
        for request in prompt_requests:
            result = self.execute_with_system_prompt(
                request["system_prompt"],
                request["user_prompt"],
                request.get("model", "claude-3-sonnet-20240229")
            )
            
            result["request_id"] = request.get("id", len(results))
            results.append(result)
        
        return results
```

### 3. Google Gemini API Integration

```python
import google.generativeai as genai
from typing import Dict, List

class GeminiPromptManager:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model_configs = {
            "creative": {
                "temperature": 0.9,
                "top_p": 0.95,
                "top_k": 40
            },
            "factual": {
                "temperature": 0.1,
                "top_p": 0.8,
                "top_k": 20
            },
            "balanced": {
                "temperature": 0.5,
                "top_p": 0.9,
                "top_k": 30
            }
        }
    
    def execute_with_config(
        self, 
        prompt: str, 
        config_type: str = "balanced",
        model_name: str = "gemini-pro"
    ) -> Dict:
        """Execute prompt with predefined configuration"""
        
        model = genai.GenerativeModel(model_name)
        config = self.model_configs[config_type]
        
        generation_config = genai.types.GenerationConfig(
            temperature=config["temperature"],
            top_p=config["top_p"],
            top_k=config["top_k"],
            max_output_tokens=1000
        )
        
        try:
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return {
                "content": response.text,
                "config_used": config_type,
                "model": model_name,
                "safety_ratings": [
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name
                    }
                    for rating in response.candidates[0].safety_ratings
                ]
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "config_used": config_type,
                "model": model_name
            }
    
    def multimodal_prompt(self, text_prompt: str, image_path: str) -> Dict:
        """Execute multimodal prompt with image and text"""
        
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Upload image
        image_file = genai.upload_file(path=image_path)
        
        try:
            response = model.generate_content([text_prompt, image_file])
            
            return {
                "content": response.text,
                "image_file": image_path,
                "model": "gemini-pro-vision"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "image_file": image_path,
                "model": "gemini-pro-vision"
            }
```

## Unified Prompt Management API

### 1. Multi-Provider Abstraction Layer

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union

class ProviderType(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"

class PromptProvider(ABC):
    @abstractmethod
    def execute_prompt(self, prompt: str, **kwargs) -> Dict:
        pass
    
    @abstractmethod
    def optimize_parameters(self, prompt: str, test_cases: List[Dict]) -> Dict:
        pass

class UnifiedPromptManager:
    def __init__(self):
        self.providers = {}
        self.default_provider = None
        self.fallback_chain = []
    
    def register_provider(
        self, 
        provider_type: ProviderType, 
        provider_instance: PromptProvider
    ):
        """Register a prompt provider"""
        self.providers[provider_type] = provider_instance
        
        if self.default_provider is None:
            self.default_provider = provider_type
    
    def set_fallback_chain(self, provider_chain: List[ProviderType]):
        """Set fallback chain for provider failures"""
        self.fallback_chain = provider_chain
    
    def execute_with_fallback(
        self, 
        prompt: str, 
        preferred_provider: Optional[ProviderType] = None,
        **kwargs
    ) -> Dict:
        """Execute prompt with automatic fallback"""
        
        provider_to_try = preferred_provider or self.default_provider
        providers_tried = []
        
        # Try preferred provider first
        if provider_to_try in self.providers:
            result = self._try_provider(provider_to_try, prompt, **kwargs)
            providers_tried.append(provider_to_try)
            
            if "error" not in result:
                result["provider_used"] = provider_to_try.value
                result["providers_tried"] = [p.value for p in providers_tried]
                return result
        
        # Try fallback chain
        for fallback_provider in self.fallback_chain:
            if fallback_provider not in providers_tried and fallback_provider in self.providers:
                result = self._try_provider(fallback_provider, prompt, **kwargs)
                providers_tried.append(fallback_provider)
                
                if "error" not in result:
                    result["provider_used"] = fallback_provider.value
                    result["providers_tried"] = [p.value for p in providers_tried]
                    result["fallback_used"] = True
                    return result
        
        # All providers failed
        return {
            "error": "All providers failed",
            "providers_tried": [p.value for p in providers_tried]
        }
    
    def _try_provider(self, provider_type: ProviderType, prompt: str, **kwargs) -> Dict:
        """Try executing prompt with specific provider"""
        try:
            provider = self.providers[provider_type]
            return provider.execute_prompt(prompt, **kwargs)
        except Exception as e:
            return {"error": f"Provider {provider_type.value} failed: {str(e)}"}
    
    def compare_providers(
        self, 
        prompt: str, 
        providers: List[ProviderType],
        test_cases: List[Dict]
    ) -> Dict:
        """Compare performance across multiple providers"""
        
        comparison_results = {}
        
        for provider_type in providers:
            if provider_type not in self.providers:
                continue
            
            provider_results = []
            total_cost = 0
            
            for test_case in test_cases:
                formatted_prompt = prompt.format(**test_case["input"])
                result = self._try_provider(provider_type, formatted_prompt)
                
                if "error" not in result:
                    score = self._evaluate_response(
                        result["content"], 
                        test_case["expected"]
                    )
                    
                    provider_results.append({
                        "test_case": test_case["id"],
                        "score": score,
                        "execution_time": result.get("execution_time", 0),
                        "cost": result.get("cost", 0)
                    })
                    
                    total_cost += result.get("cost", 0)
            
            if provider_results:
                comparison_results[provider_type.value] = {
                    "average_score": sum(r["score"] for r in provider_results) / len(provider_results),
                    "average_time": sum(r["execution_time"] for r in provider_results) / len(provider_results),
                    "total_cost": total_cost,
                    "success_rate": len(provider_results) / len(test_cases),
                    "individual_results": provider_results
                }
        
        return comparison_results
```

### 2. Prompt Template Management System

```python
class PromptTemplateManager:
    def __init__(self):
        self.templates = {}
        self.template_metadata = {}
        self.usage_stats = {}
    
    def register_template(
        self, 
        template_id: str, 
        template: str, 
        metadata: Dict
    ):
        """Register a reusable prompt template"""
        self.templates[template_id] = template
        self.template_metadata[template_id] = {
            "description": metadata.get("description", ""),
            "parameters": metadata.get("parameters", []),
            "use_cases": metadata.get("use_cases", []),
            "performance_target": metadata.get("performance_target", 0.8),
            "created_at": time.time(),
            "version": metadata.get("version", "1.0")
        }
        self.usage_stats[template_id] = {
            "execution_count": 0,
            "success_count": 0,
            "average_score": 0.0
        }
    
    def execute_template(
        self, 
        template_id: str, 
        parameters: Dict,
        provider: Optional[ProviderType] = None
    ) -> Dict:
        """Execute template with parameters"""
        
        if template_id not in self.templates:
            return {"error": f"Template {template_id} not found"}
        
        # Validate parameters
        validation_result = self._validate_parameters(template_id, parameters)
        if not validation_result["valid"]:
            return {"error": f"Parameter validation failed: {validation_result['errors']}"}
        
        # Format template
        try:
            formatted_prompt = self.templates[template_id].format(**parameters)
        except KeyError as e:
            return {"error": f"Missing required parameter: {str(e)}"}
        
        # Execute prompt
        manager = UnifiedPromptManager()
        result = manager.execute_with_fallback(formatted_prompt, provider)
        
        # Update usage statistics
        self._update_usage_stats(template_id, result)
        
        result["template_id"] = template_id
        result["template_version"] = self.template_metadata[template_id]["version"]
        
        return result
    
    def optimize_template(
        self, 
        template_id: str, 
        test_cases: List[Dict]
    ) -> Dict:
        """Optimize template based on test cases"""
        
        if template_id not in self.templates:
            return {"error": f"Template {template_id} not found"}
        
        current_template = self.templates[template_id]
        
        # Test current performance
        current_performance = self._test_template_performance(
            current_template, test_cases
        )
        
        # Generate variations
        variations = self._generate_template_variations(current_template)
        
        # Test variations
        best_variation = current_template
        best_score = current_performance["average_score"]
        
        for variation in variations:
            performance = self._test_template_performance(variation, test_cases)
            
            if performance["average_score"] > best_score:
                best_variation = variation
                best_score = performance["average_score"]
        
        # Update template if improvement found
        if best_variation != current_template:
            self._create_template_version(template_id, best_variation)
            
            return {
                "optimized": True,
                "improvement": best_score - current_performance["average_score"],
                "new_version": self.template_metadata[template_id]["version"],
                "new_template": best_variation
            }
        else:
            return {
                "optimized": False,
                "current_performance": current_performance["average_score"],
                "message": "No improvement found"
            }
    
    def get_template_analytics(self, template_id: str) -> Dict:
        """Get comprehensive analytics for template"""
        
        if template_id not in self.templates:
            return {"error": f"Template {template_id} not found"}
        
        return {
            "template_id": template_id,
            "metadata": self.template_metadata[template_id],
            "usage_stats": self.usage_stats[template_id],
            "template_content": self.templates[template_id],
            "performance_trend": self._get_performance_trend(template_id)
        }
```

## Automated Workflow Integration

### 1. CI/CD Pipeline Integration

```python
class PromptCICD:
    def __init__(self):
        self.test_suites = {}
        self.deployment_configs = {}
        self.quality_gates = {
            "min_accuracy": 0.85,
            "max_cost_per_execution": 0.05,
            "max_execution_time": 5.0
        }
    
    def register_test_suite(self, prompt_id: str, test_cases: List[Dict]):
        """Register test suite for prompt"""
        self.test_suites[prompt_id] = test_cases
    
    def validate_prompt_deployment(self, prompt_id: str, prompt: str) -> Dict:
        """Validate prompt for deployment"""
        
        validation_results = {
            "prompt_id": prompt_id,
            "validation_passed": True,
            "quality_checks": {},
            "deployment_ready": False
        }
        
        # Run test suite
        if prompt_id in self.test_suites:
            test_results = self._run_test_suite(prompt, self.test_suites[prompt_id])
            validation_results["test_results"] = test_results
            
            # Check quality gates
            for gate, threshold in self.quality_gates.items():
                if gate == "min_accuracy":
                    passed = test_results["average_accuracy"] >= threshold
                elif gate == "max_cost_per_execution":
                    passed = test_results["average_cost"] <= threshold
                elif gate == "max_execution_time":
                    passed = test_results["average_time"] <= threshold
                else:
                    passed = True
                
                validation_results["quality_checks"][gate] = {
                    "threshold": threshold,
                    "actual": test_results.get(gate.replace("min_", "").replace("max_", ""), 0),
                    "passed": passed
                }
                
                if not passed:
                    validation_results["validation_passed"] = False
        
        # Security checks
        security_check = self._run_security_checks(prompt)
        validation_results["security_check"] = security_check
        
        if not security_check["passed"]:
            validation_results["validation_passed"] = False
        
        # Final deployment decision
        validation_results["deployment_ready"] = validation_results["validation_passed"]
        
        return validation_results
    
    def deploy_prompt(self, prompt_id: str, prompt: str, environment: str) -> Dict:
        """Deploy validated prompt to environment"""
        
        # Validate before deployment
        validation = self.validate_prompt_deployment(prompt_id, prompt)
        
        if not validation["deployment_ready"]:
            return {
                "deployed": False,
                "reason": "Validation failed",
                "validation_results": validation
            }
        
        # Deploy to environment
        deployment_config = self.deployment_configs.get(environment, {})
        
        try:
            # Store prompt in environment-specific storage
            self._store_prompt(prompt_id, prompt, environment, deployment_config)
            
            # Update routing configuration
            self._update_routing(prompt_id, environment)
            
            # Start monitoring
            self._start_monitoring(prompt_id, environment)
            
            return {
                "deployed": True,
                "environment": environment,
                "prompt_id": prompt_id,
                "deployment_timestamp": time.time(),
                "monitoring_enabled": True
            }
            
        except Exception as e:
            return {
                "deployed": False,
                "reason": f"Deployment failed: {str(e)}",
                "environment": environment
            }
```

### 2. Webhook Integration for Real-time Updates

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

class PromptWebhookServer:
    def __init__(self, prompt_manager: UnifiedPromptManager):
        self.app = Flask(__name__)
        self.prompt_manager = prompt_manager
        self.webhook_secret = None
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/webhook/feedback', methods=['POST'])
        def handle_feedback():
            """Handle feedback webhook for prompt optimization"""
            
            # Verify webhook signature
            if not self._verify_signature(request):
                return jsonify({"error": "Invalid signature"}), 401
            
            data = request.json
            
            # Process feedback
            result = self._process_feedback(data)
            
            return jsonify(result)
        
        @self.app.route('/webhook/performance', methods=['POST'])
        def handle_performance():
            """Handle performance data webhook"""
            
            if not self._verify_signature(request):
                return jsonify({"error": "Invalid signature"}), 401
            
            data = request.json
            
            # Update performance metrics
            result = self._update_performance_metrics(data)
            
            return jsonify(result)
        
        @self.app.route('/api/prompt/execute', methods=['POST'])
        def execute_prompt_api():
            """API endpoint for prompt execution"""
            
            data = request.json
            
            # Validate request
            if "prompt" not in data:
                return jsonify({"error": "Missing prompt"}), 400
            
            # Execute prompt
            result = self.prompt_manager.execute_with_fallback(
                data["prompt"],
                data.get("provider"),
                **data.get("parameters", {})
            )
            
            return jsonify(result)
    
    def _verify_signature(self, request) -> bool:
        """Verify webhook signature"""
        if not self.webhook_secret:
            return True  # Skip verification if no secret configured
        
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return False
        
        expected_signature = 'sha256=' + hmac.new(
            self.webhook_secret.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _process_feedback(self, feedback_data: Dict) -> Dict:
        """Process feedback data for prompt optimization"""
        
        prompt_id = feedback_data.get("prompt_id")
        feedback_score = feedback_data.get("score", 0)
        user_comments = feedback_data.get("comments", "")
        
        # Trigger optimization if score is low
        if feedback_score < 0.7:
            # Add to optimization queue
            optimization_result = self._queue_optimization(
                prompt_id, feedback_data
            )
            
            return {
                "processed": True,
                "optimization_queued": True,
                "optimization_id": optimization_result.get("id")
            }
        else:
            # Just log the positive feedback
            self._log_feedback(prompt_id, feedback_data)
            
            return {
                "processed": True,
                "optimization_queued": False
            }
```

## Monitoring and Analytics Integration

### 1. Performance Dashboard API

```python
class PromptAnalyticsDashboard:
    def __init__(self):
        self.metrics_store = MetricsStore()
        self.alert_manager = AlertManager()
    
    def get_dashboard_data(self, time_range: str = "24h") -> Dict:
        """Get comprehensive dashboard data"""
        
        # Parse time range
        start_time, end_time = self._parse_time_range(time_range)
        
        # Aggregate metrics
        dashboard_data = {
            "overview": self._get_overview_metrics(start_time, end_time),
            "performance": self._get_performance_metrics(start_time, end_time),
            "usage": self._get_usage_metrics(start_time, end_time),
            "costs": self._get_cost_metrics(start_time, end_time),
            "errors": self._get_error_metrics(start_time, end_time),
            "top_prompts": self._get_top_performing_prompts(start_time, end_time),
            "optimization_opportunities": self._get_optimization_opportunities()
        }
        
        return dashboard_data
    
    def get_prompt_performance(self, prompt_id: str, time_range: str = "7d") -> Dict:
        """Get detailed performance data for specific prompt"""
        
        start_time, end_time = self._parse_time_range(time_range)
        
        return {
            "prompt_id": prompt_id,
            "time_range": time_range,
            "execution_count": self.metrics_store.get_execution_count(
                prompt_id, start_time, end_time
            ),
            "average_score": self.metrics_store.get_average_score(
                prompt_id, start_time, end_time
            ),
            "cost_analysis": self.metrics_store.get_cost_analysis(
                prompt_id, start_time, end_time
            ),
            "performance_trend": self.metrics_store.get_performance_trend(
                prompt_id, start_time, end_time
            ),
            "error_rate": self.metrics_store.get_error_rate(
                prompt_id, start_time, end_time
            ),
            "user_satisfaction": self.metrics_store.get_user_satisfaction(
                prompt_id, start_time, end_time
            )
        }
```

### 2. Real-time Monitoring Integration

```python
import asyncio
import websockets
import json

class RealTimeMonitoring:
    def __init__(self):
        self.connections = set()
        self.metrics_stream = MetricsStream()
        self.alert_thresholds = {
            "error_rate": 0.05,
            "response_time": 10.0,
            "cost_spike": 2.0
        }
    
    async def start_monitoring_server(self, port: int = 8765):
        """Start WebSocket server for real-time monitoring"""
        
        async def handle_client(websocket, path):
            self.connections.add(websocket)
            try:
                await websocket.wait_closed()
            finally:
                self.connections.remove(websocket)
        
        # Start metrics streaming
        asyncio.create_task(self._stream_metrics())
        
        # Start WebSocket server
        await websockets.serve(handle_client, "localhost", port)
    
    async def _stream_metrics(self):
        """Stream real-time metrics to connected clients"""
        
        while True:
            # Collect current metrics
            current_metrics = {
                "timestamp": time.time(),
                "active_prompts": self.metrics_stream.get_active_prompt_count(),
                "requests_per_minute": self.metrics_stream.get_rpm(),
                "average_response_time": self.metrics_stream.get_avg_response_time(),
                "error_rate": self.metrics_stream.get_error_rate(),
                "cost_per_hour": self.metrics_stream.get_hourly_cost()
            }
            
            # Check for alerts
            alerts = self._check_alert_conditions(current_metrics)
            if alerts:
                current_metrics["alerts"] = alerts
            
            # Send to all connected clients
            if self.connections:
                message = json.dumps(current_metrics)
                await asyncio.gather(
                    *[conn.send(message) for conn in self.connections],
                    return_exceptions=True
                )
            
            await asyncio.sleep(5)  # Update every 5 seconds
    
    def _check_alert_conditions(self, metrics: Dict) -> List[Dict]:
        """Check if any alert conditions are met"""
        alerts = []
        
        for threshold_name, threshold_value in self.alert_thresholds.items():
            current_value = metrics.get(threshold_name, 0)
            
            if current_value > threshold_value:
                alerts.append({
                    "type": "threshold_exceeded",
                    "metric": threshold_name,
                    "current_value": current_value,
                    "threshold": threshold_value,
                    "severity": self._calculate_severity(threshold_name, current_value, threshold_value)
                })
        
        return alerts
```

## Integration Examples and Use Cases

### 1. E-commerce Chatbot Integration

```python
class EcommercePromptIntegration:
    def __init__(self):
        self.prompt_manager = UnifiedPromptManager()
        self.template_manager = PromptTemplateManager()
        self._setup_ecommerce_templates()
    
    def _setup_ecommerce_templates(self):
        """Setup predefined templates for e-commerce use cases"""
        
        templates = {
            "product_recommendation": {
                "template": """
                Based on the customer's purchase history and preferences, 
                recommend products that would interest them.
                
                Customer Profile:
                - Previous purchases: {purchase_history}
                - Preferences: {preferences}
                - Budget range: {budget_range}
                
                Provide 3-5 specific product recommendations with reasons.
                """,
                "metadata": {
                    "description": "Generates personalized product recommendations",
                    "parameters": ["purchase_history", "preferences", "budget_range"],
                    "use_cases": ["product_discovery", "upselling", "cross_selling"]
                }
            },
            "order_support": {
                "template": """
                Help resolve the customer's order-related inquiry professionally.
                
                Customer Issue:
                - Order ID: {order_id}
                - Issue Type: {issue_type}
                - Customer Message: {customer_message}
                - Order Status: {order_status}
                
                Provide a helpful response and suggest next steps.
                """,
                "metadata": {
                    "description": "Handles order support inquiries",
                    "parameters": ["order_id", "issue_type", "customer_message", "order_status"],
                    "use_cases": ["customer_support", "order_tracking", "issue_resolution"]
                }
            }
        }
        
        for template_id, template_data in templates.items():
            self.template_manager.register_template(
                template_id,
                template_data["template"],
                template_data["metadata"]
            )
    
    def handle_customer_inquiry(self, inquiry_type: str, customer_data: Dict) -> Dict:
        """Handle customer inquiry using appropriate template"""
        
        template_mapping = {
            "product_recommendation": "product_recommendation",
            "order_issue": "order_support",
            "general_support": "general_support"
        }
        
        template_id = template_mapping.get(inquiry_type)
        
        if template_id:
            return self.template_manager.execute_template(
                template_id, customer_data
            )
        else:
            # Fallback to general prompt
            return self.prompt_manager.execute_with_fallback(
                f"Help the customer with their {inquiry_type} inquiry: {customer_data}"
            )
```

### 2. Content Generation API

```python
class ContentGenerationAPI:
    def __init__(self):
        self.prompt_manager = UnifiedPromptManager()
        self.content_cache = ContentCache()
        self.quality_scorer = ContentQualityScorer()
    
    def generate_blog_post(
        self, 
        topic: str, 
        target_audience: str,
        word_count: int = 1000,
        style: str = "professional"
    ) -> Dict:
        """Generate blog post with quality validation"""
        
        prompt = f"""
        Write a {word_count}-word blog post about {topic} for {target_audience}.
        
        Requirements:
        - Style: {style}
        - Include an engaging introduction
        - Use clear headings and subheadings
        - Provide actionable insights
        - Include a compelling conclusion
        - Optimize for SEO
        
        Make the content valuable and engaging for the target audience.
        """
        
        # Check cache first
        cache_key = self._generate_cache_key(topic, target_audience, word_count, style)
        cached_content = self.content_cache.get(cache_key)
        
        if cached_content:
            return {
                "content": cached_content["content"],
                "from_cache": True,
                "quality_score": cached_content["quality_score"]
            }
        
        # Generate new content
        result = self.prompt_manager.execute_with_fallback(prompt)
        
        if "error" not in result:
            # Score content quality
            quality_score = self.quality_scorer.score_content(
                result["content"], topic, target_audience
            )
            
            # Cache if quality is good
            if quality_score > 0.8:
                self.content_cache.store(cache_key, {
                    "content": result["content"],
                    "quality_score": quality_score,
                    "generated_at": time.time()
                })
            
            result["quality_score"] = quality_score
            result["from_cache"] = False
        
        return result
```

## Conclusion

This API integration framework provides:

- **Multi-Provider Support**: Unified interface across major LLM providers
- **Production Ready**: Error handling, monitoring, and optimization
- **Scalable Architecture**: Template management and automated workflows
- **Real-time Capabilities**: WebSocket monitoring and webhook integration
- **Quality Assurance**: Automated testing and validation pipelines

The framework enables developers to integrate sophisticated prompt engineering capabilities into their applications with minimal complexity while maintaining production-grade reliability and performance.
