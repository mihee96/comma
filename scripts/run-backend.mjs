// backend/.venv 의 파이썬으로 uvicorn 을 실행합니다 (venv 활성화 불필요).
// 루트에서 `npm run dev` 또는 `npm run dev:api` 로 호출됩니다.
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const backendDir = join(here, '..', 'backend');
const isWin = process.platform === 'win32';
const venvPython = join(
  backendDir,
  '.venv',
  isWin ? 'Scripts' : 'bin',
  isWin ? 'python.exe' : 'python',
);

if (!existsSync(venvPython)) {
  console.error('\n[run-backend] backend/.venv 를 찾을 수 없습니다. 먼저 백엔드 환경을 만드세요:\n');
  console.error('  cd backend');
  console.error(isWin ? '  py -3.12 -m venv .venv' : '  python3.12 -m venv .venv');
  console.error(isWin ? '  .venv\\Scripts\\Activate.ps1' : '  source .venv/bin/activate');
  console.error('  pip install -r requirements-dev.txt');
  console.error('  copy .env.example .env   (mac/linux: cp .env.example .env)\n');
  process.exit(1);
}

const port = process.env.API_PORT ?? '8000';
const args = ['-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', port];

const child = spawn(venvPython, args, { cwd: backendDir, stdio: 'inherit' });
child.on('exit', (code) => process.exit(code ?? 0));
