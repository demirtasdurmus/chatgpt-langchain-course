# Load env variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')

# from langchain.chat_models import ChatOpenAI

from langchain_openai import ChatOpenAI

from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory, ConversationSummaryMemory

chat = ChatOpenAI(
  # Output details
  verbose=True
  )

# This is the first approach, saving full context to the memory
# memory = ConversationBufferMemory(
#   chat_memory=FileChatMessageHistory('messages.json'),
#   memory_key='messages', 
#   # Dont just throw strings but add the appropriate objects including these strings
#   return_messages=True
#   )

# This is the second approach, saving just the summary context to the memory
memory = ConversationSummaryMemory(
  # Saving the context to a file is omitted, because FileChatMessageHistory does not work well with this one
  memory_key='messages',
  return_messages=True,
  # LLM to use to summarize context
  llm=chat
)

prompt = ChatPromptTemplate(
  input_variables=['content', 'messages'],
  messages=[
    # Tells to find messages
    MessagesPlaceholder(variable_name='messages'),
    HumanMessagePromptTemplate.from_template("{content}")
  ]
)

chain = LLMChain(
  llm=chat,
  prompt=prompt,
  memory=memory,
  verbose=True
)


while True:
  content = input('>> ')

  result = chain({"content": content})
  print(result['text'])