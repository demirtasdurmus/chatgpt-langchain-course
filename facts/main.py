# Load env variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
## This one is deprecated
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

embeddings = OpenAIEmbeddings()

emb = embeddings.embed_query('Hi there')

text_splitter = CharacterTextSplitter(
  separator='\n',
  chunk_size=200,
  chunk_overlap=0
)

loader = TextLoader('facts.txt')
docs = loader.load_and_split(
  text_splitter=text_splitter
  )

db = Chroma.from_documents(
  docs,
  embedding=embeddings,
  persist_directory='emb'
)

# for doc in docs:
#   print(doc.page_content)
#   print('\n')

results = db.similarity_search('What is the interesting fact about the English language')

for result in results:
  print('\n')
  # print(result[1])
  # print(result[0].page_content)
  print(result.page_content)