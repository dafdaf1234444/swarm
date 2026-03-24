import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = REPO_ROOT / "workspace"
PWSH = shutil.which("pwsh") or shutil.which("pwsh.exe")
BASH = shutil.which("bash")


def _to_windows_path(path: Path) -> str:
    text = str(path)
    if text.startswith("/mnt/") and len(text) > 6:
        drive = text[5].upper()
        rest = text[6:].replace("/", "\\")
        return f"{drive}:{rest}"
    return text


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


if __name__ == "__main__":
    unittest.main()
