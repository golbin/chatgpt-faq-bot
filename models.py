from pydantic import BaseModel


class Document(BaseModel):
    id: str
    question: str
    answer: str
    score: float


class Query(BaseModel):
    query: str
    top_k: int
