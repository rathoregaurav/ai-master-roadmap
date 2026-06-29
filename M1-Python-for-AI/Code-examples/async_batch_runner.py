import asyncio
import logging
from dataclasses import dataclass

try:
    from loguru import logger
except ModuleNotFoundError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("async-batch-runner")


@dataclass(frozen=True)
class PromptJob:
    job_id: str
    prompt: str


async def fake_llm_call(job: PromptJob) -> dict[str, str]:
    logger.info(f"starting {job.job_id}")
    await asyncio.sleep(0.4)
    return {
        "job_id": job.job_id,
        "answer": f"Processed: {job.prompt[:40]}",
    }


async def run_batch(jobs: list[PromptJob]) -> list[dict[str, str]]:
    tasks = [fake_llm_call(job) for job in jobs]
    return await asyncio.gather(*tasks)


async def main() -> None:
    jobs = [
        PromptJob("job-1", "Summarize async Python for AI engineers."),
        PromptJob("job-2", "Explain why validation matters."),
        PromptJob("job-3", "Generate a JSON output contract."),
    ]
    results = await run_batch(jobs)
    logger.info(f"results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
