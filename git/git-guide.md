# Git — A Practical Guide

---

## The History of Git

Before Git existed, development teams relied on centralised version control systems such as **CVS** and **Subversion (SVN)**. In these systems, there was one central server that held the entire history of a project. Every developer would check out files from that server, make changes, and commit them back. This worked, but it came with serious limitations — if the central server went down, no one could collaborate or access the history. If the server's hard drive was corrupted without a backup, everything was lost.

The story of Git begins in 2005 with the **Linux kernel project** — one of the largest and most active open-source software projects in the world. At the time, the Linux development community was using a proprietary distributed version control system called **BitKeeper**. The relationship between the Linux community and BitKeeper's company broke down over licensing disputes, and the free licence was revoked.

This left the Linux kernel project without a version control system. **Linus Torvalds**, the creator of the Linux kernel, decided to build a replacement himself. He had strong requirements: it had to be fast, it had to support distributed workflows, it had to have robust safeguards against corruption, and it had to be free.

In just a few weeks, Torvalds wrote the first version of Git. It was self-hosting — meaning it was used to manage its own source code — from the very beginning. The name _"git"_ is British slang for an unpleasant or dim-witted person; Torvalds has joked that he names all his projects after himself.

Git was released to the public on **7 April 2005**. It was adopted rapidly by the open-source community, and its distributed model — where every developer has a full copy of the repository — proved transformative. Today, Git is by far the most widely used version control system in the world, underpinning platforms like **GitHub**, **GitLab**, and **Bitbucket**.

---

## What is Version Control?

**Version control** is the practice of tracking and managing changes to files over time. It allows you to record every modification made to a project, see who made it, when they made it, and why — and to roll back to any earlier state at any point.

Without version control, managing a codebase across a team is chaotic. Developers overwrite each other's work, bugs get introduced with no clear record of what changed, and there is no safe way to experiment without risking the stability of the project.

Version control solves all of this. It gives a project a full, searchable history and provides the infrastructure for multiple people to work on the same codebase simultaneously without conflict.

---

## What is Git?

**Git** is a **distributed version control system**. Unlike centralised systems where history lives on a single server, Git gives every developer a complete copy of the entire repository — including its full history — on their own machine. There is no single point of failure.

Changes are tracked as a series of **snapshots** rather than as a list of file differences. When you save a version of your project in Git, it takes a snapshot of every file at that moment and stores a reference to it. If a file hasn't changed, Git doesn't store it again — it simply links to the previous identical file. This makes Git extremely efficient.

Git is also fundamentally **offline-capable**. Because the full history is local, you can commit, branch, compare history, and work freely without any network connection. Syncing with a remote server only happens when you explicitly push or pull.

---

## Core Concepts

Before using Git effectively, it is important to understand the four key areas that Git works with.

### The Working Directory

The **working directory** is simply your project folder as it exists on your filesystem — the files you can see and edit. When you make a change to a file, that change lives in the working directory until you explicitly tell Git about it.

### The Staging Area

The **staging area** (also called the **index**) is a holding area between your working directory and your repository. It lets you carefully select exactly which changes you want to include in your next commit, even if you have modified multiple files. This allows you to craft precise, meaningful commits rather than dumping all your changes in at once.

### The Repository

The **repository** (or **repo**) is where Git permanently stores the history of your project. It lives in a hidden `.git` folder at the root of your project. Every commit you make is stored here as a snapshot, along with metadata — who made it, when, and a message describing the change.

### Commits

A **commit** is a saved snapshot of your project at a specific point in time. Each commit has a unique identifier called a **SHA hash** — a long string of letters and numbers like `a3f8c21d...` — which Git uses to reference it precisely. Commits are the building blocks of Git's history.

---

## Getting Started

### Initialising a Repository

To start tracking a project with Git, navigate to the project folder and run:

```bash
git init
```

This creates the hidden `.git` folder and initialises an empty repository. Git is now watching that directory.

