#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

// Helper to recursively copy directories
function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function printUsage() {
  console.log(`
Usage:
  npx context-management-for-antigravity [options]

Options:
  --agy           Install to Antigravity CLI directory (~/.gemini/antigravity-cli/skills)
  --path <path>   Install to a custom directory path
  --help, -h      Show this help message
`);
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    printUsage();
    process.exit(0);
  }

  let targetDir = '';
  const pathIndex = args.indexOf('--path');

  if (pathIndex !== -1 && pathIndex < args.length - 1) {
    targetDir = path.resolve(process.cwd(), args[pathIndex + 1]);
  } else if (args.includes('--agy')) {
    targetDir = path.join(os.homedir(), '.gemini', 'antigravity-cli', 'skills');
  } else {
    targetDir = path.join(os.homedir(), '.agents', 'skills');
  }

  console.log(`Installing Context Engineering Skills to: ${targetDir}`);

  const sourceSkillsDir = path.join(__dirname, '..', 'skills');
  const sourceRootSkill = path.join(__dirname, '..', 'SKILL.md');

  if (!fs.existsSync(sourceSkillsDir)) {
    console.error(`Error: Source skills directory not found at ${sourceSkillsDir}`);
    process.exit(1);
  }

  try {
    // Ensure target dir exists
    fs.mkdirSync(targetDir, { recursive: true });

    // Copy skills folder contents
    const skills = fs.readdirSync(sourceSkillsDir);
    let copiedCount = 0;
    
    for (const skill of skills) {
      const srcPath = path.join(sourceSkillsDir, skill);
      if (fs.statSync(srcPath).isDirectory()) {
        const destPath = path.join(targetDir, skill);
        copyRecursiveSync(srcPath, destPath);
        console.log(`  [✓] Copied skill: ${skill}`);
        copiedCount++;
      }
    }

    // Copy root SKILL.md if it exists
    if (fs.existsSync(sourceRootSkill)) {
      fs.copyFileSync(sourceRootSkill, path.join(targetDir, 'SKILL.md'));
      console.log(`  [✓] Copied collection SKILL.md`);
    }

    console.log(`\nSuccess! Installed ${copiedCount} skills to ${targetDir}`);
  } catch (err) {
    console.error(`\nError occurred during installation:`, err.message);
    process.exit(1);
  }
}

main();
