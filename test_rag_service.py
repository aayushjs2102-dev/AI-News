from services.rag_services.rag_service import RAGService

rag = RAGService()

question = input("Question: ")

result = rag.answer(question)

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)

print(result["answer"])

print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

for article in result["articles"]:
    print(f"- {article['source']}")
    print(f"  {article['title']}")
    print(f"  Score: {article['similarity_score']:.4f}")
    print()