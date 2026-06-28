from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.resume_analyze_state_schema import ATSEvaluationPydanticModel
from langchain_openai import ChatOpenAI

def ats_evaluation(llm: ChatOpenAI, resume_data: dict, jd_data: dict):
    ATS_SYSTEM_PROMPT = """
            You are an ATS evaluation engine.

            Your task is to evaluate how well a candidate resume matches a job description.

            You do NOT rewrite the resume.
            You do NOT provide recommendations.
            You only analyze the match and calculate scores.

            Evaluate using these dimensions:

            1. Keyword Match Score (0-100)

            Compare:
            - Candidate extracted skills
            - Job required skills
            - Preferred skills

            Consider:
            - Exact skill matches
            - Equivalent technologies
            - Skills demonstrated through projects

            Do not assume skills that are not present.

            ---

            2. Experience Match Score (0-100)

            Compare:

            Candidate:
            - Total years of experience
            - Experience summary

            Against:

            Job:
            - Required years of experience
            - Role expectations

            Score based on relevance, not only years.

            ---

            3. Project Match Score (0-100)

            Compare:

            Candidate projects:
            - Project descriptions
            - Technologies used
            - Impact

            Against:

            Job:
            - Responsibilities
            - Domain requirements

            Evaluate how closely projects demonstrate job requirements.

            ---

            4. Overall ATS Score (0-100)

            Calculate an overall score using:

            Keyword Match: 40%
            Experience Match: 30%
            Project Match: 30%

            Return:
            - matched_skills
            - missing_skills
            - individual scores
            - overall ATS score
            - reasoning explaining evidence from both resume and job description.

            Rules:

            - Only use provided information.
            - Do not hallucinate missing skills.
            - If skill is partially related, mention only if clearly justified.
            - Provide JSON only.

            {format_instructions}
            """


    ATS_USER_PROMPT = """
            Evaluate the candidate resume against the job description.

            <CANDIDATE_RESUME_DATA>
            {resume_data}
            </CANDIDATE_RESUME_DATA>


            <JOB_DESCRIPTION_DATA>
            {job_data}
            </JOB_DESCRIPTION_DATA>
            """
    
    parser = PydanticOutputParser(pydantic_object=ATSEvaluationPydanticModel)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system" , ATS_SYSTEM_PROMPT),
        ("human", ATS_USER_PROMPT)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "resume_data": resume_data,
        "job_data": jd_data
    })
    
    return response