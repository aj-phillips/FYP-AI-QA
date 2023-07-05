from flask import Flask, jsonify, request
from haystack.pipelines import FAQPipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever
import pandas as pd
from flask_cors import CORS, cross_origin

# Initialize the pipeline
document_store = InMemoryDocumentStore()
retriever = EmbeddingRetriever(document_store=document_store, embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                               use_gpu=True, scale_score=False)
pipe = FAQPipeline(retriever=retriever)

# Load the FAQs
df = pd.read_csv("Data/qa-pairs.csv")
df.fillna(value="", inplace=True)
df["question"] = df["question"].apply(lambda x: x.strip())
questions = list(df["question"].values)
df["embedding"] = retriever.embed_queries(queries=questions).tolist()
df = df.rename(columns={"question": "content"})
docs_to_index = df.to_dict(orient="records")
document_store.write_documents(docs_to_index)

# Create the Flask app
app = Flask(__name__)


@app.route("/api/predict", methods=["POST"])
@cross_origin()
def predict():
    # Get the query from the POST request
    query = request.json["query"]

    # Run the query through the pipeline
    prediction = pipe.run(query=query, params={"Retriever": {"top_k": 1}})

    # Return the answer(s) as a JSON response
    response = {"answers": prediction["answers"]}
    return jsonify(response)


# Run the app
if __name__ == "__main__":
    app.run(debug=False)
