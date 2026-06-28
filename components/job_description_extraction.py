from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.resume_analyze_state_schema import JobExtractionPydanticModel
from langchain_openai import ChatOpenAI

def get_info_from_job_description(llm: ChatOpenAI, job_description: str):
    JOB_EXTRACTION_SYSTEM_PROMPT = """You are an expert technical recruiter and information extraction system.
    Your task is to read a job description and extract structured information from it
    with high precision. Follow these rules strictly:

    1. Extract only information that is explicitly present in the job description. Do not
    infer, assume, or fabricate details that are not stated.
    2. For fields that are optional and not mentioned in the text, return null (or an empty
    list for list fields) rather than guessing a value.
    3. When classifying a skill's category, use:
    - "technical" for programming languages, frameworks, and technical concepts
    - "tool" for named software, platforms, or tools (e.g. Docker, Jenkins, Jira)
    - "soft" for interpersonal or communication-related skills
    - "domain" for industry or business-domain knowledge (e.g. healthcare, fintech)
    4. When classifying a skill's requirement_level, mark it "required" only if the job
    description uses language indicating it is mandatory (e.g. "must have", "required",
    "X+ years of experience in"). Mark it "preferred" if the language is optional
    (e.g. "nice to have", "preferred", "a plus", "bonus").
    5. Extract responsibilities as distinct, atomic items — split compound bullet points
    into separate responsibilities where it makes sense, but do not merge unrelated duties.
    6. Return only the structured output in the exact format requested. Do not include any
    commentary, explanation, or text outside of the requested format.

    {format_instructions}
    """

    JOB_EXTRACTION_USER_PROMPT = """Extract structured information from the following job description.

    Job Description:
    {job_description}
    """
    
    parser = PydanticOutputParser(pydantic_object=JobExtractionPydanticModel)
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", JOB_EXTRACTION_SYSTEM_PROMPT),
        ("human", JOB_EXTRACTION_USER_PROMPT)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm | parser
    
    result = chain.invoke({
        "job_description": job_description
    })
    
    return result