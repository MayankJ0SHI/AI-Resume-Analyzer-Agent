#Resume Processing Node
from components.resume_processing import load_pdf_document
from schemas.resume_analyze_state_schema import ResumeAnalyzeState

def resume_processor_node(state: ResumeAnalyzeState):
    print("\n === Resume Processor Node Executed ===")
    result = load_pdf_document(state.resume_path)
    return {
        "resume_content": result
    }
