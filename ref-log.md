# Assignment 2 | Reflection Document
Multi-agent Travel Planning Application in Streamlit 

## What I Learned from Implementing a Multi-Agent Workflow

I learned the importance of separating the two agents. This allowed the first agent to create the travel itinerary and the second to judge it and improve it. For the reviewer agent, I learned about Tavily, which is a tool for Internet searches. 

The main key learning takeaway for me was the need for collaborative AI design. It was essential to have the planner agent disconnected from the Internet while the second agent was connected. This agent interconnection enabled improved travel results, based on facts, with extremely impressive deltas. 

## Challenges I Faced and How I Addressed Them

The main challenge was striking the correct balance between detail and conciseness. While the traveller needs a day-by-day breakdown, it also needs to be short enough to be accomplishable. 

The second challenge was accessibility. I emphasized in my prompt the need for accessibility. For example, if a traveller has kids, make sure the activities are suitable for them. Or, if a traveller has a disability, then suggest ideas that take that into account. 

## Creative Design Choices

As a design choice, I added a "cite your sources" clause so it is easier for the traveller to verify any information. I also included that the budget is in USD, unless stated otherwise. 

Most importantly, in the prompt design, I include that the agent is an expert, so it better embodies those characteristics. 

## External Tools and GenAI Assistance

OpenAI and Tavily were used. The first was used for the agents. The second was used for internet searching. LLMs were used to debug. 
