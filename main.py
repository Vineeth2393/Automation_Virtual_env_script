import os
import subprocess
import sys

def check_virtualenv(folder_path, env_name):
    # Check if the virtual environment already exists
    if os.path.exists(os.path.join(folder_path, env_name, 'bin')):
        return True

    # Create the virtual environment if it doesn't exist
    try:
        subprocess.run(['python3', '-m', 'venv', env_name], cwd=folder_path, check=True)
        print(f"Virtual environment created in {folder_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def activate_venv(env_name):
    activate_script = os.path.join(env_name, 'bin', 'activate')
    activate_cmd = f'source {activate_script}'
    subprocess.run(activate_cmd, shell=True, executable='/bin/bash')

def deactivate_venv(env_name):
    deactivate_cmd = f'deactivate {env_name}'
    subprocess.run(deactivate_cmd, shell=True)

def install_tensorflow(env_name):
    activate_venv(env_name)
    # Install TensorFlow
    subprocess.run(['pip', 'install', 'tensorflow'], check=True)
    # Install TensorFlow-Metal plug-in
    subprocess.run(['pip', 'install', 'tensorflow-metal'], check=True)

def install_pytorch(env_name):
    activate_venv(env_name)
    # Install PyTorch
    subprocess.run(['pip3', 'install', '--pre', 'torch', 'torchvision', 'torchaudio', '--extra-index-url', 'https://download.pytorch.org/whl/nightly/cpu'], check=True)

def install_requirements(folder_path,env_name):
    # Check for the requirements.txt file
    requirements_path = os.path.join(folder_path, 'requirements.txt')
    if not os.path.exists(requirements_path):
        print(f"Warning: requirements.txt not found at {requirements_path}")
        return

    activate_venv(env_name)
    print(f"Installing packages from requirements.txt...")
    subprocess.run(['pip', 'install', '-r', requirements_path], check=True)

def main():
    folder_path = os.getcwd()
    env_name = input('Provide Virtual environment name: ')

    # Check if the virtual environment exists or create it if needed
    venv_exists = check_virtualenv(folder_path, env_name)

    if venv_exists:
        print(f"Activating virtual environment: {env_name}")
        activate_venv(env_name)
        install_requirements(folder_path,env_name)
        print(f"Packages installed successfully!")
        install_tensorflow(env_name)
        install_pytorch(env_name)
        print(f"TensorFlow, TensorFlow-Metal, and PyTorch installed successfully!")
        # Deactivate the virtual environment
        deactivate_venv(env_name)
    else:
        print(f"Failed to create or activate virtual environment: {env_name}")

if __name__ == '__main__':
    main()