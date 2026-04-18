from config import setEnvironment
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Optional, Union, Literal
from typing_extensions import TypedDict
#from IPython.display import Image, display

setEnvironment()

# Langgraph example with conditional edges (no reducer)
'''
# The state schema
class JobApplicationState( TypedDict ):
    jobDescription: str
    isSuitable: bool
    application: str

def analyzeJobDescription( state ):
    print( "...Analyzing the provided JD..." )
    return { "isSuitable": len( state["jobDescription"] ) > 20 }

def generateApplication( state ):
    print( "...Generating application...")
    return { "application": "some_fake_application" }

builder = StateGraph( JobApplicationState )
builder.add_node( "analyzeJobDescription", analyzeJobDescription )
builder.add_node( "generateApplication", generateApplication )

def isSuitableCondition( state: JobApplicationState ) -> Literal[ "generateApplication", END ]:
    if state.get( "isSuitable" ):
        print( "...condition met..." )
        return "generateApplication"
    return END

builder.add_edge( START, "analyzeJobDescription" )
builder.add_conditional_edges( "analyzeJobDescription", isSuitableCondition )
builder.add_edge( "generateApplication", END )

graph = builder.compile()

#display( Image( graph.get_graph().draw_mermaid_png() ) )

result = graph.invoke( {"jobDescription": "This should go over twenty letters"} )
print( result )
'''

# Langgraph example with custom reducer
def myReducer(left: list[str], right: Optional[Union[str, list[str]]]) -> list[str]:
  if right:
    return left + [right] if isinstance(right, str) else left + right
  return left

class JobApplicationState( TypedDict ):
    jobDescription: str
    isSuitable: bool
    application: str
    actions: Annotated[list[str], myReducer]

def analyzeJobDescription( state ):
    print( "...Analyzing the provided JD..." )
    return { "isSuitable": len( state["jobDescription"] ) > 20, "actions": "action1" }

def generateApplication( state ):
    print( "...Generating application...")
    return { "application": "some_fake_application", "actions": ["action2", "action3"] }

builder = StateGraph( JobApplicationState )
builder.add_node( "analyzeJobDescription", analyzeJobDescription )
builder.add_node( "generateApplication", generateApplication )

def isSuitableCondition( state: JobApplicationState ) -> Literal[ "generateApplication", END ]:
    if state.get( "isSuitable" ):
        return "generateApplication"
    return END

builder.add_edge( START, "analyzeJobDescription" )
builder.add_conditional_edges( "analyzeJobDescription", isSuitableCondition )
builder.add_edge( "generateApplication", END )

graph = builder.compile()

#display( Image( graph.get_graph().draw_mermaid_png() ) )

result = graph.invoke( {"jobDescription": "This should go over twenty letters"} )
print( result )

# Important built-in reducer (add_messages)
'''
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class JobApplicationState( TypedDict ):
    ...
    messages : Annotated[ list[ AnyMessage ], add_messages]

# There is a built-in state for this reducer (MessagesState)
# class JobApplicationState( MessagesState ):
#    ...
'''

