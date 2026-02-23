"""
Rebrand StudyMate to LearnLoop
This script updates all occurrences of StudyMate/studymate to LearnLoop/learnloop
"""
import os
import re

# Files to update (excluding certain directories)
EXCLUDE_DIRS = {'.venv', '__pycache__', '.git', 'node_modules', '.kiro'}
EXCLUDE_FILES = {'rebrand_to_learnloop.py'}

# Replacement mappings
REPLACEMENTS = {
    'StudyMate': 'LearnLoop',
    'studymate': 'learnloop',
    'STUDYMATE': 'LEARNLOOP',
    'studymate_invertis_2024': 'learnloop_secret_2024',
}

def should_process_file(filepath):
    """Check if file should be processed"""
    # Skip excluded directories
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in filepath:
            return False
    
    # Skip excluded files
    if os.path.basename(filepath) in EXCLUDE_FILES:
        return False
    
    # Only process text files
    text_extensions = {'.py', '.html', '.md', '.txt', '.json', '.sql', '.css', '.js', '.bat', '.sh'}
    return any(filepath.endswith(ext) for ext in text_extensions)

def rebrand_file(filepath):
    """Replace StudyMate with LearnLoop in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("  Rebranding StudyMate → LearnLoop")
    print("=" * 60)
    print()
    
    updated_files = []
    skipped_files = []
    
    # Walk through all files
    for root, dirs, files in os.walk('.'):
        # Remove excluded directories from search
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if should_process_file(filepath):
                if rebrand_file(filepath):
                    updated_files.append(filepath)
                    print(f"✅ Updated: {filepath}")
                else:
                    skipped_files.append(filepath)
    
    print()
    print("=" * 60)
    print("  Rebranding Complete!")
    print("=" * 60)
    print(f"✅ Files updated: {len(updated_files)}")
    print(f"⏭️  Files skipped: {len(skipped_files)}")
    print()
    
    if updated_files:
        print("Updated files:")
        for f in updated_files[:20]:  # Show first 20
            print(f"  - {f}")
        if len(updated_files) > 20:
            print(f"  ... and {len(updated_files) - 20} more")
    
    print()
    print("🎉 StudyMate is now LearnLoop!")
    print()
    print("Next steps:")
    print("1. Update database name: CREATE DATABASE learnloop;")
    print("2. Update app.config['MYSQL_DB'] = 'learnloop'")
    print("3. Run: python app.py")
    print()

if __name__ == '__main__':
    main()
