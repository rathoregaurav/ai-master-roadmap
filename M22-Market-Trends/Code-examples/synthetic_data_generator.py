"""
M22: Synthetic Data Generator
==============================
Generate synthetic datasets for RAG evaluation and fine-tuning.

Key skills:
- Seed-based generation
- Topic expansion from documents
- Quality filtering
- Diverse output generation
- Self-critique validation
"""

import json
import logging
import random
from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Data Models
# ──────────────────────────────────────────────

class QAPair(BaseModel):
    """A single question-answer pair."""
    id: str
    question: str
    answer: str
    difficulty: str = "medium"  # easy, medium, hard
    topic: str = "general"
    source_chunk: Optional[str] = None


class SyntheticDataset(BaseModel):
    """A complete synthetic dataset."""
    name: str
    description: str
    qa_pairs: list[QAPair]
    total_pairs: int
    difficulty_distribution: dict[str, int] = Field(default_factory=dict)
    topic_distribution: dict[str, int] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    """Quality check on a generated Q&A pair."""
    qa_id: str
    is_valid: bool
    accuracy_score: float = Field(..., ge=0.0, le=1.0)
    issues: list[str] = Field(default_factory=list)
    suggested_improvement: Optional[str] = None


# ──────────────────────────────────────────────
# 2. Synthetic Data Generator
# ──────────────────────────────────────────────

