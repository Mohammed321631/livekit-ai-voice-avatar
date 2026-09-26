import os

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession
from livekit.plugins import google, tavus


load_dotenv(".env")


class VoiceAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a friendly real-time AI voice assistant. "
                "Answer clearly, naturally, and briefly."
            )
        )


server = AgentServer()


@server.rtc_session(agent_name="voice-avatar-agent")
async def voice_avatar_agent(ctx: agents.JobContext):

    session = AgentSession(
      llm=google.realtime.RealtimeModel(
    model="gemini-2.5-flash-native-audio-preview-09-2025",
    voice="Puck",
)
        )    

    avatar = tavus.AvatarSession(
        face_id=os.getenv("TAVUS_FACE_ID"),
    )

    await avatar.start(
        session,
        room=ctx.room,
    )

    await session.start(
        room=ctx.room,
        agent=VoiceAssistant(),
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
    
