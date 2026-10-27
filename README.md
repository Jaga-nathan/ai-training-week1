# Week 1 – Python & Data Engineering (Days 3, 4, 5)

Three **main Python programs**, designed to be run in order. Supporting CSVs, charts,
reports, a notebook and the optional Streamlit app are created by these programs.

> **Important:** Day 5 training instructions include **no source dataset**; `day5.py`
> generates explicitly labelled **synthetic practice data**. Do not present its figures
> as results from a real company or the assignment's illustrative 1480-row example.

## Start from zero in VS Code (Windows / PowerShell)

1. Install Python and VS Code with the Python extension, if not already installed.
2. Install Git for Windows if you don't have Git (`git --version` checks it).
3. Extract the ZIP, then VS Code → **File → Open Folder** → `ai-training-week1`.
4. VS Code → **Terminal → New Terminal**. Terminal should be in `ai-training-week1`.
5. Check `python --version` (or `py --version` if `python` is unavailable).
6. Create the venv (once):

   ```powershell
   python -m venv .venv
   ```

7. Activate the venv (for every new PowerShell terminal):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and try again.
   This changes the execution policy for **that terminal session only**.

8. Install packages (once, from activated venv):

   ```powershell
   python -m pip install -r requirements.txt
   ```

9. Select VS Code's interpreter: **Ctrl+Shift+P → Python: Select Interpreter →
   `ai-training-week1\.venv\Scripts\python.exe`**.
10. Run the three main files **in this order**:

    ```powershell
    python day3.py
    python day4.py
    python day5.py
    ```

11. Check generated folders: `data/` (CSV files), `reports/day4_figures/` (four
    required PNG charts plus a bonus), `reports/figures/` (five Day 5 PNG charts).
12. Open `reports/day5_analysis.ipynb` in VS Code, select `.venv` as kernel, and
    click **Run All**. Save the notebook to include executed outputs.
13. Export the notebook to HTML from the project root:

    ```powershell
    jupyter nbconvert --execute --to html reports/day5_analysis.ipynb --output day5_analysis --output-dir reports
    ```

    This creates `reports/day5_analysis.html`. A PDF is optional, but HTML is enough
    for the assignment's "HTML or PDF" requirement. Avoid moving the HTML away from
    `reports/figures/`, which contains the linked images.
14. Optional Streamlit bonus (Day 5):

    ```powershell
    streamlit run app.py
    ```

    To stop Streamlit, use `Ctrl+C` in the terminal.

## Day 3
- First half: NumPy marks, slicing, mean/sum, broadcasting, weighted `dot`, reshape,
  employee DataFrame, `head/info/describe`, `loc/iloc`, filtering, bonus 3D array.
- Second half: missing data, duplicates, numeric and string dtypes, groupby/agg,
  customer inner/left/outer joins, and bonus `concat` of monthly order files.
- Day 3 script creates **exact source values from the assignment** in
  `data/employees.csv`, `data/orders.csv`, and `data/customers.csv` if absent.

## Day 4
- Uses Day 3 employees.csv. Creates bar/histogram/scatter/line PNGs and 2x2 bonus.
- Git and GitHub commands are manual below, not part of `day4.py`.

## Day 5
- Synthesizes practice CSV to demonstrate cleaning and EDA.
- Cleans missing/duplicate values, flags IQR outliers, computes stats, groups,
  correlations, 5 numeric business answers, budget merge and pivot table.
- Creates 5 figures with insights, one-page summary, presentation notes,
  executable analysis notebook, and a bonus Streamlit dashboard.

## GitHub – one commit on `main` (as requested)

**This single-branch path is your requested simplification.** Your original Day 4
and Day 5 assignment explicitly calls for a feature branch, a Pull Request,
review/merge and a merge conflict. A direct `main` push will **not fulfill those
particular assignment items**, even though it correctly uploads the project.

1. On [github.com](https://github.com), sign in. Click **+ → New repository**.
2. Name it `ai-training-week1`. Choose Public or Private as your trainer requires.
3. **Do not** tick Initialize with README, .gitignore or license; we already have
   local files. Click **Create repository** and copy the HTTPS URL.
4. From **VS Code's terminal inside the extracted folder**, run:

   ```powershell
   git --version
   git init
   git branch -M main
   git config --global user.name "YOUR NAME"
   git config --global user.email "YOUR_GITHUB_EMAIL"
   git status
   git add .
   git status
   git commit -m "Complete Week 1 Days 3 to 5 Python data engineering tasks"
   git remote add origin https://github.com/YOUR_USERNAME/ai-training-week1.git
   git remote -v
   git push -u origin main
   ```

   **Replace** `YOUR NAME`, `YOUR_GITHUB_EMAIL`, `YOUR_USERNAME` with your real
   details. `git config --global` is needed only once on a new Git installation.
   If you already configured Git identity, you can skip the two `git config` lines.
   Do **not** type the final `git push` until you have created the GitHub repo.

5. A browser GitHub sign-in popup may appear. Complete authorization as directed.
   If Git prompts for an HTTPS password rather than using a credential helper,
   enter a GitHub personal access token instead of your account password.
6. Refresh the GitHub repo. Switch to **main**, if needed. Verify your three
   main files and generated results appear. Copy that repository URL to submit.
7. Save your terminal's graph as a screenshot:

   ```powershell
   git log --oneline --graph --all
   ```

   With a single commit, this graph contains only one commit line.

### Future updates (again directly on main)

```powershell
git status
git add .
git commit -m "Update Week 1 analysis and documentation"
git push origin main
```

If you see `remote origin already exists`, do **not** add it again. Use
`git remote -v` to inspect it. If it is the wrong address, run:

```powershell
git remote set-url origin https://github.com/YOUR_USERNAME/ai-training-week1.git
```

If pushing fails because the remote has commits you do not have, stop and
inspect the history with `git fetch origin` and `git log --oneline --all --graph`.
Do **not** force push or run a blind pull. It is simpler to create the GitHub
repository empty at the start.

## What to submit
- Repository URL pointing at `main` (not a hypothetical branch/PR link)
- `day3.py`, `day4.py`, `day5.py` plus generated CSVs and charts
- `reports/day5_analysis.ipynb` with saved outputs and the HTML export
- `reports/one_page_summary.md` and presentation notes
- `git log --oneline --graph --all` screenshot
- **If trainer strictly grades PR/merge/conflict:** discuss permission to omit
  those exercises; this direct-main workflow cannot produce a merged PR link.

## Troubleshooting
- `python` missing: try `py -m venv .venv` and install Python if needed.
- `ModuleNotFoundError`: activate `.venv`, then run `python -m pip install -r requirements.txt`.
- PowerShell says scripts are disabled: use process-scoped execution-policy command above.
- Day 4 missing CSV: run `python day3.py` first.
- Running from wrong location: in VS Code choose File → Open Folder and select
  the extracted `ai-training-week1` folder, then Terminal → New Terminal.
- After a run, `python day5.py` intentionally does **not** overwrite an existing
  `data/weekly_project_raw.csv` (allowing edits). Delete it only when you want to
  regenerate its example records.
