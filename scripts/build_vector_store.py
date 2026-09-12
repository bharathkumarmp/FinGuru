from app.rag.pipeline import build_vector_store


print("=" * 60)
print("FINGURU RAG VECTOR STORE BUILD")
print("=" * 60)


result = build_vector_store(
    data_directory="rag_data"
)


print("\nDocuments :", result["documents"])
print("Chunks    :", result["chunks"])

print("\n" + "=" * 60)
print("VECTOR STORE BUILD COMPLETE")
print("=" * 60)