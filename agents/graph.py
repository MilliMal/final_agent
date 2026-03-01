"""LangGraph Agent Implementation"""
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Any
import operator
from langchain_core.messages import AnyMessage, BaseMessage
from langchain_openai import ChatOpenAI
import os

class AgentState(TypedDict):
    """State schema for the agent graph"""
    user_id: str
    input: str
    messages: Annotated[list[AnyMessage], operator.add]
    output: str

def create_agent_graph():
    """
    Create and compile the LangGraph agent
    
    Returns:
        Compiled graph ready for invocation
    """
    # Initialize language model
    llm = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL', 'gpt-4'),
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0.7
    )
    
    # Create state graph
    workflow = StateGraph(AgentState)
    
    def process_input(state: AgentState) -> AgentState:
        """Process user input through the LLM"""
        messages = state.get('messages', [])
        user_input = state['input']
        
        # Add user message
        from langchain_core.messages import HumanMessage
        messages.append(HumanMessage(content=user_input))
        
        # Get response from LLM
        response = llm.invoke(messages)
        messages.append(response)
        
        return {
            **state,
            'messages': messages,
            'output': response.content
        }
    
    # Add nodes
    workflow.add_node('process', process_input)
    
    # Set entry point
    workflow.set_entry_point('process')
    
    # Set finish point
    workflow.set_finish_point('process')
    
    # Compile graph
    graph = workflow.compile()
    
    return graph
