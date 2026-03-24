import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = REPO_ROOT / "workspace"
PWSH = shutil.which("pwsh") or shutil.which("pwsh.exe")


def _to_windows_path(path: Path) -> str:
    text = str(path)
    if text.startswith("/mnt/") and len(text) > 6:
        drive = text[5].upper()
        rest = text[6:].replace("/", "\\")
        return f"{drive}:{rest}"
    return text


@unittest.skipUnless(PWSH, "pwsh runtime required")
class TestOrientPwshWrapper(unittest.TestCase):
    def _run_pwsh(self, script: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PWSH, "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_live_lock_adds_coord_when_no_explicit_mode(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            tools_dir = tempdir_path / "tools"
            git_dir = tempdir_path / ".git"
            tools_dir.mkdir(parents=True, exist_ok=True)
            git_dir.mkdir(parents=True, exist_ok=True)
            (git_dir / "index.lock").write_text("", encoding="utf-8")
            (tools_dir / "orient.ps1").write_text(
                (REPO_ROOT / "tools" / "orient.ps1").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (tools_dir / "pwsh_startup.ps1").write_text(
                textwrap.dedent(
                    """
                    function Show-PwshGitRecoveryNotice {
                        param([string]$RepoRoot)
                    }

                    function Test-PwshGitWriteLockActive {
                        param([string]$GitDir)
                        return Test-Path (Join-Path $GitDir "index.lock")
                    }

                    function Invoke-BashPythonTool {
                        param([string]$RepoRoot, [string]$ToolPath, [string[]]$ToolArgs)
                        Write-Host ("TOOLARGS=" + ($ToolArgs -join "|"))
                        return 0
                    }
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            repo_root = _to_windows_path(tempdir_path)
            orient_ps1 = _to_windows_path(tools_dir / "orient.ps1")
            script = textwrap.dedent(
                f"""
                Set-Location '{repo_root}'
                & '{orient_ps1}'
                """
            )
            completed = self._run_pwsh(script)

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertIn("auto-selecting --coord", completed.stdout)
        self.assertIn("TOOLARGS=|--coord", completed.stdout)

    def test_live_lock_preserves_explicit_coord(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE_DIR) as tempdir:
            tempdir_path = Path(tempdir)
            tools_dir = tempdir_path / "tools"
            git_dir = tempdir_path / ".git"
            tools_dir.mkdir(parents=True, exist_ok=True)
            git_dir.mkdir(parents=True, exist_ok=True)
            (git_dir / "index.lock").write_text("", encoding="utf-8")
            (tools_dir / "orient.ps1").write_text(
                (REPO_ROOT / "tools" / "orient.ps1").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (tools_dir / "pwsh_startup.ps1").write_text(
                textwrap.dedent(
                    """
                    function Show-PwshGitRecoveryNotice {
                        param([string]$RepoRoot)
                    }

                    function Test-PwshGitWriteLockActive {
                        param([string]$GitDir)
                        return Test-Path (Join-Path $GitDir "index.lock")
                    }

                    function Invoke-BashPythonTool {
                        param([string]$RepoRoot, [string]$ToolPath, [string[]]$ToolArgs)
                        Write-Host ("TOOLARGS=" + ($ToolArgs -join "|"))
                        return 0
                    }
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            repo_root = _to_windows_path(tempdir_path)
            orient_ps1 = _to_windows_path(tools_dir / "orient.ps1")
            script = textwrap.dedent(
                f"""
                Set-Location '{repo_root}'
                & '{orient_ps1}' --coord
                """
            )
            completed = self._run_pwsh(script)

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        self.assertNotIn("auto-selecting --coord", completed.stdout)
        self.assertIn("TOOLARGS=--coord", completed.stdout)


if __name__ == "__main__":
    unittest.main()
