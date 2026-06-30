# AI Engineering Use Cases Library

> Real-world use cases mapped to your roadmap phases. Each use case shows the problem, AI solution, architecture, and the exact modules/phases it tests.

## How To Use

1. Read one use case per day
2. Identify: "Which Phase/modules does this use?"
3. Explain the solution out loud
4. Note interview questions that could arise

---

## Use Case 1: Customer Support Ticket Classification + Auto-Response

**Industry:** E-commerce / SaaS

**Problem:** A company receives 5,000 support tickets/day. Agents spend 80% of time on tier-1 issues (password reset, order status, refund status).

**AI Solution:**
- Classifier agent categorizes ticket: (password, order, refund, technical, other)
- For tier-1 issues, RAG over help articles generates a draft response
- For refunds over $500, route to human with AI-generated summary
- Agent tracks resolution success and updates knowledge base

**Architecture:**
```
Email/chat → Classifier → Router → [RAG agent] → Draft response → Human review (if needed)
                                    → [Human agent] → Escalation
```

**Modules Used:** M4 (Prompt Engineering - classification), M6 (RAG - knowledge base), M7 (Agents - routing), M8 (Tool Calling - ticket API), M11 (Evaluation - resolution rate)

**Interview Angle:**
- "How would you measure if this system is better than humans alone?"
- "What happens when the classifier is wrong?"
- "How do you handle edge cases where the knowledge base has no answer?"

---

## Use Case 2: Legal Contract Analysis Platform

**Industry:** Legal / Insurance

**Problem:** Lawyers manually review 100-page contracts for risky clauses. This takes hours per contract.

**AI Solution:**
- Document ingestion pipeline: OCR scanned contracts, extract text, structure-aware chunking by clause (indemnification, liability, termination, etc.)
- Embed and index clauses
- Query: "Highlight all clauses that shift liability to party A"
- RAG returns clause text + position + risk score
- Agent generates summary of key risks

**Architecture:**
```
PDF → OCR → Structure-aware chunking (by clause) → Embed → Vector DB
Lawyer query → Router → Retrieve relevant clauses → Rerank → LLM summarizes risks → Citation
```

**Modules Used:** M2 (Async doc processing), M5 (Embeddings), M6 (Advanced chunking + retrieval), M8 (Tool Calling - extract/flag tools), M11 (Evaluation - precision of risk detection), M13 (Security - confidential docs)

**Interview Angle:**
- "How do you chunk legal documents differently from general text?"
- "What if the contract uses non-standard clause names?"
- "How do you ensure zero data leakage between law firms (multi-tenancy)?"

---

## Use Case 3: Personalized Learning Assistant

**Industry:** EdTech

**Problem:** A learning platform has 100K+ courses. Students have different backgrounds, learning speeds, and goals. One-size-fits-all courses have low completion rates.

**AI Solution:**
- Memory system tracks each student's knowledge state, learning preferences, and progress
- Agent adapts content difficulty, suggests next topics, generates practice questions
- RAG over course materials to answer specific questions with citations
- Evaluation: pre/post test scores, engagement metrics

**Architecture:**
```
Student interaction → Memory (knowledge graph + preferences) → Agent → Content selection
                                                                        → Question generation
                                                                        → RAG over course materials
```

**Modules Used:** M3 (LLM Fundamentals), M4 (Prompt Engineering - question generation), M6 (RAG over content), M7 (Agents - adaptive routing), M10 (Memory - student state), M11 (Evaluation - learning outcomes)

**Interview Angle:**
- "How does the system handle a student asking about a topic they haven't studied yet?"
- "How do you prevent the AI from giving answers instead of teaching?"
- "How would you evaluate if learning actually improved?"

---

## Use Case 4: Real-Time Fraud Detection Agent

**Industry:** FinTech

**Problem:** Credit card fraud attempts need detection in < 100ms. Traditional rules engines miss novel fraud patterns.

