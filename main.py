from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

app.add_middleware(
     CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3001"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gemini-2.5-pro"
    project_path: str = "my-test-project"

@app.post("/generate")
async def generate_code(req: GenerateRequest):
        # Save prompt to a file for GPT Engineer
        prompt_file = os.path.join(req.project_path, "prompt")
        os.makedirs(req.project_path, exist_ok=True)
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(req.prompt)
        # Get timeout from env or default to 600 seconds
        timeout = int(os.getenv("GPTE_TIMEOUT", "600"))
        try:
            result = subprocess.run([
                "poetry", "run", "gpte", req.project_path, "--model", req.model
            ], capture_output=True, text=True, input="y\n", timeout=timeout)
            main_py = os.path.join(req.project_path, "src", "main.py")
            code = None
            if os.path.exists(main_py):
                with open(main_py, "r", encoding="utf-8") as f:
                    code = f.read()
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": code,
                "returncode": result.returncode,
                "timeout": timeout,
                "project_path": req.project_path,
                "model": req.model,
                "prompt_file": prompt_file
            }
        except subprocess.TimeoutExpired as e:
            stdout = getattr(e, 'stdout', None)
            stderr = getattr(e, 'stderr', None)
            return {
                "error": "GPT Engineer process timed out.",
                "stdout": stdout,
                "stderr": stderr,
                "timeout": timeout,
                "project_path": req.project_path,
                "model": req.model,
                "prompt_file": prompt_file
            }
        except Exception as ex:
            import traceback
            return {
                "error": str(ex),
                "traceback": traceback.format_exc(),
                "timeout": timeout,
                "project_path": req.project_path,
                "model": req.model,
                "prompt_file": prompt_file
            }
