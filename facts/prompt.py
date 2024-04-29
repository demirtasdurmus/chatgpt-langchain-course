# Load env variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')

from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever
import langchain

langchain.debug= True

chat = ChatOpenAI()

embeddings = OpenAIEmbeddings()

db = Chroma(persist_directory='emb', embedding_function=embeddings)

retriever = RedundantFilterRetriever(
  embedding=embeddings,
  chroma=db
)

chain = RetrievalQA.from_chain_type(
  llm=chat,
  retriever=retriever,
  # use this for 99 of the scenarios others mapreduce refine ...
  chain_type='stuff'
)

result = chain.run("What is an interesting thing about English language?")

print(result)