from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.resume_analyze_state_schema import Recommendation
from langchain_openai import ChatOpenAI

def recommendation_generator(llm: ChatOpenAI, resume_data: dict, jd_data: dict, ats_result: dict):
    
    RECOMMENDATION_SYSTEM_PROMPT = """

        You are a professional resume improvement advisor.

        Your job is to generate ONE highest-impact recommendation
        to improve the candidate's ATS score.

        Analyze:

        - Missing skills
        - Weak matches
        - Resume evidence gaps
        - Project alignment
        - Keyword optimization opportunities


        Choose only the most important improvement.

        Recommendation categories:

        1. skill_gap
        2. resume_improvement
        3. project_improvement
        4. keyword_optimization
        5. experience_alignment


        Rules:

        - Return exactly ONE recommendation.
        - Do not return a list.
        - Do not return multiple recommendations.
        - Do not invent skills or experience.
        - Be specific and actionable.

        {format_instructions}

        Return only JSON.
        """

    RECOMMENDATION_USER_PROMPT = """

        ATS Evaluation:

        <ATS>
        {ats_result}
        </ATS>


        Resume:

        <RESUME>
        {resume_data}
        </RESUME>


        Job:

        <JOB>
        {job_data}
        </JOB>

        Generate improvement recommendations.

        """
    
    parser = PydanticOutputParser(pydantic_object=Recommendation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system" , RECOMMENDATION_SYSTEM_PROMPT),
        ("human", RECOMMENDATION_USER_PROMPT)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "ats_result": ats_result,
        "resume_data": resume_data,
        "job_data": jd_data
    })
    
    return response