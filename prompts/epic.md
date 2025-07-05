This plan is designed to deliver value incrementally, starting with a solid foundation and building features on top, while keeping tickets small and focused.

---

### **Jira Epics & Tickets: Vibe AI Newsletter - Phase 1 (MVP)**

---

### **Epic 1: VAI-E1 - MVP Core Content Sourcing Engine**

**Goal:** To build a reliable, automated, and ethically compliant system that can ingest news articles and research papers from the web and store them for processing.

---

**Ticket VAI-1: [Foundation] Build a basic web scraper for a single, static news source**

*   **Background:** This is the foundational component of our content pipeline. We need to prove we can reliably extract text content from a target website. We will start with one high-value, structurally simple source like a well-known tech blog.
*   **Acceptance Criteria:**
    *   A script can be run that takes a URL from the target source as input.
    *   The script successfully extracts the main article title and body text.
    *   The extracted content is saved to a local file (e.g., JSON) with `url`, `title`, and `content` fields.
    *   The script handles basic network errors gracefully.
*   **Implementation Suggestions:**
    *   **Language:** Python
    *   **Libraries:** `requests` for fetching the page, `BeautifulSoup4` for parsing HTML. Avoid more complex tools like Selenium for this initial task to keep it simple.
    *   Ref: Tech Spike Sec 2.1 (Code-based solutions).

---

**Ticket VAI-2: Integrate arXiv API client to fetch research papers**

*   **Background:** The "Research Spotlight" section is a key feature. Using the official arXiv API is more reliable and ethical than scraping their website. This ticket establishes our first non-scraping data source.
*   **Acceptance Criteria:**
    *   A script can fetch the latest 10 papers from the `cs.AI` category on arXiv.
    *   The script extracts the `id`, `title`, `authors`, and `summary` for each paper.
    *   The extracted data is saved in a structured format (JSON).
    *   The client respects the API's rate-limiting guidelines.
*   **Implementation Suggestions:**
    *   **Language:** Python
    *   **Libraries:** The official `arxiv` PyPI package is recommended as it handles pagination and query building.
    *   Ref: Tech Spike Sec 2.2.

---

**Ticket VAI-3: Implement a `robots.txt` compliance layer for the scraper**

*   **Background:** Ethical scraping is a non-negotiable requirement. Before we scrape any URL, we must programmatically check if we are allowed to. This ticket builds that guardrail.
*   **Acceptance Criteria:**
    *   Given a URL, the system can fetch and parse the corresponding `robots.txt` file.
    *   A function `can_fetch(url)` returns `True` or `False` based on the `robots.txt` rules for our user-agent.
    *   The scraper from VAI-1 now calls `can_fetch()` before making a request and halts if `False`.
*   **Implementation Suggestions:**
    *   **Libraries:** Python's built-in `urllib.robotparser` is a good starting point.
    *   **Architecture:** This should be a utility function or class that can be used by all future scraping jobs.
    *   Ref: Tech Spike Sec 7.2.

---

**Ticket VAI-4: Persist ingested content to a staging database**

*   **Background:** We need a centralized place to store all raw content before it enters the AI processing pipeline. A simple, scalable NoSQL database is ideal for this.
*   **Acceptance Criteria:**
    *   A new record can be written to a cloud database (e.g., DynamoDB) containing the scraped article or arXiv paper data.
    *   The database schema includes fields for `source_url` (as a unique key), `content`, `title`, `source_type` (e.g., 'news', 'arxiv'), and a `status` field (e.g., 'ingested').
    *   The scripts from VAI-1 and VAI-2 are updated to write their output to this database instead of a local file.
*   **Implementation Suggestions:**
    *   **Database:** AWS DynamoDB is recommended for its serverless nature and alignment with our proposed architecture.
    *   **Libraries:** `boto3` for Python if using AWS.
    *   Ref: Tech Spike Sec 4.1, 4.2.

---

### **Epic 2: VAI-E2 - MVP AI Content Processing Pipeline**

**Goal:** To transform raw ingested content into high-quality, categorized summaries ready for publication, using a RAG architecture.

---

**Ticket VAI-5: [Foundation] Implement embedding pipeline and vector store**

*   **Background:** Retrieval Augmented Generation (RAG) is core to our strategy for accuracy and cost control. The first step is to embed our ingested content and store it in a vector database for efficient retrieval.
*   **Acceptance Criteria:**
    *   When new content is added to the staging database (from VAI-4), a process is triggered.
    *   The process chunks the text content into smaller, manageable pieces.
    *   Each chunk is converted into a vector embedding using an embedding model API (e.g., OpenAI `text-embedding-ada-002`).
    *   The chunks and their corresponding embeddings are stored in a vector database.
*   **Implementation Suggestions:**
    *   **Vector DB:** Weaviate or LlamaIndex are strong candidates. Start with a cloud-hosted version to speed up development.
    *   **Frameworks:** LangChain's `RecursiveCharacterTextSplitter` and embedding wrappers can simplify this process.
    *   Ref: Tech Spike Sec 3.3 (RAG) and 4.2.

---

**Ticket VAI-6: Create a text summarization function for a single content piece**

