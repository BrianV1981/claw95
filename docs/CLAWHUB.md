# ClawHub Workflow for Agent Skills

Use ClawHub to discover/install/update skills for your OpenClaw agents.

## Check CLI
```bash
clawhub -V
clawhub list
```

## Search for skills
```bash
clawhub search "discord moderation"
clawhub search "multi agent"
```

## Install a skill
```bash
clawhub install <slug>
```

## Update skills
```bash
clawhub update <slug>
clawhub update --all
```

## Publish your own skill
```bash
clawhub login
clawhub whoami
clawhub publish ./skills/my-skill --slug my-skill --name "My Skill" --version 0.1.0 --changelog "Initial release"
```

## Recommended process for this project
1. Search for skills related to Discord relay, moderation, logging, and prompts.
2. Install in a feature branch.
3. Document what each skill changes.
4. Run `make check` and manual room tests.
5. Keep only skills that improve reliability/clarity.
