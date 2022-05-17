#! /usr/bin/env node

const { execFileSync } = require('child_process');

if (process.platform !== 'darwin') {
  console.error('This command only supports MacOS/Darwin');
  process.exit(1);
}

execFileSync('../dist/to_json');