**AI Solution:**
- Agent monitors transaction streams in real-time
- Tool calls to: transaction history API, fraud scoring model, customer profile DB
- Agent combines rules (amount > threshold → flag) with LLM reasoning (unusual pattern detection)
- High-confidence fraud → block + notify customer
- Medium confidence → hold + human review
- Low confidence → allow, log for model improvement

**Architecture:**
```
Transaction stream → Agent → Tool 1: History API
                           → Tool 2: Fraud model
                           → Tool 3: Profile DB
                           → Reasoning → [Block | Hold | Allow]
```

**Modules Used:** M7 (Agents - real-time decision), M8 (Tool Calling - APIs), M11 (Evaluation - false positive/negative rates), M12 (Observability - latency, decisions), M13 (Security - data protection)

**Interview Angle:**
- "How do you handle latency requirements when LLM inference takes 500ms+?"
- "What's your strategy for false positives vs false negatives?"
- "How do you improve the system over time from labeled fraud cases?"

---

## Use Case 5: Enterprise Knowledge Management with Chat

**Industry:** Any large enterprise

**Problem:** A 10,000-employee company has knowledge scattered across Confluence, SharePoint, Slack, email, and internal wikis. Employees waste 2+ hours/day searching.

**AI Solution:**
- Ingestion pipeline: crawl all sources (Confluence API, SharePoint, Slack export) → normalize → chunk → embed
- RAG with hybrid search (BM25 for exact terms, vector for semantics)
- Citations with source links, confidence scores
- Agent can also query internal APIs for real-time data (PTO balance, IT ticket status)
- Memory stores per-user preferences (role, department, document access level)

**Architecture:**
```
Crawlers → Document processing → Embed → Vector DB
Employee query → Auth (tenant_id + role) → RAG + Agent → Response with citations + API data
```

**Modules Used:** M2 (FastAPI), M5 (Embeddings), M6 (RAG + Hybrid search), M7 (Agent for API calls), M8 (Tool Calling), M10 (Memory), M13 (Security - access control), M21 (Enterprise - audit, multi-tenancy)

**Interview Angle:**
- "How do you handle cross-source deduplication?"
- "How do you ensure employees only see documents they're authorized to see?"
- "What happens when the Confluence API is down?"

---

## Use Case 6: AI-Powered Code Review Assistant

**Industry:** Software Development

**Problem:** Code reviews take 2-4 hours/day per senior engineer. Simple issues (style, test coverage, documentation) consume time that should go to architecture review.

**AI Solution:**
- Code RAG: index the entire repo (functions, classes, APIs, docs) into chunks
- Agent receives a PR diff
- Tool calls: git log (history), test runner (coverage), linting (style)
- Agent evaluates: code style, test coverage, API compatibility, documentation updates
- Generates review comments with code citations
- Suggests fixes with confidence levels

**Architecture:**
```
PR → Agent → Tool: git history
            → Tool: test runner
            → Tool: linter
            → Code RAG over repo
            → Generate review → [Auto-approve (style only) | Suggest changes | Require human review]
```

**Modules Used:** M6 (RAG over code), M7 (Agents - review workflow), M8 (Tool Calling - git, test, lint), M11 (Evaluation - comment accuracy), M12 (Observability - PR cycle time improvement)

**Interview Angle:**
- "How do you chunk code files differently from natural language?"
- "How do you prevent the AI from suggesting breaking changes?"
- "What metrics prove the system saves engineer time without reducing quality?"

---

## Use Case 7: Healthcare Clinical Note Summarization

**Industry:** Healthcare

**Problem:** Doctors spend 2+ hours/day on clinical documentation. Notes contain structured data (vitals, labs) and unstructured observations.

