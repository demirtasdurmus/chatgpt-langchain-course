# Load env variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
## This one is deprecated
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

emb = embeddings.embed_query('Hi there')

text_splitter = CharacterTextSplitter(
  separator='\n',
  chunk_size=200,
  chunk_overlap=0
)

loader = TextLoader('facts.txt')
docs = loader.load_and_split(text_splitter=text_splitter)

for doc in docs:
  print(doc.page_content)
  print('\n')