### Cloning an Existing Repository

To get a copy of a repository that already exists — on GitHub, for example — use:

```bash
git clone <url>
```

This downloads the entire repository, including its full history, to your machine. The remote it was cloned from is automatically set up as a remote named `origin`.

---

## Core Commands

### Checking Status

```bash
git status
```

Shows you the current state of your working directory and staging area — which files have been modified, which are staged, and which are untracked. This is the most frequently used Git command and a good habit to run before any other operation.

### Staging Changes

```bash
git add <file>
```

Moves a file's changes from the working directory to the staging area. To stage everything at once:

```bash
git add .
```

Use this with care — staging everything at once can accidentally include files you didn't intend to commit.

### Committing

```bash
git commit -m "your message here"
```

Takes everything in the staging area and saves it as a permanent snapshot in the repository. The `-m` flag lets you write the commit message inline. A good commit message is short, specific, and written in the imperative — _"add login page"_, not _"added login page"_ or _"changes"_.

### Viewing History

```bash
git log
```

Shows the full commit history for the current branch — each commit's SHA, author, date, and message. For a more compact view:

```bash
git log --oneline
```

### Viewing Differences

```bash
git diff
```

Shows the exact line-by-line differences between your working directory and the last commit — what has changed but not yet been staged. To see what is staged and ready to commit:

```bash
git diff --staged
```

---

## Branching

### What is a Branch?

A **branch** is an independent line of development. By default, every Git repository starts on a branch called `main` (or historically `master`). When you create a new branch, you are creating a separate pointer that diverges from the current state of the project — allowing you to work on a feature, fix, or experiment in complete isolation, without affecting the main codebase.

Branches are one of Git's most powerful features. They are lightweight — creating a branch in Git is nearly instantaneous, because all Git is doing is creating a new pointer to the current commit.

### Creating and Switching Branches

To create a new branch:

```bash
git branch <branch-name>
```

To switch to it:

```bash
git switch <branch-name>
```

Or to create and switch in one step:

```bash
git switch -c <branch-name>
```

### Viewing Branches

```bash
git branch
```

Lists all local branches. The one you are currently on is marked with an asterisk. To see remote branches too:

```bash
git branch -a
```

### Deleting a Branch

Once a branch has been merged and is no longer needed:

```bash
git branch -d <branch-name>
```

---

## Merging

**Merging** is the process of integrating the work from one branch into another. Typically, this means taking a completed feature branch and merging it back into `main`.

```bash
git switch main
git merge <branch-name>
```

### Fast-Forward Merge

If no new commits have been made on `main` since the branch diverged, Git performs a **fast-forward merge** — it simply moves the `main` pointer forward to the tip of the feature branch. No merge commit is created; the history remains linear.

### Three-Way Merge

If both branches have diverged — meaning commits have been made on both since they split — Git performs a **three-way merge**. It finds the common ancestor commit, compares both branch tips against it, and combines the changes. This creates a new **merge commit** that ties the two histories together.

### Merge Conflicts

When the same part of the same file has been changed differently on both branches, Git cannot automatically decide which version to keep. This is a **merge conflict**. Git pauses the merge and marks the conflicting sections in the file like this:

```
<<<<<<< HEAD
your version of the code
=======
the incoming version of the code
>>>>>>> feature-branch
```

You resolve it by editing the file to the correct state, removing the conflict markers, staging the result, and completing the merge with `git commit`.

---

## Remote Repositories

A **remote** is a version of your repository hosted somewhere else — typically on a server like GitHub. Remotes allow teams to share work and synchronise changes.

### Viewing Remotes

```bash
git remote -v
```

Lists all configured remotes and their URLs. The default remote after a clone is called `origin`.

### Pushing Changes

```bash
git push origin <branch-name>
```

Sends your local commits on the specified branch to the remote repository. The first time you push a new branch, use:

```bash
git push -u origin <branch-name>
```

