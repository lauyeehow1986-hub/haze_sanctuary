import zipfile
import os
import shutil

zip_path = r"C:\Users\lauye\.gemini\antigravity\brain\24927ba1-48eb-4e41-9f01-6caac3937133\.user_uploaded\media_1793120630871_6c409ed4.zip"
temp_extract_dir = r"C:\Users\lauye\Downloads\haze\temp_skills_extract"
global_skills_dir = r"C:\Users\lauye\.gemini\config\skills"
workspace_skills_dir = r"C:\Users\lauye\Downloads\haze\skills"
workspace_agents_skills_dir = r"C:\Users\lauye\Downloads\haze\.agents\skills"

os.makedirs(temp_extract_dir, exist_ok=True)
os.makedirs(global_skills_dir, exist_ok=True)
os.makedirs(workspace_skills_dir, exist_ok=True)
os.makedirs(workspace_agents_skills_dir, exist_ok=True)

print(f"Opening {zip_path}...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_extract_dir)

print("Extracted archive contents:")
for root, dirs, files in os.walk(temp_extract_dir):
    rel_root = os.path.relpath(root, temp_extract_dir)
    for f in files:
        print(f"  {os.path.join(rel_root, f)}")

# The skills are in temp_extract_dir/skills/
extracted_skills_folder = os.path.join(temp_extract_dir, "skills")
if os.path.exists(extracted_skills_folder):
    for skill_name in os.listdir(extracted_skills_folder):
        skill_src = os.path.join(extracted_skills_folder, skill_name)
        if os.path.isdir(skill_src):
            print(f"\nInstalling skill '{skill_name}'...")
            
            # 1. Global installation
            dest_global = os.path.join(global_skills_dir, skill_name)
            if os.path.exists(dest_global):
                shutil.rmtree(dest_global)
            shutil.copytree(skill_src, dest_global)
            print(f"  -> Installed globally to: {dest_global}")
            
            # 2. Workspace installation
            dest_workspace = os.path.join(workspace_skills_dir, skill_name)
            if os.path.exists(dest_workspace):
                shutil.rmtree(dest_workspace)
            shutil.copytree(skill_src, dest_workspace)
            print(f"  -> Installed in workspace to: {dest_workspace}")

            # 3. Workspace .agents installation
            dest_agents = os.path.join(workspace_agents_skills_dir, skill_name)
            if os.path.exists(dest_agents):
                shutil.rmtree(dest_agents)
            shutil.copytree(skill_src, dest_agents)
            print(f"  -> Installed in .agents to: {dest_agents}")

# Clean up temp
shutil.rmtree(temp_extract_dir)
print("\nTemporary extraction directory cleaned up.")
print("All skills installed successfully!")
