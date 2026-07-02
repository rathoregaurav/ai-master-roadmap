# Key AI Research Papers for AI Engineers

> Summaries of the most important papers for AI engineering practice. You don't need to read every paper—these summaries give you the key insights for interviews and system design.

## How To Use

1. Read the summary (2 min each)
2. Understand: "What problem does this solve?"
3. Connect: "How does this apply to my roadmap?"
4. For interviews: mention the paper when discussing trade-offs

---

## 1. RAG Papers

### "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
**The original RAG paper.**

- **Problem:** LLMs hallucinate on knowledge-intensive tasks
- **Solution:** Retrieve relevant documents from Wikipedia, concatenate with input, generate answer
- **Key insight:** RAG outperforms both pure generation and pure retrieval baselines
- **Architecture:** Dense retriever (DPR) + BART generator
- **Relevance:** This is the foundation of all modern RAG systems. Every RAG interview question traces back to this paper.

### "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., 2023)
**Why RAG still matters even with 128K+ context windows.**

- **Problem:** Models perform worse when relevant information is in the middle of a long context
- **Key finding:** Performance is best when relevant info is at the start or end of context, drops significantly in the middle
- **Implication:** Even with long context, RAG with careful ordering beats stuffing everything into the prompt
- **Relevance:** Justifies RAG over "just put everything in the prompt" approaches

### "CRAG: Corrective Retrieval Augmented Generation" (Yan et al., 2024)
**Making RAG self-correcting.**

- **Problem:** RAG fails when retrieved documents are irrelevant
- **Solution:** Evaluate retrieval quality, if low → rewrite query and re-retrieve, if still low → use web search
- **Key insight:** RAG should evaluate its own retrieval and adapt
- **Relevance:** Advanced RAG pattern for production systems

---

## 2. Agent Papers

### "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
**The foundation of modern agent design.**

- **Problem:** LLMs either reason (CoT) or act (tool use), but not both
- **Solution:** Interleave reasoning traces with action steps
- **Key insight:** Reasoning helps the model decide what to do; acting grounds reasoning in real observations
- **Architecture:** Thought → Action → Observation loop
- **Relevance:** This is the default agent pattern. Every agent framework (LangGraph, AutoGen) implements ReAct.

### "Toolformer: Language Models Can Teach Themselves to Use Tools" (Schick et al., 2023)
**How models learn to call tools.**

- **Problem:** Models need to learn which tools to call and when
- **Solution:** Self-supervised learning: model proposes API calls, checks if result helps, fine-tunes on successful calls
- **Key insight:** Models can learn tool use without human annotations
- **Relevance:** Explains why modern models are so good at tool calling

### "Reflexion: Language Agents with Verbal Reinforcement Learning" (Shinn et al., 2023)
**Agents that learn from mistakes.**

- **Problem:** Agents repeat the same mistakes
- **Solution:** After failure, agent reflects on what went wrong and stores the lesson for next time
- **Key insight:** Self-reflection is a form of reinforcement learning without gradient updates
- **Relevance:** Production agents should reflect on failures

---

## 3. Evaluation Papers

### "Judging LLM-as-a-Judge" (Zheng et al., 2023)
**Can LLMs evaluate other LLMs?**

- **Problem:** Human evaluation is expensive and slow
- **Solution:** Use a strong LLM (GPT-4) to evaluate outputs
- **Key finding:** GPT-4 as judge agrees with humans 80%+ of the time, but has biases (prefers longer answers, prefers its own style)
- **Relevance:** LLM-as-a-judge is the standard evaluation method, but you must account for biases

### "RAGAS: Automated Evaluation of Retrieval Augmented Generation" (Shahul et al., 2023)
**Standardized RAG evaluation metrics.**

- **Problem:** No standard way to evaluate RAG systems
- **Solution:** Define metrics: faithfulness, answer relevance, context precision, context recall
- **Key insight:** RAG evaluation needs both retrieval metrics and generation metrics
- **Relevance:** RAGAS is the most popular RAG evaluation framework

---

## 4. Security Papers

### "Ignore Previous Prompt: Attack Techniques For Language Models" (Perez & Ribeiro, 2022)
**The first systematic study of prompt injection.**

