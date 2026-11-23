GPUS = {
    "NVIDIA A100":     {"quantity": 4, "memory_gb": 80, "in_use": 1},
    "NVIDIA L40S":     {"quantity": 6, "memory_gb": 48, "in_use": 2},
    "NVIDIA RTX 4090": {"quantity": 3, "memory_gb": 24, "in_use": 0},
    "NVIDIA H100":     {"quantity": 2, "memory_gb": 80, "in_use": 2},
    "NVIDIA A40":      {"quantity": 4, "memory_gb": 48, "in_use": 1},
}

def _with_free(name: str, g: dict) -> list:
  return {"name": name, **g, "free": g["quantity"] - g["in_use"]}

def get_gpu_info(name: str) -> dict:
  # Return VRAM and availability for a GPU model (A100, H100, L40S, RTX 4090, A40)
  if name not in GPUS:
    return GPUS.get(name, {"error": f"GPU '{name}' not found"})
  return _with_free(name, GPUS[name])

def list_all_gpus() -> list:
  # List ALL GPUs in the infrastructure, including those with no free units.
  return [_with_free(n, g) for n, g in GPUS.items()]

def list_available_gpus() -> list:
  # List all GPUs that currently have free units
  return [_with_free(n, g) for n, g in GPUS.items() if (g["quantity"] - g["in_use"]) > 0]

TOOLS = {
  "get_gpu_info": get_gpu_info,
  "list_all_gpus": list_all_gpus,
  "list_available_gpus": list_available_gpus
}