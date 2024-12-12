from fastapi import APIRouter
import importlib
import os
from typing import List

router = APIRouter()

def import_routers():
    routers: List[APIRouter] = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"app.routers.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'router'):
                routers.append(module.router)
    return routers

routers = import_routers()
for r in routers:
    router.include_router(r)