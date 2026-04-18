from config import setEnvironment
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.messages import SystemMessage, HumanMessage
#from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

setEnvironment()

# Simple example
'''
llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash" )
messages = [
    SystemMessage( content="You are a very artistic poet"),
    HumanMessage( content="Write a short poem about South Korea")
]
response = llm.invoke( messages )
print( response.content )
'''

# Chat prompt template example
'''
llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash" )
template = ChatPromptTemplate([
    ("system", "You are a very artistic poet"),
    ("user", "Wirte a shor poem about {text}")
])
formattedMsgs = template.format_messages(text="gender equality")
response = llm.invoke(formattedMsgs)
print(response.content)
'''

# Pipe example
'''
llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash" )
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()
# Chain them
chain = prompt | llm | output_parser
result = chain.invoke({"topic": "Hyun Chul Chung working at Arista Networks"})
print(result)
'''

# Multistep chaining (loses intermediate state)
'''
llm = GoogleGenerativeAI( model="gemini-2.5-flash" )
storyPrompt = PromptTemplate.from_template("Write a short story about {topic}")
storyChain = storyPrompt | llm | StrOutputParser()

analysisPrompt = PromptTemplate.from_template(
    "Analyze the following story's mood:\n{story}")
analysisChain = analysisPrompt | llm | StrOutputParser()

storyWithAnalysis = storyChain | analysisChain
storyAnalysis = storyWithAnalysis.invoke({"topic": "flowers"})
print("Analysis:", storyAnalysis)
'''

# Multistep chaining (preserve intermediate state)
'''
llm = GoogleGenerativeAI( model="gemini-2.5-flash" )
storyPrompt = PromptTemplate.from_template("Write a short poem about {topic}")
storyChain = storyPrompt | llm | StrOutputParser()

analysisPrompt = PromptTemplate.from_template(
    "Analyze the following poem's mood:\n{story}")
analysisChain = analysisPrompt | llm | StrOutputParser()

enhancedChain = RunnablePassthrough.assign(
    story=storyChain
).assign(
    analysis=analysisChain
)
result = enhancedChain.invoke({"topic": "chess"})
print(result.keys())
'''

# Multistep chaining (preserve intermediate state; more control over output structure)
'''
llm = GoogleGenerativeAI( model="gemini-2.5-flash" )
storyPrompt = PromptTemplate.from_template("Write a short poem about {topic}")
storyChain = storyPrompt | llm | StrOutputParser()

analysisPrompt = PromptTemplate.from_template(
    "Analyze the following poem's mood:\n{story}")
analysisChain = analysisPrompt | llm | StrOutputParser()

manualChain = RunnablePassthrough() | {
    "story": storyChain,
    "topic": itemgetter("topic")
} | RunnablePassthrough.assign(
    analysis=analysisChain
)
result = manualChain.invoke({"topic": "chess"})
print(result.values())
'''

# Simplifying multistep chaining with piping
llm = GoogleGenerativeAI( model="gemini-2.5-flash" )
storyPrompt = PromptTemplate.from_template("Write a short poem about {topic}")
storyChain = storyPrompt | llm | StrOutputParser()

analysisPrompt = PromptTemplate.from_template(
    "Analyze the following poem's mood:\n{story}")
analysisChain = analysisPrompt | llm | StrOutputParser()

simpleChain = storyChain | {"analysis": analysisChain}
result = simpleChain.invoke( {"topic": "a rainy day"} )
print( result.keys() )