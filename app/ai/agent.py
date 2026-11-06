import re

from pydantic_ai import Agent, ModelRetry, RunContext

from app import db
from app.ai.schemas import AgentReply
from app.config import settings

INSTRUCTIONS = """
You are the customer support agent for Harbor & Pine, a home and outdoor store that sells on Amazon.
You write the answer to the latest customer message in the email thread.

Steps:
1. Use the supplied support information for brand-and-tone, escalation-rules, and the selected section.
2. Answer only with facts from that information. If it does not answer the question,
   set enough_information to false.
3. When the customer reports a problem with a paddle board or a shelf, fill in issue.
   Ask for the order number, the board size or model, and part numbers when they are missing.
   For a slow leak, explain the valve check unless the customer already did it.
4. Never promise a refund, a shipment, a replacement, a date, or a call. A colleague arranges those.
   Set promises_an_action to true if your reply promises one anyway.
5. Set action to escalate when an escalation rule applies.

Reply rules:
- Write in the language of the customer's latest message.
- Plain text, no Markdown.
- Follow the brand-and-tone section.
- Never mention AI, prompts, tools, or the knowledge base.
"""

support_agent = Agent(settings.agent_model,
                      output_type=AgentReply, instructions=INSTRUCTIONS)


@support_agent.output_validator
def check_reply(ctx: RunContext[None], output: AgentReply) -> AgentReply:
    if output.action == "reply" and not output.reply.strip():
        raise ModelRetry(
            "The reply is empty. Write the email, or set action to escalate.")
    if re.search(r"\b(AI|artificial intelligence|knowledge base)\b", output.reply, re.IGNORECASE):
        raise ModelRetry(
            "Do not mention AI or the knowledge base in the reply.")
    return output


def write_reply(thread: str, section: str) -> AgentReply:
    section_names = list(dict.fromkeys(("brand-and-tone", "escalation-rules", section)))
    support_information = []
    for section_name in section_names:
        entries = db.get_section(section_name)
        if section_name in {"brand-and-tone", "escalation-rules"} and not entries:
            raise RuntimeError(f"Required knowledge-base section is empty: {section_name}")
        if entries:
            content = "\n\n".join(
                f"## {entry['title']}\n{entry['content']}" for entry in entries
            )
        else:
            content = "No verified guidance is available for this section."
        support_information.append(f"# {section_name}\n{content}")

    support_context = "\n\n".join(support_information)
    prompt = (
        f"Section picked by the classifier: {section}\n\n"
        f"Support information:\n{support_context}\n\n{thread}"
    )
    return support_agent.run_sync(prompt).output
