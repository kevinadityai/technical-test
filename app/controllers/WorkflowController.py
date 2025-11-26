from langgraph.graph import StateGraph, END


class WorkflowController:
    def __init__(self):
        pass

    def _create_workflow(self):
        try:
            workflow = StateGraph(dict)
            workflow.add_node("retrieve", simple_retrieve)
            workflow.add_node("answer", simple_answer)
            workflow.set_entry_point("retrieve")
            workflow.add_edge("retrieve", "answer")
            workflow.add_edge("answer", END)
            chain = workflow.compile()

            return chain

        except Exception as e:
            raise e