class SyntheticDataGenerator:
    """
    Generate synthetic Q&A datasets for RAG evaluation.
    
    Methods:
    - seed_based: Generate variations from seed examples
    - document_based: Extract Q&A from document corpus
    - adversarial: Create hard/distracting examples
    """

    DIFFICULTY_PROMPTS = {
        "easy": """
            Generate a simple factual question that can be answered 
            by quoting directly from the text. The answer should be 
            a single sentence or short paragraph.
        """,
        "medium": """
            Generate a question that requires combining information 
            from 2-3 sentences. The answer requires some synthesis.
        """,
        "hard": """
            Generate a complex question that requires:
            - Multi-step reasoning across the text
            - Logical inference or deduction
            - Comparing/contrasting multiple concepts
            The answer should be detailed and well-structured.
        """,
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(timeout=60.0)

    def from_seeds(
        self,
        seed_qa_pairs: list[dict],
        target_count: int = 50,
        topic: str = "general",
    ) -> SyntheticDataset:
        """
        Generate synthetic Q&A pairs from seed examples.
        
        Uses seed pairs as templates, creates variations
        with different difficulty levels and phrasings.
        """
        all_pairs = []
        batch_size = 5

        for i in range(0, target_count, batch_size):
            remaining = min(batch_size, target_count - len(all_pairs))
            
            # Pick random seed for inspiration
            seed = random.choice(seed_qa_pairs) if seed_qa_pairs else {}
            
            prompt = f"""
            Generate {remaining} diverse question-answer pairs for a {topic} knowledge base.
            
            Use this as inspiration (but create new content, don't copy):
            Seed Question: {seed.get('question', 'What is AI?')}
            Seed Answer: {seed.get('answer', 'AI is...')}
            
            For each pair, vary:
            - Difficulty (easy, medium, hard)
            - Question style (what, how, why, explain, compare)
            - Answer length and depth
            
            Return JSON array of {{question, answer, difficulty, topic}} for each pair.
            Make questions diverse and natural-sounding.
            """

            try:
                response = self.client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You generate diverse synthetic Q&A pairs."},
                            {"role": "user", "content": prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "max_tokens": 3000,
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                )
                response.raise_for_status()
                data = response.json()
                result = json.loads(data["choices"][0]["message"]["content"])

                pairs_data = result.get("qa_pairs", result.get("pairs", []))
                if isinstance(pairs_data, list):
                    for p in pairs_data:
                        all_pairs.append(QAPair(
                            id=f"syn_{len(all_pairs):04d}",
                            question=p.get("question", ""),
                            answer=p.get("answer", ""),
                            difficulty=p.get("difficulty", "medium"),
                            topic=p.get("topic", topic),
                        ))

                logger.info(f"Generated batch: {len(all_pairs)}/{target_count} pairs")

            except Exception as e:
                logger.error(f"Generation batch failed: {e}")
                continue

        return self._build_dataset(all_pairs, f"Seed-generated {topic} dataset")

    def from_document(
        self,
        document_path: str,
        pairs_per_chunk: int = 2,
    ) -> SyntheticDataset:
        """
        Generate Q&A pairs from a document corpus.
        
        Reads document, splits into chunks, generates Q&A per chunk.
        """
        path = Path(document_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")

        text = path.read_text(encoding="utf-8")
        
        # Simple chunking for demo
        chunks = []
        chunk_size = 1000
        for i in range(0, len(text), chunk_size):
            chunk_text = text[i:i + chunk_size].strip()
            if chunk_text:
                chunks.append(chunk_text)

        all_pairs = []
        for i, chunk in enumerate(chunks):
            prompt = f"""
            Generate {pairs_per_chunk} question-answer pairs based on this text chunk.
            
            Text:
            {chunk[:500]}...  # Truncated for demo
            
            Requirements:
            - Questions must be answerable from the text
            - Include a mix of difficulty levels
            - Answers should cite relevant parts of the text
            - Each pair should test different aspects
            
            Return JSON: {{"pairs": [{{"question", "answer", "difficulty", "topic"}}]}}
            """

            try:
                response = self.client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You generate Q&A pairs from document text."},
                            {"role": "user", "content": prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "max_tokens": 2000,
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                )
                response.raise_for_status()
                data = response.json()
                result = json.loads(data["choices"][0]["message"]["content"])

                for p in result.get("pairs", []):
                    all_pairs.append(QAPair(
                        id=f"doc_{len(all_pairs):04d}",
                        question=p.get("question", ""),
                        answer=p.get("answer", ""),
                        difficulty=p.get("difficulty", "medium"),
                        topic=p.get("topic", "general"),
                        source_chunk=f"chunk_{i:04d}",
                    ))

                logger.info(f"Generated {len(all_pairs)} pairs from chunk {i+1}/{len(chunks)}")

            except Exception as e:
                logger.error(f"Chunk {i} generation failed: {e}")
                continue

        return self._build_dataset(all_pairs, f"Document-generated: {path.name}")

    def generate_adversarial(
        self,
        base_dataset: SyntheticDataset,
        count: int = 20,
    ) -> SyntheticDataset:
        """
        Generate adversarial examples to test system boundaries.
        
        These include:
        - Edge cases (missing info, ambiguous questions)
        - Distractors (similar but wrong contexts)
        - Boundary tests (very long/short questions)
        """
        prompt = f"""
        Generate {count} adversarial question-answer pairs to test a RAG system.
        
        Include:
        1. Questions where the answer requires info NOT in the context (5 pairs)
        2. Questions that are ambiguous and could match multiple chunks (5 pairs)
        3. Questions with common misconceptions or traps (5 pairs)
        4. Very short/terse questions that lack context (3 pairs)
        5. Questions with domain-specific terminology (2 pairs)
        
        For each, mark "expected_behavior": "should_reject" or "should_answer"
        
        Return JSON: {{"pairs": [{{"question", "answer", "difficulty", "expected_behavior"}}]}}
        """

        try:
            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You generate adversarial test cases for RAG systems."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 3000,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            result = json.loads(data["choices"][0]["message"]["content"])

            new_pairs = []
            for p in result.get("pairs", []):
                new_pairs.append(QAPair(
                    id=f"adv_{len(new_pairs):04d}",
                    question=p.get("question", ""),
                    answer=p.get("answer", ""),
                    difficulty="hard",
                    topic="adversarial",
                ))

            logger.info(f"Generated {len(new_pairs)} adversarial pairs")
            base_dataset.qa_pairs.extend(new_pairs)
            base_dataset.total_pairs = len(base_dataset.qa_pairs)
            return base_dataset

        except Exception as e:
            logger.error(f"Adversarial generation failed: {e}")
            return base_dataset

    def validate_dataset(
        self,
        dataset: SyntheticDataset,
        sample_size: int = 10,
    ) -> list[ValidationResult]:
        """
        Validate a sample of the generated dataset.
        Uses LLM to check quality and accuracy.
        """
        sample = random.sample(dataset.qa_pairs, min(sample_size, len(dataset.qa_pairs)))
        results = []

        for qa in sample:
            prompt = f"""
            Validate this Q&A pair for a RAG evaluation dataset:
            
            Question: {qa.question}
            Answer: {qa.answer}
            Difficulty: {qa.difficulty}
            
            Check:
            1. Is the question answerable? (yes/no)
            2. Is the answer accurate and factual? (score 0-1)
            3. Does the difficulty match? (yes/no)
            4. Any issues? (list)
            
            Return JSON: {{"is_valid", "accuracy_score", "issues", "suggested_improvement"}}
            """

            try:
                response = self.client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You validate synthetic Q&A pairs for quality."},
                            {"role": "user", "content": prompt},
                        ],
                        "response_format": {"type": "json_object"},
                        "max_tokens": 500,
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                )
                response.raise_for_status()
                data = response.json()
                result = json.loads(data["choices"][0]["message"]["content"])

                results.append(ValidationResult(
                    qa_id=qa.id,
                    is_valid=result.get("is_valid", True),
                    accuracy_score=result.get("accuracy_score", 1.0),
                    issues=result.get("issues", []),
                    suggested_improvement=result.get("suggested_improvement"),
                ))

            except Exception as e:
                logger.error(f"Validation failed for {qa.id}: {e}")
                continue

        valid_count = sum(1 for r in results if r.is_valid)
        logger.info(f"Validation: {valid_count}/{len(results)} valid")
        return results

    def _build_dataset(self, pairs: list[QAPair], description: str) -> SyntheticDataset:
        """Build dataset with statistics."""
        difficulty_dist = {}
        topic_dist = {}
        for p in pairs:
            difficulty_dist[p.difficulty] = difficulty_dist.get(p.difficulty, 0) + 1
            topic_dist[p.topic] = topic_dist.get(p.topic, 0) + 1

        return SyntheticDataset(
            name=f"synthetic_dataset_{len(pairs)}",
            description=description,
            qa_pairs=pairs,
            total_pairs=len(pairs),
            difficulty_distribution=difficulty_dist,
            topic_distribution=topic_dist,
        )

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 3. Demo
# ──────────────────────────────────────────────

