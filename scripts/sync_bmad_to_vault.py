import os
import re
import argparse

def update_frontmatter(content, category, default_name):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        body = match.group(2)
        
        data = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                val = val.strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                data[key.strip()] = val
                
        version = data.get('version', '1.0.0')
        desc = data.get('description', '').replace('"', '\\"')
    else:
        version = '1.0.0'
        desc = ''
        body = content

    new_frontmatter = f"""---
name: "{default_name}"
version: "{version}"
category: "{category}"
description: "{desc}"
dependencies: []
---
"""
    return new_frontmatter + body

def sync_files(source_dir, target_dir):
    personas_map = {
        "_bmad/bmm/1-analysis/bmad-agent-analyst/SKILL.md": "personas/analyst.md",
        "_bmad/bmm/3-solutioning/bmad-agent-architect/SKILL.md": "personas/architect.md",
        ".bmad-core/agents/branding.md": "personas/branding.md",
        "_bmad/cis/skills/bmad-cis-agent-innovation-strategist/SKILL.md": "personas/cis.md",
        "_bmad/bmm/4-implementation/bmad-agent-dev/SKILL.md": "personas/dev.md",
        "_bmad/bmm/2-plan-workflows/bmad-agent-pm/SKILL.md": "personas/pm.md",
        ".bmad-core/agents/po.md": "personas/po.md",
        "_bmad/bmm/4-implementation/bmad-agent-qa/SKILL.md": "personas/qa.md",
        "_bmad/bmm/1-analysis/bmad-agent-tech-writer/SKILL.md": "personas/tech-writer.md",
        "_bmad/bmm/2-plan-workflows/bmad-agent-ux-designer/SKILL.md": "personas/ux.md"
    }

    frameworks_map = {
        ".agent/workflows/analyst.md": "frameworks/analyst.md",
        ".agent/workflows/architect.md": "frameworks/architect.md",
        ".agent/workflows/branding.md": "frameworks/branding.md",
        ".agent/workflows/cis.md": "frameworks/cis.md",
        ".agent/workflows/dev.md": "frameworks/dev.md",
        ".agent/workflows/pm.md": "frameworks/pm.md",
        ".agent/workflows/po.md": "frameworks/po.md",
        ".agent/workflows/qa.md": "frameworks/qa.md",
        ".agent/workflows/ux.md": "frameworks/ux.md"
    }

    def process_map(mapping, category):
        for src_rel, tgt_rel in mapping.items():
            src = os.path.join(source_dir, src_rel)
            tgt = os.path.join(target_dir, tgt_rel)
            if os.path.exists(src):
                with open(src, 'r') as f:
                    content = f.read()
                name = os.path.basename(tgt_rel).replace('.md', '')
                new_content = update_frontmatter(content, category, name)
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                with open(tgt, 'w') as f:
                    f.write(new_content)
                print(f"Synced {src_rel} -> {tgt_rel}")
            else:
                print(f"Warning: Source not found: {src}")

    process_map(personas_map, "persona")
    process_map(frameworks_map, "framework")
    print("Sync complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync BMad personas and frameworks to Savile vault.")
    parser.add_argument("source_bmad_path", help="Path to source bmad directory")
    parser.add_argument("target_vault_path", help="Path to target savile vault directory")
    args = parser.parse_args()
    
    sync_files(args.source_bmad_path, args.target_vault_path)
