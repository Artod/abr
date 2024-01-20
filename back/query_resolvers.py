from typing import Dict, Any
import asyncio

from tartiflette import Resolver

@Resolver("Query.downloadArtifact")
async def resolve_query_download_artifact(
    parent: None, args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo"
) -> Dict[str, Any]:
    return "3434 download Artifact hghgh"

# {
#         "_id": args["_id"],
#         "body": "3434 download Artifact hghgh"
#     }

@Resolver("Query.run")
async def resolve_query_get_run_artifacts(
    parent: None, args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo"
) -> Dict[str, Any]:
    return {
        "_id": args["_id"],
        "artifacts": [
            {
                "_id": 2,
                "name": "name 2"
            },
            {
                "_id": 3,
                "name": "name 3"
            },
        ]
    }