**AI Solution:**
- Document processing pipeline for clinical notes (handwritten via OCR, typed)
- PII/PHI scrubbing at ingestion (HIPAA compliance)
- RAG over past patient history for context
- LLM generates: SOAP note (Subjective, Objective, Assessment, Plan) from doctor's dictation
- Structured output (JSON) integrates with EHR system
- Audit trail: every note has a trace from ingestion to output

**Architecture:**
```
Doctor dictation → PII scrub → LLM → Structured SOAP → EHR integration
Patient history DB → RAG for context → Note generation → Audit log
```

**Modules Used:** M2 (Async), M5 (Embeddings for patient history), M6 (RAG), M8 (Tool Calling - EHR API), M13 (Security - HIPAA, PII), M21 (Enterprise - audit trail)

**Interview Angle:**
- "How do you handle PHI while using third-party LLM APIs?"
- "How do you verify the AI didn't hallucinate patient data?"
- "How would you handle multi-language clinical notes?"

---

## Use Case 8: Autonomous Email Response Agent

**Industry:** B2B Sales / Customer Success

**Problem:** A sales team receives 500+ emails/day (inquiries, meeting requests, follow-ups). Manual response time averages 4+ hours.

**AI Solution:**
- Agent monitors inbox via API
- Classifier: inquiry | meeting request | complaint | spam
- For inquiries: RAG over product docs → draft response
- For meeting requests: tool calls calendar API → find slots → propose times
- For complaints: triage severity → draft acknowledgment → route to appropriate team
- Memory: remembers past interactions with each contact
- Human loop: all outbound emails require human review first (for compliance)

**Architecture:**
```
Email → Agent → Classifier → [Inquiry: RAG + draft]
                            → [Meeting: Calendar tool + propose]
                            → [Complaint: Severity + route]
                            → Human review queue → Send
```

**Modules Used:** M6 (RAG over product docs), M7 (Agents), M8 (Tool Calling - calendar, email APIs), M10 (Memory - contact history), M13 (Security - email access control), M21 (Enterprise - compliance)

**Interview Angle:**
- "How do you prevent the agent from sending an email with incorrect information?"
- "What if the agent drafts a response that violates company policy?"
- "How do you measure: does this save time or create more work for humans?"

---

## Use Case 9: Supply Chain Anomaly Detection + Response

**Industry:** Manufacturing / Logistics

**Problem:** A manufacturer has 10,000+ SKUs from 500 suppliers. Supply chain disruptions (delays, quality issues, price changes) are detected late, causing production delays.

**AI Solution:**
- Agent monitors supplier data feeds, shipping updates, quality reports
- RAG over historical disruptions and resolution patterns
- When anomaly detected: classify severity, root cause analysis using tools (supplier DB, shipping API, weather API)
- Generate response plan with recommendations
- High severity → human approval before execution
- Memory stores resolution patterns for future use

**Architecture:**
```
Data feeds → Agent → Anomaly detection → Tool calls (supplier, shipping, weather)
                                          → RAG over past resolutions
                                          → Response plan → [Auto-respond (low) | Human approve (high)]
```

**Modules Used:** M7 (Agents - monitoring + response), M6 (RAG over historical data), M8 (Tool Calling - APIs), M10 (Memory - resolution patterns), M11 (Evaluation - response accuracy), M12 (Observability - detection latency)

**Interview Angle:**
- "How do you handle false positives (alert fatigue)?"
- "How do you combine real-time data with historical patterns?"
- "What's your strategy for supplier-specific custom logic vs general patterns?"

---

## Use Case 10: Multimodal Product Catalog Search

**Industry:** Retail / E-commerce

**Problem:** A retailer's website search returns poor results for queries like "red dress with floral pattern like the one in this image" or "show me products similar to this but cheaper."

**AI Solution:**
- Multimodal embeddings: product images + descriptions → joint embedding space
- Search query can be text, image, or both
- RAG over product specs, reviews, inventory
- Agent provides recommendations with reasons, comparisons
- Feedback loop: clicks, purchases, returns → improve embeddings

