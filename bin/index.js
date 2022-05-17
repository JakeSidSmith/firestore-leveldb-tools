#! /usr/bin/env node

const { execFileSync } = require('child_process');
const path = require('path');

if (process.platform !== 'darwin') {
  console.error('This command only supports MacOS/Darwin');
  process.exit(1);
}

execFileSync(path.resolve(__dirname, '../dist/to_json'));