*   **Background:** This is the core value proposition of the newsletter. We need a function that can take a piece of content and generate a concise summary using a powerful LLM.
*   **Acceptance Criteria:**
    *   A function takes a content ID as input.
    *   It retrieves the relevant text chunks from the vector database (from VAI-5).
    *   It sends these chunks as context to an LLM (e.g., GPT-4) with a specific summarization prompt.
    *   It returns a coherent, "bite-sized" summary of the content.
*   **Implementation Suggestions:**
    *   **LLM API:** OpenAI or Anthropic Claude API.
    *   **Prompting:** The prompt should be version-controlled and specify the desired tone ("for developers," "concise," "high-signal"). Start with a simple "stuff" method for documents that fit in the context window.
    *   Ref: Tech Spike Sec 3.1.

---

**Ticket VAI-7: Implement a "MapReduce" chain for long-document summarization**

*   **Background:** Many research papers and in-depth articles will exceed the LLM's context window. We need a strategy to summarize these long documents effectively.
*   **Acceptance Criteria:**
    *   The summarization function from VAI-6 now detects if the source document is too long for a single API call.
    *   If too long, it summarizes each chunk individually ("map" step).
    *   It then combines the chunk summaries and sends them for a final summarization ("reduce" step).
    *   A final, coherent summary of the entire document is produced.
*   **Implementation Suggestions:**
    *   **Frameworks:** LangChain provides a built-in `MapReduceDocumentsChain` that is perfect for this.
    *   **Cost:** Be mindful that this process is more token-intensive. Log the token usage for each run.
    *   Ref: Tech Spike Sec 3.2.

---

**Ticket VAI-8: Implement a "human-in-the-loop" review and approval step**

*   **Background:** To ensure quality and mitigate legal risks (copyright), all AI-generated content must be reviewed by a human before publication. This ticket creates a simple mechanism for that.
*   **Acceptance Criteria:**
    *   A simple script or UI lists all content pieces with a status of 'summarized'.
    *   The interface displays the original source link, the generated summary, and the assigned category.
    *   A user can approve or reject the content.
    *   Approving changes the content's status to 'approved'. Rejecting changes it to 'rejected'.
*   **Implementation Suggestions:**
    *   **Interface:** This can be as simple as a command-line script for the MVP to avoid UI development overhead.
    *   **Database:** This will update the `status` field in the DynamoDB table from VAI-4.
    *   Ref: Tech Spike Sec 7.1.

---

### **Epic 3: VAI-E3 - MVP Newsletter Delivery & Presentation**

**Goal:** To assemble the approved, AI-curated content into a visually appealing, mobile-first newsletter and deliver it via a third-party platform.

---

**Ticket VAI-9: [Foundation] Set up Beehiiv account and a basic mobile-first template**

*   **Background:** The newsletter's presentation is key to our brand. We need to set up our chosen platform and create a reusable template that reflects our "vibecoder" aesthetic and works flawlessly on mobile.
*   **Acceptance Criteria:**
    *   A Beehiiv account is created and configured.
    *   A new email template is created within Beehiiv.
    *   The template uses a single-column layout, legible fonts (e.g., >=14px body), and has placeholders for our content sections (`Top Storylines`, `Research Spotlight`, etc.).
    *   The template renders correctly when tested on both desktop (Gmail) and mobile (iOS Mail, Gmail App) clients.
*   **Implementation Suggestions:**
    *   Use Beehiiv's visual editor. Focus on structure and mobile responsiveness over complex design elements for now.
    *   Follow the best practices outlined in the research.
    *   Ref: Tech Spike Sec 5.1, 5.3, 5.4.

---

**Ticket VAI-10: Develop a script to push approved content to the Beehiiv API**

*   **Background:** To achieve full automation, our backend system needs to programmatically create a new newsletter draft with our curated content.
*   **Acceptance Criteria:**
    *   A script fetches all content from our database with a status of 'approved'.
    *   It formats the content (summaries, links, categories) into the HTML structure required by our Beehiiv template.
    *   It makes a successful API call to Beehiiv to create a new post (draft) with the formatted content.
    *   The status of the pushed content in our database is updated to 'published'.
*   **Implementation Suggestions:**
    *   **API:** Use the official Beehiiv API.
    *   **Formatting:** Use a templating engine like Jinja2 in Python to inject the content into the HTML template structure.
    *   Ref: Tech Spike Sec 5.1 (Beehiiv API capabilities).

---

**Ticket VAI-11: Implement a scheduler to trigger the end-to-end pipeline**

*   **Background:** The entire process, from sourcing to publishing the draft, should run on a regular schedule (e.g., weekly) without manual intervention.
*   **Acceptance Criteria:**
    *   A scheduler is configured to trigger the content sourcing jobs (scraping, arXiv).
    *   Upon completion, the processing jobs (embedding, summarization) are triggered.
    *   Finally, the newsletter draft creation job (VAI-10) is run.
    *   The entire pipeline runs automatically once per week.
*   **Implementation Suggestions:**
    *   **Scheduler:** AWS EventBridge (CloudWatch Events) is a perfect serverless option to trigger AWS Lambda functions on a cron schedule.
    *   **Orchestration:** For MVP, a simple sequence of events is fine. For Phase 2, this will evolve into a more robust orchestration system (e.g., Step Functions or an AI Agent framework).
    *   Ref: Tech Spike Sec 4.1.