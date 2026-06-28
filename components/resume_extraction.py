from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.resume_analyze_state_schema import ResumeExtractionPydanticModel
from langchain_openai import ChatOpenAI

def get_info_from_resume(llm: ChatOpenAI, resume: str):
    RESUME_EXTRACTION_SYSTEM_PROMPT = """You are a resume parsing engine. Your only job is to extract \
        structured information from the resume text provided by the user. You do not evaluate, judge, \
        or score the resume — that happens in a later step. You only extract what is explicitly present.

        Extract the following:

        1. candidate_name: The candidate's full name as it appears at the top of the resume. \
        If no name is found, return null.

        2. experience_summary: A neutral, factual 2-3 sentence summary of the candidate's work \
        history (roles, companies, domains worked in). Do not editorialize or evaluate quality — \
        just summarize what is there.

        3. total_experience_years: Total years of professional work experience, calculated from \
        employment dates listed on the resume. Sum the duration of all listed roles. If dates overlap \
        (e.g., concurrent jobs), do not double count the overlapping period. If dates are ambiguous or \
        missing, make a reasonable estimate — but always return a number.

        4. extracted_skills: Every skill explicitly mentioned anywhere in the resume. For each skill, \
        assign exactly one category:
        - "technical": programming languages, frameworks, technical concepts
        - "tool": named software/platforms (e.g., Docker, Jira, Excel)
        - "domain": industry or subject-matter knowledge (e.g., healthcare compliance)
        - "soft": interpersonal/non-technical skills (e.g., leadership, communication)
        Do not infer skills that are not explicitly stated.

        5. extracted_projects: Every project, work experience entry, or notable initiative described \
        with enough detail to evaluate. For each: name, description (1-2 sentences), skills_used \
        (must overlap with extracted_skills where applicable), and impact (quantified outcome if \
        explicitly stated, otherwise null — never fabricate metrics).

        Rules:
        - Extract only what is stated or directly evidenced in the text. Do not infer, embellish, or assume.
        - If a section is entirely absent, return an empty list rather than fabricating entries.
        - Resume text may contain PDF/DOCX formatting artifacts (extra whitespace, broken line breaks, \
        garbled bullets). Parse through these; do not treat them as content.

        {format_instructions}

        Respond with ONLY the JSON object. No preamble, no explanation, no markdown code fences.
        """

    RESUME_EXTRACTION_USER_PROMPT = """Extract structured information from the following resume.

    <resume>
    {resume}
    </resume>
    """
    
    parser = PydanticOutputParser(pydantic_object=ResumeExtractionPydanticModel)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system" , RESUME_EXTRACTION_SYSTEM_PROMPT),
        ("human", RESUME_EXTRACTION_USER_PROMPT)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "resume": resume
    })
    
    return response