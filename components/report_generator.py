from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from schemas.resume_analyze_state_schema import FinalResumeAnalysisReport

def generate_final_report(llm, candidate_data, job_data, ats_data, recommendation_data):

    SYSTEM_PROMPT = """

You are an expert AI Resume Analyzer.

Generate a professional recruitment-style resume analysis report.

The report should summarize:

- Candidate profile
- ATS compatibility
- Skill alignment
- Experience match
- Project relevance
- Skill gaps
- Improvement suggestions
- Hiring recommendation


Rules:

- Be factual.
- Use only provided information.
- Do not invent missing experience.
- Keep assessment professional.
- ATS score must remain unchanged.


{format_instructions}

Return only JSON.

"""

    USER_PROMPT = """

Candidate Information:

<CANDIDATE>
{candidate_data}
</CANDIDATE>


Job Information:

<JOB>
{job_data}
</JOB>


ATS Evaluation:

<ATS>
{ats_data}
</ATS>


Recommendations:

<RECOMMENDATIONS>
{recommendation_data}
</RECOMMENDATIONS>

Generate final report.

"""

    parser = PydanticOutputParser(pydantic_object=FinalResumeAnalysisReport)

    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", USER_PROMPT)]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser

    return chain.invoke(
        {
            "candidate_data": candidate_data,
            "job_data": job_data,
            "ats_data": ats_data,
            "recommendation_data": recommendation_data,
        }
    )