def demo():
    """Generate a sample synthetic dataset."""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        logger.info("To run: export OPENAI_API_KEY='your-key'")
        return

    generator = SyntheticDataGenerator(api_key=api_key)

    # Seed-based generation
    seeds = [
        {"question": "What is RAG?", "answer": "RAG combines retrieval and generation."},
        {"question": "How do embeddings work?", "answer": "Embeddings convert text to vectors."},
    ]

    logger.info("Generating from seeds...")
    dataset = generator.from_seeds(seeds, target_count=20, topic="AI Engineering")
    
    print(f"\n{'='*60}")
    print(f"Dataset: {dataset.name}")
    print(f"Total pairs: {dataset.total_pairs}")
    print(f"Difficulty distribution: {dataset.difficulty_distribution}")
    print(f"Topics: {dataset.topic_distribution}")
    print(f"{'='*60}")

    for qa in dataset.qa_pairs[:5]:
        print(f"\n[{qa.difficulty}] Q: {qa.question[:80]}...")
        print(f"A: {qa.answer[:80]}...")

    # Validate a sample
    logger.info("\nValidating dataset...")
    results = generator.validate_dataset(dataset, sample_size=5)
    valid = sum(1 for r in results if r.is_valid)
    print(f"\nValidation: {valid}/{len(results)} pairs valid")

    # Generate adversarial
    logger.info("\nGenerating adversarial examples...")
    dataset = generator.generate_adversarial(dataset, count=10)
    print(f"Total after adversarial: {dataset.total_pairs}")

    generator.close()


if __name__ == "__main__":
    demo()