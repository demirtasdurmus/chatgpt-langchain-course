from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from threading import Thread

queue = Queue()

class StreamingHandler(BaseCallbackHandler):
  def on_llm_new_token(self, token, **kwargs):
    queue.put(token)

  # to break the while loop when content is finished, see while loop in StreamingChain
  def on_llm_end(self, response, **kwargs):
    queue.put(None)

  # to break the while loop if an error occurs
  def on_llm_error(self, error, **kwargs):
    queue.put(None)

chat = ChatOpenAI(
  streaming=True,
  callbacks=[StreamingHandler()]
  )

prompt = ChatPromptTemplate.from_messages([
  ('human', '{content}')
])

class StreamingChain(LLMChain):
  def stream(self, input): 
    def task():
      self(input)

    # offloading this 'task' to a separate thread
    Thread(target=task).start()

    while True:
      token = queue.get()
      if token is None:
        break
      yield token

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={'content': 'Tell me a joke'}):
  print(output)



# messages = prompt.format_messages(content='Tell me a joke')

# # Streaming here will override chatopenai streaming config
# for message in chat.stream(messages):
#   print(message.content)