- **Problem:** Models follow instructions from any source (user, retrieved text, system)
- **Solution:** No perfect defense exists, but multiple layers help
- **Key insight:** Prompt injection is not a bug—it's a feature of instruction-following models
- **Relevance:** Explains why prompt injection is so hard to fix

### "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications" (Greshake et al., 2023)
**Indirect prompt injection in the wild.**

- **Problem:** Retrieved documents can contain hidden instructions
- **Solution:** Context separation, input sanitization, output monitoring
- **Key insight:** RAG systems are especially vulnerable because they ingest untrusted content
- **Relevance:** Every RAG system needs indirect injection defenses

---

## 5. System Design Papers

### "Attention Is All You Need" (Vaswani et al., 2017)
**The transformer architecture.**

- **Problem:** RNNs are slow and can't parallelize
- **Solution:** Self-attention mechanism processes all tokens in parallel
- **Key insight:** Attention allows the model to weigh the importance of different input parts
- **Relevance:** Understanding transformers helps you understand model behavior, context windows, and token limits

### "Scaling Laws for Neural Language Models" (Kaplan et al., 2020)
**Why bigger models are better (and when they're not).**

- **Problem:** How should you allocate compute between model size, data, and training?
- **Key finding:** Model performance follows a power-law with compute, data, and parameters
- **Key insight:** Larger models are more sample-efficient—they need fewer tokens per parameter
- **Relevance:** Explains the trend toward larger models and why small models need different strategies

---

## 6. Memory Papers

### "MemGPT: Towards LLMs as Operating Systems" (Packer et al., 2023)
**Memory management for LLMs.**

- **Problem:** LLMs have fixed context windows
- **Solution:** Treat context like virtual memory—page in relevant context, page out stale context
- **Key insight:** Memory management (eviction, retrieval, compression) is essential for long-running agents
- **Relevance:** Foundation for agent memory systems

---

## 7. Multimodal Papers

### "CLIP: Learning Transferable Visual Models From Natural Language Supervision" (Radford et al., 2021)
**The foundation of multimodal AI.**

- **Problem:** Vision models need labeled data
- **Solution:** Train on image-text pairs from the internet using contrastive learning
- **Key insight:** A single model can understand both images and text in the same embedding space
- **Relevance:** Powers multimodal search, image classification, and vision-language models

---

## 8. Cost & Efficiency Papers

### "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale" (Dettmers et al., 2022)
**Making LLMs cheaper to run.**

- **Problem:** LLMs are expensive to serve (need multiple GPUs)
- **Solution:** Use 8-bit quantization instead of 16-bit, with outlier feature splitting
- **Key insight:** Most weights can be quantized to 8-bit without quality loss; only outlier features need 16-bit
- **Relevance:** Enables running models on fewer GPUs, reducing cost

### "FlashAttention: Fast and Memory-Efficient Exact Attention" (Dao et al., 2022)
**Making attention faster.**

- **Problem:** Attention is O(n²) in memory and compute
- **Solution:** Tiling algorithm that computes attention without materializing the full attention matrix
- **Key insight:** FlashAttention is 2-4x faster and uses much less memory
- **Relevance:** Enables longer context windows and faster inference

---

## How To Reference Papers In Interviews

**Good:** "The ReAct paper showed that interleaving reasoning and action improves agent performance. I apply this by having my agent output a reasoning step before each tool call."

**Better:** "The ReAct paper found that reasoning traces help the model decide which tool to call, and tool observations ground the reasoning. In my system, I implement this as a Thought → Action → Observation loop with a max of 20 iterations."

**Best:** "The ReAct paper established the Thought → Action → Observation loop. However, the Reflexion paper showed that adding self-reflection after failures improves performance. I combine both: ReAct for the main loop, Reflexion for post-failure learning."

## Reading Strategy

| Priority | Papers | Time |
|----------|--------|------|
| Must-read | RAG, ReAct, Lost in the Middle, LLM-as-a-Judge | 2 hours |
| Important | Toolformer, Reflexion, RAGAS, Prompt Injection | 2 hours |
| Good to know | Attention, Scaling Laws, MemGPT, CLIP | 2 hours |
| Bonus | FlashAttention, LLM.int8(), CRAG | 1 hour |