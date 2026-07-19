"""
RAG Context Builder

Author: Aayush
"""


class ContextBuilder:
    """
    Builds a clean context string from
    retrieved news articles.
    """

    def build(self, articles):

        if not articles:
            return "No relevant news articles found."

        sections = []

        for i, article in enumerate(articles, start=1):

            section = (
                f"Article {i}\n"
                f"Title: {article['title']}\n"
                f"Source: {article['source']}\n"
                f"Category: {article['category']}\n"
                f"Summary: {article['summary']}\n"
                "----------------------------------------"
            )

            sections.append(section)

        return "\n\n".join(sections)