import json
import operator
from typing import Dict, Any, List
from functools import partial
from config import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

# Import modular agents
from agents.state import ReviewState
from agents.security import security_node
from agents.performance import performance_node
from agents.style import style_node
from agents.aggregator import aggregator_node

class CodeAnalyzer:    
    def __init__(self):
        # Initialize LangChain Groq model
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=0.2
        )
        self.parser = JsonOutputParser()
        self.graph = self._build_review_graph()

    def _build_review_graph(self):
        workflow = StateGraph(ReviewState)

        # Partial functions to inject dependencies into nodes
        security_call = partial(security_node, llm=self.llm, parser=self.parser)
        performance_call = partial(performance_node, llm=self.llm, parser=self.parser)
        style_call = partial(style_node, llm=self.llm, parser=self.parser)

        # Define Nodes
        workflow.add_node("security_expert", security_call)
        workflow.add_node("performance_guru", performance_call)
        workflow.add_node("style_architect", style_call)
        workflow.add_node("aggregator", aggregator_node)

        # Define Edges
        workflow.set_entry_point("security_expert")
        workflow.add_edge("security_expert", "performance_guru")
        workflow.add_edge("performance_guru", "style_architect")
        workflow.add_edge("style_architect", "aggregator")
        workflow.add_edge("aggregator", END)

        return workflow.compile()

    # --- Public API Methods ---

    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code using a Multi-Agent LangGraph workflow
        """
        try:
            initial_state = {
                "code": code,
                "language": language.upper(),
                "security_issues": [],
                "performance_issues": [],
                "style_issues": [],
                "suggestions": [],
                "scores": [],
                "final_result": {}
            }
            
            final_output = self.graph.invoke(initial_state)
            return final_output["final_result"]
            
        except Exception as e:
            print(f"DEBUG: LangGraph Workflow failed ({str(e)}). Using Mock Mode.")
            return {
                "score": 8,
                "issues": ["Graph failed to execute, falling back to mock."],
                "suggestions": ["Check API logs for graph connectivity."],
                "reasoning": f"Multi-agent review failed: {str(e)[:100]}",
                "language": language
            }

    def generate_code(self, prompt: str, language: str) -> Dict[str, Any]:
        """
        Generate code based on a prompt using LangChain
        """
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an expert {language} developer. Generate clean, efficient, and well-documented code. You must respond with valid JSON only."),
                ("user", self._get_generation_prompt_template())
            ])
            
            chain = prompt_template | self.llm | self.parser
            
            result = chain.invoke({
                "prompt": prompt,
                "language": language
            })
            
            return result
            
        except Exception as e:
            print(f"DEBUG: LangChain Generation API Call failed ({str(e)}). Using Mock Mode.")
            return {
                "code": f"// Mock code for: {prompt}\nfunction example() {{\n  console.log('AI Generation is currently in mock mode.');\n}}",
                "explanation": "This is a fallback response since the AI service encountered an error.",
                "language": language
            }
    
    def chat(self, code: str, review_context: str, messages: List[Dict[str, str]], language: str) -> str:
        """
        Hold a follow-up conversation about the code review
        """
        try:
            # Prepare conversation history for LangChain
            history = []
            for msg in messages:
                role = "human" if msg["role"] == "user" else "ai"
                history.append((role, msg["content"]))

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self._get_chat_system_template()),
                *history
            ])
            
            # For chat, we don't necessarily need a JSON parser unless we want structured chat
            # For now, simple string response is better for a chat interface
            chain = prompt_template | self.llm
            
            result = chain.invoke({
                "code": code,
                "review_context": review_context,
                "language": language
            })
            
            return result.content
            
        except Exception as e:
            print(f"DEBUG: LangChain Chat API Call failed ({str(e)}).")
            return f"I'm sorry, I'm having trouble connecting to the AI service right now. Error: {str(e)[:100]}"
    
    def _get_chat_system_template(self) -> str:
        """System template for follow-up chat"""
        return """You are a senior software engineer. You just reviewed some {language} code. 
A junior developer has a follow-up question about your review or the code itself.

Context:
---
Code:
```{language}
{code}
```

Your Previous Review:
{review_context}
---

Be helpful, concise, and professional in your answers. If the developer asks for a fix, explain the fix and show the corrected code.
"""

    def _get_generation_prompt_template(self) -> str:
        """Instruction template for code generation"""
        return """Task: {prompt}
Language: {language}

You must respond with a JSON object in this exact format:
{{
    "code": "<the generated code string>",
    "explanation": "<brief explanation of how the code works>",
    "language": "{language}"
}}
"""
