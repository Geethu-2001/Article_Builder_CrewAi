import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM

# Set your Gemini AI API key and model
gemini_api_key = 'enter your api key'
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the LLM instance
my_llm = LLM(
    api_key=gemini_api_key,  # Replace with your actual API key
    model="gemini/gemini-pro"
)

# Define your agents with roles, goals, and backstory
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}. "
              "You collect information that helps the "
              "audience learn something and make informed decisions. "
              "Your work is the basis for the Content Writer to write an article on this topic.",
    llm=my_llm,  # Use the LLM instance here
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're writing a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of the Content Planner, "
              "who provides an outline and relevant context about the topic. "
              "You follow the main objectives and direction of the outline provided by the Content Planner.",
    llm=my_llm,  # Use the LLM instance here
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory="You are an editor who reviews blog posts from the Content Writer to ensure they follow journalistic best practices, provide balanced viewpoints, "
              "and avoid controversial topics when possible.",
    llm=my_llm,  # Use the LLM instance here
    allow_delegation=False,
    verbose=True
)

# Define your tasks with descriptions, expected output, and the associated agent
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
        "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
        "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
        "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
                    "with an outline, audience analysis, SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
        "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
        "4. Proofread for grammatical errors and alignment with the brand's voice."
    ),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, each section should have 2 or 3 paragraphs.",
    agent=editor
)

# Create the crew with your agents and tasks
article_crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    manager_llm=False,
    verbose=True
)

# Streamlit interface for user input
st.title('Content Creation for Blog Articles')
st.write("Enter the topic for your blog article:")

# Input for the topic from the user
topic = st.text_input("Topic", "Artificial Intelligence")

if st.button('Generate Article'):
    # Run the crew with the topic
    result = article_crew.kickoff(inputs={"topic": topic})

    
    # Display the results as markdown on the Streamlit page
    st.markdown(result)