**Architecture:**
```
Product catalog (images + text) → Multimodal embeddings → Vector DB
User query (text/image) → Multimodal search → RAG + Agent → Recommendations
User feedback → Training data → Embedding refresh
```

**Modules Used:** M5 (Embeddings - multimodal), M6 (RAG over catalog), M7 (Agent - recommendations), M14 (Multimodal AI), M20 (Cost - embedding optimization)

**Interview Angle:**
- "How do you align text and image embeddings?"
- "How do you handle new products with no purchase history?"
- "How would you evaluate: are recommendations actually leading to more purchases?"

---

## Use Case 11: Automated Regulatory Compliance Agent

**Industry:** Finance / Insurance

**Problem:** Financial regulations change frequently. Compliance teams must manually review policies, identify gaps, and update documentation. This is slow and error-prone.

**AI Solution:**
- MCP server connects to regulatory databases (SEC, FINRA, GDPR register)
- Agent monitors regulation changes via RSS/webhook
- When new regulation detected: extract requirements using structured output
- RAG over current internal policies to identify gaps
- Agent generates: gap analysis report, recommended policy changes, compliance risk score
- Human approval required before any policy change

**Architecture:**
```
Regulation source → MCP server (monitor tool) → Agent → Extract requirements
                                                       → RAG over policies → Gap analysis
                                                       → Report → Human approval → Policy update
```

**Modules Used:** M6 (RAG over policies), M7 (Agents - monitoring + analysis), M8 (Tool Calling), M9 (MCP - regulation connectors), M11 (Evaluation - gap detection accuracy), M21 (Enterprise - audit trail)

**Interview Angle:**
- "How do you handle ambiguous regulations that require legal interpretation?"
- "How do you prevent the agent from making changes based on incorrect regulation parsing?"
- "What's the MCP architecture for connecting to multiple regulatory data sources?"

---

## Use Case 12: AI-Powered Recruitment Assistant

**Industry:** HR / Recruitment

**Problem:** Recruiters spend 60% of time screening resumes, scheduling interviews, and sending follow-ups.

**AI Solution:**
- Document processing: parse resumes (PDF, DOCX, LinkedIn exports) → structured profile
- RAG over job descriptions to match requirements
- Agent: screens candidate → generates summary + fit score
- Tool calls: calendar API for interview scheduling, email for communication
- Memory: stores candidate preferences, interview feedback
- Human loop: shortlisted candidates reviewed by recruiter before proceeding

**Architecture:**
```
Resume → Document processing → Structured profile → Vector DB
Job description → RAG matching → Agent → Screen → Summary + Score
                                          → Schedule interview (tool)
                                          → Send email (tool)
                                          → Human review gate
```

**Modules Used:** M2 (Async ingestion), M6 (RAG - matching), M7 (Agents - workflow), M8 (Tool Calling - calendar, email), M10 (Memory - candidate history), M13 (Security - PII in resumes)

**Interview Angle:**
- "How do you prevent bias in AI screening?"
- "What if the resume parser misses important information?"
- "How do you handle candidates who apply for multiple roles?"

---

## Use Case 13: Real-Time Meeting Assistant

**Industry:** Any

**Problem:** During meetings, participants miss action items, decisions are forgotten, and follow-ups are inconsistent.

**AI Solution:**
- Real-time transcription (speech-to-text)
- Agent monitors conversation for: decisions, action items, questions, deadlines
- RAG over project context to provide relevant info during meeting
- After meeting: generate minutes, assigned task list, calendar events
- Memory: track decisions across meetings for continuity

**Architecture:**
```
Meeting audio → STT → Agent → Extract: decisions, actions, questions
                              → RAG: project context
                              → Post-meeting: minutes, tasks, calendar events
                              → Memory: cross-meeting continuity
```

**Modules Used:** M7 (Agents - real-time processing), M8 (Tool Calling - calendar, task tools), M10 (Memory - decisions across meetings), M14 (Multimodal - audio), M20 (Cost - streaming transcription)

