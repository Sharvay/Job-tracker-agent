from state import JobTrackerState
from graph import job_tracker_app
import asyncio
from typing import List
import time

async def run_job_async(job_url: str, index: int, total: int):
    print(f"[{index}/{total}] Starting: {job_url[:50]}...")
    
    try:
        # Run in thread pool since invoke is blocking
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, 
            job_tracker_app.invoke, 
            {"job_url": job_url}
        )
        
        if final_state.get('save_status') == 'success':
            details = final_state['final_details']
            print(f"[{index}/{total}] {details['Job Title']} at {details['Company']}")
            return {"status": "success", "details": details, "url": job_url}
        else:
            print(f"[{index}/{total}] Failed")
            return {"status": "failed", "url": job_url}
            
    except Exception as e:
        print(f"[{index}/{total}] Error: {str(e)}")
        return {"status": "error", "error": str(e), "url": job_url}


async def run_batch_parallel(job_urls: List[str], max_concurrent: int = 5):
    """
    Process multiple jobs in parallel with concurrency limit
    """

    print(f"\nProcessing {len(job_urls)} jobs (max {max_concurrent} concurrent)...\n")
    
    start_time = time.time()
    
    # Create tasks
    tasks = [
        run_job_async(url, i+1, len(job_urls)) 
        for i, url in enumerate(job_urls)
    ]
    
    # Run with concurrency limit
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_task(task):
        async with semaphore:
            return await task
    
    results = await asyncio.gather(*[limited_task(t) for t in tasks])
    
    elapsed = time.time() - start_time
    
    # Summary
    print("\n" + "=" * 70)
    print("BATCH SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for r in results if r['status'] == 'success')
    duplicates = sum(1 for r in results if r['status'] == 'duplicate')
    failed = sum(1 for r in results if r['status'] in ['failed', 'error'])
    
    print(f"\nSuccessful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(job_urls)}")
    print(f"Time: {elapsed:.1f} seconds")
    print(f"Speed: {len(job_urls)/elapsed:.1f} jobs/second")
    
    print("\n" + "=" * 70)
    
    return results


if __name__ == "__main__":
    job_urls = [
        "https://www.linkedin.com/jobs/view/4219256012",
        "https://www.linkedin.com/jobs/view/4219256012",
        "https://www.linkedin.com/jobs/view/4196121788",
    ]
    
    # Run parallel batch
    asyncio.run(run_batch_parallel(job_urls, max_concurrent=5))