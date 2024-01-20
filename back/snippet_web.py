from typing import Dict, Any
import asyncio

from tartiflette import Resolver

"""Relevant GraphQL snippets

enum RunStatus {
  NEW
  QUEUED
  TRAINING_START
  TRAINING_DONE
  COMPILE_START
  COMPILE_DONE
  METRICS_START
  METRICS_DONE
  ERROR
}

type Hardware {
  _id: String!
  name: String!
}

type Run {
  _id: ObjectId!
  name: String
  hardware: Hardware!
  status: RunStatus!
}

type Mutation {
  startOptimize(run: ObjectId!): Run!
}
"""

def log(*args, **kwargs):
    print('update', args, kwargs)

db = {
    "runs": {
        "update_one": log,
        "find_one": lambda: {'run_id': 'id'}
    }
}

get_db = lambda: db

@Resolver("Mutation.startOptimize")
async def resolve_mutation_start_optimize(
    parent: None, args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo"
) -> Dict[str, Any]:
    """Resolves mutation that runs the optimize task."""

    db = get_db(ctx["username"])
    runner = ctx["req"].app.state.runner
    run_id = args["run"]

    await db.runs.update_one(args["run"], {"status": "QUEUED"})
    run = await db.runs.find_one(args["run"])

    # use a separate task to wait for and queue each task in turn
    async def run_optimize() -> None:
        status = await runner.queue(
            "train",
            username=ctx["username"],
            run_id=args["run"],
            device=run["hardware"],
        )
        await db.runs.update_one(args["run"], {"jobID": status.job_id})
        exit_code, _ = await status.wait()

        if exit_code == 0:
            status = await runner.queue(
                "compile",
                username=ctx["username"],
                run_id=args["run"],
                device=run["hardware"],
            )
            await db.runs.update_one(args["run"], {"jobID": status.job_id})
            exit_code, _ = await status.wait()

        if exit_code == 0:
            status = await runner.queue(
                "metrics",
                username=ctx["username"],
                run_id=args["run"],
                device=run["hardware"],
            )
            await db.runs.update_one(args["run"], {"jobID": status.job_id})
            exit_code, _ = await status.wait()

        if exit_code != 0:
            await db.runs.update_one(args["run"], {"status": "ERROR"})

    asyncio.get_event_loop().create_task(run_optimize())

    return await db.runs.find_one(args["run"])
