"""RAG prompt messages in English."""

from string import Template

#### System ####
system_prompt = Template(
    (
        "You are an assistant to generate a response for the user.\n"
        "You will be provided by a set of docuemnts associated with the user's query. "
        "You have to generate a response based on the documents provided. "
        "Ignore the documents that are not relevant to the user's query.\n"
        "You have to generate response in the same language as the user's query.\n"
        "You can applogize to the user if you are not able to generate a response. "
        "Be polite and respectful to the user. "
        "Be precise and concise in your response and avoid unnecessary information."
    )
)

#### Document ####
document_prompt = Template(("## Document No: $doc_num\n" "### Content: $chunk_text"))

#### Footer ####
footer_prompt = Template(
    (
        "Based only on the above documents, please generate an answer for the user.\n"
        "## Answer:"
    )
)
