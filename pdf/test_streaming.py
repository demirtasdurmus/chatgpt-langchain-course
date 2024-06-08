from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from threading import Thread

class StreamingHandler(BaseCallbackHandler):
  def __init__(self, queue):
    self.queue = queue

  def on_llm_new_token(self, token, **kwargs):
    self.queue.put(token)

  # to break the while loop when content is finished, see while loop in StreamingChain
  def on_llm_end(self, response, **kwargs):
    self.queue.put(None)

  # to break the while loop if an error occurs
  def on_llm_error(self, error, **kwargs):
    self.queue.put(None)

chat = ChatOpenAI(
  streaming=True
  )

prompt = ChatPromptTemplate.from_messages([
  ('human', '{content}')
])

class StreamableChain:
  def stream(self, input): 
    queue = Queue()
    handler = StreamingHandler(queue)

    def task():
      self(input, callbacks=[handler])

    # offloading this 'task' to a separate thread
    Thread(target=task).start()

    while True:
      token = queue.get()
      if token is None:
        break
      yield token

class StreamingChain(StreamableChain, LLMChain):
  pass

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={'content': 'Tell me a joke'}):
  print(output)



# messages = prompt.format_messages(content='Tell me a joke')

# # Streaming here will override chatopenai streaming config
# for message in chat.stream(messages):
#   print(message.content)
