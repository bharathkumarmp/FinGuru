from typing import Optional

from app.rag.retriever import retrieve, build_context


def build_customer_context(
    monthly_income: float,
    monthly_spending: float,
    monthly_surplus: float,
    savings_rate: float,
    emi_ratio: float,
    financial_health: float,
    financial_stress: float,
) -> str:
    """
    Build a minimized financial context for the Copilot.

    Do not include unnecessary PII such as:
    - account numbers
    - phone numbers
    - email addresses
    - authentication information
    """

    return f"""
Customer Financial State:

Monthly Income: ₹{monthly_income:,.2f}
Monthly Spending: ₹{monthly_spending:,.2f}
Monthly Surplus: ₹{monthly_surplus:,.2f}
Savings Rate: {savings_rate:.2f}
EMI Ratio: {emi_ratio:.2f}
Financial Health Score: {financial_health:.1f}/100
Financial Stress Score: {financial_stress:.1f}/100
""".strip()


def build_copilot_prompt(
    question: str,
    knowledge_context: str,
    customer_context: Optional[str] = None,
) -> str:
    """
    Build the final prompt used by the LLM.

    The architecture follows:
    RAG knowledge + customer financial state + safety instructions.
    """

    customer_section = ""

    if customer_context:
        customer_section = f"""
CUSTOMER FINANCIAL CONTEXT
---------------------------
{customer_context}
"""

    return f"""
You are FinGuru, an AI-powered personal financial copilot.

Your role is to help customers understand their financial situation
and make responsible financial decisions.

IMPORTANT RULES:
1. Use the provided banking knowledge as the primary source.
2. Use customer financial context only when it is relevant.
3. Never invent customer information.
4. Never claim that a loan or financial product is approved.
5. Do not encourage borrowing when affordability is poor.
6. Explain financial concepts in simple language.
7. Do not expose sensitive personal information.
8. If information is insufficient, clearly say so.
9. Do not make decisions that should be made by the bank.
10. Recommendations must prioritize customer suitability and affordability,
    not product sales.

BANKING KNOWLEDGE
-----------------
{knowledge_context}

{customer_section}

CUSTOMER QUESTION
-----------------
{question}

Provide a concise, helpful answer.

If the question involves a financial recommendation:
- explain the relevant factors,
- use the available customer financial state,
- state the recommended action,
- explain why.

If the question is about a suspicious transaction or security issue,
prioritize customer safety and official bank security procedures.

Answer:
""".strip()


def retrieve_copilot_context(
    question: str,
    top_k: int = 5,
) -> dict:
    """
    Retrieve relevant knowledge for a Copilot question.
    """

    results = retrieve(
        query=question,
        top_k=top_k,
    )

    context = build_context(results)

    sources = []

    for result in results:
        metadata = result.get("metadata", {})

        sources.append(
            {
                "source": metadata.get("source", "unknown"),
                "category": metadata.get("category", "unknown"),
                "distance": result.get("distance"),
            }
        )

    return {
        "context": context,
        "sources": sources,
    }