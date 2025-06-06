import vast_api

def create_worker():
    instance = vast_api.create_instance(
        image="yourusername/ace-step-inference:latest",
        gpu="A100",  # или RTX 4090 / A6000
        disk=100,
        env={"MODEL_NAME": "ACE-Step/ACE-Step-v1-3.5B"}
    )
    print(f"Worker запущен: {instance['id']}")

if __name__ == "__main__":
    create_worker()