The `-u` flag sets the upstream tracking reference, so future pushes on that branch can be done with just `git push`.

### Fetching and Pulling

```bash
git fetch
```

Downloads new commits and branches from the remote but does **not** merge anything into your local branches. It is a safe operation — it only updates your remote-tracking references.

```bash
git pull
```

Fetches from the remote and immediately merges the changes into your current branch. It is effectively `git fetch` followed by `git merge`. If you want to avoid the merge commit, you can pull with rebase instead:

```bash
git pull --rebase
```

---

## Git Rebase

### What is Rebase?

**Rebasing** is an alternative to merging for integrating changes from one branch into another. Rather than creating a merge commit, rebase **rewrites the commit history** of your branch so that it appears to have started from a different point.

When you rebase a feature branch onto `main`, Git takes every commit on your feature branch and replays them — one by one — on top of the latest commit on `main`. The result is a perfectly linear history, as if your feature branch was always built on top of the current state of `main`.

```bash
git switch feature-branch
git rebase main
```

### Merge vs Rebase

|                        | **Merge**                                              | **Rebase**                                             |
| ---------------------- | ------------------------------------------------------ | ------------------------------------------------------ |
| **History**            | Preserves full history, including branch structure     | Rewrites history into a clean linear sequence          |
| **Merge commit**       | Creates a merge commit                                 | No merge commit — history appears as if always linear  |
| **Safety**             | Safe on shared branches                                | Should not be used on shared/public branches           |
| **Best for**           | Integrating completed features into a shared branch    | Keeping a feature branch up to date with main          |
| **Conflict handling**  | Resolved once during the merge                        | Resolved commit by commit as they are replayed         |

### The Golden Rule of Rebase

**Never rebase commits that have been pushed to a shared remote branch.** Rebase rewrites commit history, which means the SHA hashes of every replayed commit change. If others have based work on the original commits, their history will diverge and conflicts will be extremely difficult to resolve. Rebase is safe on local, private branches — but once commits are public, use merge.

### Interactive Rebase

Interactive rebase gives you fine-grained control over a sequence of commits before sharing them. You can reorder, combine (squash), edit, or delete individual commits.

```bash
git rebase -i HEAD~3
```

This opens an editor showing the last 3 commits, each prefixed with a command. Changing `pick` to `squash` on a commit folds it into the one above it. This is commonly used to clean up a messy series of work-in-progress commits into a single, clear commit before opening a pull request.

---

## Best Practices

**Commit often, but make each commit meaningful.** Small, focused commits are easier to review, easier to revert if something goes wrong, and produce a history that clearly explains the evolution of the codebase. Avoid the two extremes — committing every single line change, or committing enormous batches of unrelated work.

**Write clear commit messages.** The message should describe _why_ the change was made, not just what. A future reader — including your future self — will thank you. Use the imperative mood: _"fix null pointer in user service"_, not _"fixed"_ or _"changes"_.

**Use branches for everything.** Never commit experimental or in-progress work directly to `main`. Every feature, bug fix, or experiment should live on its own branch. This keeps `main` stable and deployable at all times.

**Pull before you push.** Always fetch or pull the latest changes from the remote before pushing your own. This reduces the chance of conflicts and keeps your local history in sync.

**Keep `main` clean.** Treat `main` as the source of truth. Only merge into it when work is complete, reviewed, and tested. Many teams protect `main` with branch rules that require a pull request and at least one approval before anything can be merged.

**Use `.gitignore`.** Every project should have a `.gitignore` file that tells Git which files and folders to ignore — build artefacts, dependency folders like `node_modules` or `venv`, environment files containing secrets, and editor configuration files. These have no place in version history.

**Never commit secrets.** API keys, passwords, tokens, and credentials should never be committed to a repository — even a private one. Use environment variables and keep sensitive configuration out of version control entirely. Once a secret is committed and pushed, assume it is compromised, even if you delete it in a later commit — the history still contains it.
