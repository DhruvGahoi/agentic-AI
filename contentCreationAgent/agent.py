from google.adk.agents import ParallelAgent, LlmAgent

GEMINI_MODEL = "gemini-2.5-flash"

blog_agent = LlmAgent(
    name="BlogAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a blogging expert. Suggest an engaging blog outline and content ideas
    on the topic based on user query.

    Output format:
    - Suggested title
    - Blog Outline (3 - 5 headings)
    - Key Points under each heading
    """,
    output_key="blog_content"
)

youtube_agent = LlmAgent(
    name="YoutubeAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a Youtube content strategist. Create:
    1. A catchy title.
    2. A video script (short, conversational, less than 2 min read)
    3. A Youtube description (SEO-friendly, with 3 - 4 keywords)
    """,
    output_key="youtube_content"
)

instagram_agent = LlmAgent(
    name="InstagramAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a social media content creator. Suggest 3 Instagram Reel ideas for the topic.
    For each reel, provide:
    - Hook line
    - Quick script idea
    - Suggested hashtags
    """,
    output_key="instagram_content"
)

content_creator_agent = ParallelAgent(
    name="ContentCreatorAgent",
    sub_agents=[blog_agent, youtube_agent, instagram_agent],
    description="""
    Generate blog ideas, Youtube video content, and Instagram reel ideas in parallel.
    """
)

root_agent = content_creator_agent