**Interview Angle:**
- "How do you handle multiple people speaking simultaneously?"
- "How do you distinguish between a decision and a suggestion?"
- "How would you evaluate the accuracy of extracted action items?"

---

## Use Case 14: AI Data Quality Monitor

**Industry:** Data Engineering / Analytics

**Problem:** Data pipelines produce dirty data: missing values, duplicates, outliers, schema changes. Detecting these manually is reactive.

**AI Solution:**
- Agent monitors data streams against expected schema + patterns
- RAG over data dictionary and business rules
- When anomaly detected: classify type, severity, root cause
- Tool calls: data catalog API, lineage tracker, data quality score
- Generates: incident report + fix recommendation + data quality trend
- Auto-fix low-risk issues (type casting, dedup); escalate high-risk (data loss, PII leak)

**Architecture:**
```
Data streams → Agent → Schema validation → Anomaly detection
                                            → RAG over business rules
                                            → Tool calls (catalog, lineage)
                                            → [Auto-fix | Escalate]
```

**Modules Used:** M6 (RAG over rules), M7 (Agents - monitoring), M8 (Tool Calling - APIs), M11 (Evaluation - detection rate), M12 (Observability - alert latency), M21 (Enterprise - data lineage)

**Interview Angle:**
- "How do you distinguish between a real data quality issue and a temporary spike?"
- "How does the agent learn new data quality patterns?"
- "How do you prevent the monitoring agent itself from creating noise?"

---

## Use Case 15: Multi-Channel Customer Communication Hub

**Industry:** Customer Experience / CX

**Problem:** Customers interact via chat, email, phone, social media. Each channel is handled separately, losing context.

**AI Solution:**
- All channels → MCP connectors → unified message bus
- Agent maintains cross-channel conversation state via memory
- RAG over knowledge base, past interactions, customer profile
- Agent provides consistent responses regardless of channel
- Handoff: if a customer switches from chat to email, the agent continues the same conversation
- Human escalation if needed, with full context

**Architecture:**
```
Chat → MCP connector
Email → MCP connector     → Unified Agent → RAG → Response
Phone → MCP connector                    → Memory (cross-channel)
Social → MCP connector                   → Human handoff (with context)
```

**Modules Used:** M7 (Agents - unified), M8 (Tool Calling), M9 (MCP - channel connectors), M10 (Memory - cross-channel), M21 (Enterprise - audit)

**Interview Angle:**
- "How do you maintain context when a customer interacts across different channels?"
- "What happens when the customer says the same thing in chat and email?"
- "How do you measure: is cross-channel context actually improving satisfaction?"

---

## Use Cases Per Phase Map

| Phase | Use Cases |
|-------|-----------|
| Phase 1 (Foundation) | All (underlying tech) |
| Phase 2 (RAG) | 1, 2, 3, 5, 7, 8, 9, 12, 13 |
| Phase 3 (Agents) | 1, 4, 5, 6, 8, 9, 11, 12, 13, 15 |
| Phase 4 (Production) | 4, 5, 7, 9, 11, 14 |
| Phase 5 (Infra/Enterprise) | 5, 7, 11, 14, 15 |
| Phase 6 (Multimodal/Trends) | 10, 13 |

## Daily Practice

```
Day 1:  Use Cases 1-3 (Customer support, Legal, EdTech)
Day 2:  Use Cases 4-6 (Fraud, Knowledge Mgmt, Code Review)
Day 3:  Use Cases 7-9 (Healthcare, Email, Supply Chain)
Day 4:  Use Cases 10-12 (Retail, Compliance, Recruitment)
Day 5:  Use Cases 13-15 (Meeting, Data Quality, Multi-Channel)
Day 6:  Pick any 3, draw architecture diagrams from memory
Day 7:  Mock interview: explain any use case in 5 minutes