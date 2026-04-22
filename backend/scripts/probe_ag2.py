"""Probe AG2 API to understand what's available in v0.12."""
import autogen, inspect
print("AG2 version:", autogen.__version__)
attrs = [a for a in dir(autogen) if not a.startswith('_')]
print("Top-level exports:", attrs[:30])

# Check ConversableAgent
try:
    from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
    print("ConversableAgent OK")
    print("  __init__ params:", list(inspect.signature(ConversableAgent.__init__).parameters.keys())[:15])
except Exception as e:
    print("ConversableAgent ERROR:", e)

# Check if register_for_llm / register_for_execution available
try:
    from autogen import register_function
    print("register_function OK")
except Exception as e:
    print("register_function:", e)

# Check tool support
try:
    agent = AssistantAgent(name="test", llm_config=False)
    print("AssistantAgent without LLM OK")
except Exception as e:
    print("AssistantAgent ERROR:", e)
