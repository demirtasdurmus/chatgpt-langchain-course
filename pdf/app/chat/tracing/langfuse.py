import os
from langfuse.client import Langfuse

langfuse = Langfuse(
  os.environ['LANGFUSE_PUBLIC_KEY'],
  os.environ['LANGFUSE_SECRET_KEY'],
  host = 'https://cloud.langfuse.com' # this is by default
  # host = 'https://prod-langfuse.fly.dev' # this is stephens hosted server
);