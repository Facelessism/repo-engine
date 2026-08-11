# Repo Engine

## Overview

Repo Engine is an extensible lightweight repository analysis engine designed to understand the structure and architecture of Git repositories. It begins by generating an accurate project directory tree from a GitHub repository URL and is designed to evolve into a comprehensive repository intelligence platform capable of detecting technologies, generating documentation, analyzing project architecture, and producing insights for developers.

The project follows a modular architecture that allows new capabilities to be added without modifying the core engine.

## Features

### Current Features

- Fetches repository information using the GitHub REST API.
- Retrieves the complete repository file tree recursively.
- Generates a clean hierarchical directory structure.
- Supports public GitHub repositories.
- Lightweight and modular architecture.
- Fast retrieval without cloning repositories.
- Command-line interface for local usage.

### Planned Features

- Automatic README generation.
- README improvement and modernization.
- Primary programming language detection.
- Framework detection (React, Vue, Angular, Django, Flask, Express, etc.).
- Package manager detection.
- Build system detection.
- Entry point identification.
- Configuration file analysis.
- Test directory detection.
- Documentation discovery.
- CI/CD configuration detection.
- Docker environment detection.
- GitHub Actions analysis.
- Database technology detection.
- Monorepo identification.
- Repository architecture visualization.
- Repository health reports.
- AI-powered repository summaries.
- Web-based interface.

## Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/repo-engine.git
cd repo-engine
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install requests
```

or

```bash
pip install .
```

## Local Development

Repo Engine currently runs as two separate local services:

```text
Frontend → http://127.0.0.1:3000
API      → http://127.0.0.1:8000
```
Both services must be running to use the web interface.

### 1. Start the API

From the project root:

```bash
python -m api.server
```

The API will run at:

```text
http://127.0.0.1:8000
```

Verify it:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "Repo Engine API"
}
```

### 2. Start the Frontend

Open another terminal and enter the frontend directory:

```bash
cd frontend
```

Start the local web server:

```bash
python -m http.server 3000
```

Then open:

```text
http://127.0.0.1:3000
```
in your browser. If port `3000` is already in use, use another port.

### 3. Test the API

You can test repository analysis directly with:

```bash
curl -X POST http://127.0.0.1:8000/api/tree \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/Facelessism/repo-engine"}'
```

Once both servers are running, enter a public GitHub repository URL in the Repo Engine web interface and click **Analyze Repository**.


## Usage

Run the application by providing a GitHub repository URL.

```bash
python main.py https://github.com/vercel/next.js
```

## Example

Input

```text
https://github.com/vercel/next.js
```

Expected Output

```text
next.js/
├── packages/
├── docs/
├── examples/
├── test/
├── package.json
├── README.md
└── turbo.json
```


## How it Works

Repo Engine communicates directly with the GitHub REST API to retrieve repository metadata and file structure.

Instead of cloning the repository, it requests the repository's recursive Git tree, reconstructs the directory hierarchy in memory, and renders it as a readable project tree.

This approach significantly reduces bandwidth usage and improves performance compared to downloading the entire repository.

## API Endpoints Used

### Repository Metadata

```
GET /repos/{owner}/{repo}
```

Used to retrieve:

- Repository name
- Default branch
- General repository metadata

### Repository Tree

```
GET /repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1
```

Used to retrieve the complete recursive file tree for the repository.

## Limitations

- Currently supports public GitHub repositories only.
- GitHub API rate limits apply to unauthenticated requests.
- Symbolic links and Git submodules are treated as regular tree entries.
- Repository contents are not analyzed in the current version; only the directory structure is processed.
- Private repositories are not yet supported.

## Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Please ensure that new features include appropriate documentation and tests where applicable.

## License

This project is licensed under the MIT License.


## Support

For questions, suggestions, bug reports or feature requests, please open an issue in the project's repository.
