#! /usr/bin/env node

const { execFile } = require('child_process');
const path = require('path');

if (process.platform !== 'darwin') {
  console.error('This command only supports MacOS/Darwin');
  process.exit(1);
}

const child = execFile(
  path.resolve(__dirname, '../dist/to_json'),
  [process.argv[2] || '', process.argv[3] || ''],
  (error) => {
    if (error) {
      console.error(error);
      process.exit(1);
    }
  }
);

child.stdout.pipe(process.stdout);
child.stderr.pipe(process.stderr);
