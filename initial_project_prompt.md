Build a Streamlit web application that acts as a smart assistant chatbot powered by the Gemini 2.0 Flash model via the Google Generative AI API. The existing `app.py` already provides a basic Streamlit setup for configuring API keys for the MCP servers.

The assistant must integrate with the following MCP servers via HTTP wrappers:

*   **Qdrant MCP Server** for persistent vector memory storage and retrieval.
*   **Email MCP Server** to send reminder and notification emails to users. (Note: The `servers/mcp-server-email/` directory already exists in the project.)
*   **Scrapeless MCP Server** to perform real-time web searches and retrieve live data. (Note: The `servers/scrapeless-mcp-server/` directory already exists in the project.)
*   **MongoDB MCP Server** to access the MongoDB instance for data persistence. (Note: The project's Docker configuration already includes a MongoDB instance.)

Design the system with a strong emphasis on composition over inheritance:

*   Wrap each MCP service as an independent HTTP client class with clear, minimal interfaces.
*   Inject these clients into a central assistant service that orchestrates memory, email, search, and database capabilities.
*   Abstract a middleware layer between Gemini and the MCP clients to intercept and modify prompts or AI outputs, enabling fine-grained control over interactions and tool usage.

Implement a scheduler backed by a simple database (e.g., MongoDB via its MCP) to create, persist, and trigger reminder jobs that the assistant can execute at user-specified times, such as sending emails or running searches.

The app should have a clean Streamlit UI for:

*   Chatting with the assistant with context memory via Qdrant.
*   Creating and managing reminders or jobs.
*   Viewing logs or outputs of scheduled tasks.

Begin by planning the project:

*   Create a system specification document outlining the overall architecture, technologies, and integration details.
*   Create a tasks and user stories document listing the high-level features and user interactions required.
*   For the current feature or task, create a current task document that breaks it down into multiple subtasks or user stories, marking completed items as work progresses.

Save all planning and specification documents as markdown or text files in a `memory-bank` directory.

After planning, begin implementing the project incrementally according to the tasks and system specification documents, updating the current task document as subtasks are completed.

The architecture must support easy extension by adding new MCP clients or AI tools without major rewrites.
