from typing import TypedDict, Literal

Stage = Literal[
    "collecting_requirements",
    "prd",
    "trd",
    "architecture",
    "coding",
    "reviewing",
    "awaiting_user",
    "done",
    "failed",
]


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class BuildState(TypedDict):
    user_token: str
    session_id: str
    stage: Stage
    conversation: list[Message]
    requirements: dict
    requirements_complete: bool
    prd: str
    trd: str
    architecture: dict
    generated_files: dict[str, str]
    review_notes: list[str]
    review_approved: bool
    pending_question: str | None
    loop_count: int
    error: str | None


def new_state(user_token: str, session_id: str) -> BuildState:
    return BuildState(
        user_token=user_token,
        session_id=session_id,
        stage="collecting_requirements",
        conversation=[],
        requirements={},
        requirements_complete=False,
        prd="",
        trd="",
        architecture={},
        generated_files={},
        review_notes=[],
        review_approved=False,
        pending_question=None,
        loop_count=0,
        error=None,
    )
