import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = REPO_ROOT / "workspace"
PWSH = shutil.which("pwsh") or shutil.which("pwsh.exe")
BASH = shutil.which("bash")
sys.path.insert(0, str(REPO_ROOT / "tools"))
import orient_checks  # type: ignore


def _to_windows_path(path: Path) -> str:
    text = str(path)
    if text.startswith("/mnt/") and len(text) > 6:
        drive = text[5].upper()
        rest = text[6:].replace("/", "\\")
        return f"{drive}:{rest}"
    return text


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _init_git_repo(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "memory").mkdir(parents=True, exist_ok=True)
    (root / "tasks").mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(parents=True, exist_ok=True)
    (root / "SWARM.md").write_text("# Swarm\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "README.md").write_text("readme\n", encoding="utf-8")
    (root / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
    (root / "memory" / "INDEX.md").write_text("# Index\n", encoding="utf-8")
    (root / "tasks" / "NEXT.md").write_text("# Next\n", encoding="utf-8")
    (root / "tools" / "orient.py").write_text("print('ok')\n", encoding="utf-8")
    _run(["git", "init"], cwd=root)
    _run(["git", "config", "user.email", "swarm-tests@example.com"], cwd=root)
    _run(["git", "config", "user.name", "Swarm Tests"], cwd=root)
    _run(["git", "add", "."], cwd=root)
    _run(["git", "commit", "-m", "init"], cwd=root)


def _replace_with_partial_index(root: Path, tracked_paths: list[str]) -> None:
    partial_index = root / ".git" / "index.partial"
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(partial_index)
    if partial_index.exists():
        partial_index.unlink()
    subprocess.run(
        ["git", "read-tree", "--empty"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    subprocess.run(
        ["git", "add", "--"] + tracked_paths,
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    shutil.move(str(partial_index), str(root / ".git" / "index"))


def _git_tracked_count(root: Path) -> int:
    return len(_run(["git", "ls-files"], cwd=root).stdout.splitlines())


def _git_head_count(root: Path) -> int:
    return len(_run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=root).stdout.splitlines())


@unittest.skipUnless(PWSH and BASH, "pwsh+bash runtime required")
class TestPowerShellWrapperPassthrough(unittest.TestCase):
    def _run_pwsh(self, script: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PWSH, "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_invoke_native_capture_passthrough_returns_object_and_keeps_stdout_visible(self):
        helper_text = (REPO_ROOT / "tools" / "pwsh_startup.ps1").read_text(encoding="utf-8")
        start = helper_text.index("function Invoke-NativeCapturePassthrough")
        end = helper_text.index("function Invoke-BashPythonTool")
        invoke_native_capture = helper_text[start:end].strip()
        script = (
            invoke_native_capture
            + "\n"
            + textwrap.dedent(
                """
                $result = Invoke-NativeCapturePassthrough -FilePath 'bash' -CommandArgs @('-lc', 'printf ''native-ok\\n''; exit 7')
                if ($result.ExitCode -ne 7) {
                    throw "bad exit code: $($result.ExitCode)"
                }
                """
            )
        )
        completed = self._run_pwsh(script)
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertIn("native-ok", completed.stdout)

    def test_invoke_bash_python_tool_returns_int_and_keeps_stdout_visible(self):
        helper_ps1 = _to_windows_path(REPO_ROOT / "tools" / "pwsh_startup.ps1")
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            tools_dir = tempdir_path / "tools"
            tools_dir.mkdir(parents=True, exist_ok=True)
            (tools_dir / "echo_args.py").write_text(
                "import sys\n"
                "print('helper-ok')\n"
                "print('args=' + '|'.join(sys.argv[1:]))\n"
                "raise SystemExit(9)\n",
                encoding="utf-8",
            )

            repo_root = _to_windows_path(tempdir_path)
            script = textwrap.dedent(
                f"""
                . '{helper_ps1}'
                $result = Invoke-BashPythonTool -RepoRoot '{repo_root}' -ToolPath 'tools/echo_args.py' -ToolArgs @('alpha beta', 'gamma')
                if ($result -isnot [int]) {{
                    throw "wrong return type: $($result.GetType().FullName)"
                }}
                if ($result -ne 9) {{
                    throw "bad exit code: $result"
                }}
                """
            )
            completed = self._run_pwsh(script)

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertIn("helper-ok", completed.stdout)
        self.assertIn("args=alpha beta|gamma", completed.stdout)


@unittest.skipUnless(PWSH, "pwsh runtime required")
class TestPowerShellGitRecoveryNotice(unittest.TestCase):
    def _run_pwsh(self, script: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PWSH, "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_live_index_lock_reports_active_writer_not_corruption(self):
        helper_ps1 = _to_windows_path(REPO_ROOT / "tools" / "pwsh_startup.ps1")
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            (tempdir_path / ".git" / "index.lock").write_text("", encoding="utf-8")

            repo_root = _to_windows_path(tempdir_path)
            script = textwrap.dedent(
                f"""
                . '{helper_ps1}'
                Show-PwshGitRecoveryNotice -RepoRoot '{repo_root}'
                """
            )
            completed = self._run_pwsh(script)

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertIn("[NOTICE] PowerShell git write is active.", completed.stdout)
        self.assertIn("another git writer is active", completed.stdout)
        self.assertNotIn("state looks inconsistent", completed.stdout)
        self.assertNotIn("Recovery:", completed.stdout)

    def test_auto_repair_rebuilds_empty_index_with_stale_lock(self):
        helper_ps1 = _to_windows_path(REPO_ROOT / "tools" / "pwsh_startup.ps1")
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            (tempdir_path / ".git" / "index").write_bytes(b"")
            stale_lock = tempdir_path / ".git" / "index.lock"
            stale_lock.write_text("stale\n", encoding="utf-8")
            old = stale_lock.stat().st_mtime - 600
            os.utime(stale_lock, (old, old))

            repo_root = _to_windows_path(tempdir_path)
            script = textwrap.dedent(
                f"""
                . '{helper_ps1}'
                Show-PwshGitRecoveryNotice -RepoRoot '{repo_root}' -AutoRepair
                """
            )
            completed = self._run_pwsh(script)

            tracked = _run(["git", "ls-files", "--", "SWARM.md"], cwd=tempdir_path)
            index_size = (tempdir_path / ".git" / "index").stat().st_size

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertIn("[RECOVERY] Rebuilt .git/index from HEAD via temporary native index.", completed.stdout)
        self.assertNotIn("[NOTICE]", completed.stdout)
        self.assertEqual(tracked.stdout.strip(), "SWARM.md")
        self.assertGreater(index_size, 100)

    def test_cached_deletion_with_untracked_replacement_is_not_treated_as_corruption(self):
        helper_ps1 = _to_windows_path(REPO_ROOT / "tools" / "pwsh_startup.ps1")
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            _run(["git", "rm", "--cached", "README.md"], cwd=tempdir_path)

            repo_root = _to_windows_path(tempdir_path)
            script = textwrap.dedent(
                f"""
                . '{helper_ps1}'
                Show-PwshGitRecoveryNotice -RepoRoot '{repo_root}'
                """
            )
            completed = self._run_pwsh(script)

            status = _run(["git", "status", "--short"], cwd=tempdir_path).stdout

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertEqual(completed.stdout.strip(), "")
        self.assertIn("D  README.md", status)
        self.assertIn("?? README.md", status)


@unittest.skipUnless(PWSH, "pwsh runtime required")
class TestOrientGitIndexHealth(unittest.TestCase):
    def _run_pwsh(self, script: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PWSH, "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_check_git_index_health_rebuilds_empty_index_without_touching_stale_lock(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            (tempdir_path / ".git" / "index").write_bytes(b"")
            stale_lock = tempdir_path / ".git" / "index.lock"
            stale_lock.write_text("stale\n", encoding="utf-8")
            old = stale_lock.stat().st_mtime - 600
            os.utime(stale_lock, (old, old))

            lines = orient_checks.check_git_index_health(tempdir_path)
            tracked = _run(["git", "ls-files", "--", "SWARM.md"], cwd=tempdir_path)
            index_size = (tempdir_path / ".git" / "index").stat().st_size

        self.assertTrue(any("Auto-repaired" in line for line in lines), lines)
        self.assertEqual(tracked.stdout.strip(), "SWARM.md")
        self.assertGreater(index_size, 100)

    @unittest.skipUnless(BASH, "pwsh+bash runtime required")
    def test_auto_repair_restores_full_head_index(self):
        helper_ps1 = _to_windows_path(REPO_ROOT / "tools" / "pwsh_startup.ps1")
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            _replace_with_partial_index(tempdir_path, ["SWARM.md", "AGENTS.md", "tools/orient.py"])

            self.assertLess(_git_tracked_count(tempdir_path), _git_head_count(tempdir_path))

            repo_root = _to_windows_path(tempdir_path)
            script = textwrap.dedent(
                f"""
                . '{helper_ps1}'
                Show-PwshGitRecoveryNotice -RepoRoot '{repo_root}' -AutoRepair
                """
            )
            completed = subprocess.run(
                [PWSH, "-NoProfile", "-Command", script],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            self.assertNotIn("PowerShell git write is active", completed.stdout)


class TestGitIndexRepair(unittest.TestCase):
    def test_orient_checks_repairs_partial_index(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            _init_git_repo(tempdir_path)
            _replace_with_partial_index(tempdir_path, ["SWARM.md", "AGENTS.md", "tools/orient.py"])

            self.assertLess(_git_tracked_count(tempdir_path), _git_head_count(tempdir_path))

            lines = orient_checks.check_git_index_health(tempdir_path)

            self.assertTrue(any("Auto-repaired" in line for line in lines), lines)
            self.assertEqual(_git_tracked_count(tempdir_path), _git_head_count(tempdir_path))
            self.assertFalse((tempdir_path / ".git" / "index.lock").exists())


class TestPowerShellWrapperContent(unittest.TestCase):
    def test_pwsh_startup_uses_temp_index_swap(self):
        text = (REPO_ROOT / "tools" / "pwsh_startup.ps1").read_text(encoding="utf-8")
        self.assertIn('$env:GIT_INDEX_FILE = $tempIndex', text)
        self.assertIn('Move-Item $tempIndex $indexPath -Force', text)


if __name__ == "__main__":
    unittest.main()
