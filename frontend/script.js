const API_URL = "http://127.0.0.1:8000";

const input = document.getElementById("repo-url");
const analyzeButton = document.getElementById("analyze-btn");
const status = document.getElementById("status");
const results = document.getElementById("results");
const repoName = document.getElementById("repo-name");
const treeOutput = document.getElementById("tree");
const language = document.getElementById("language");
const framework = document.getElementById("framework");
const fileCount = document.getElementById("file-count");
const directoryCount = document.getElementById("directory-count");
const structureType = document.getElementById("structure-type");
const newAnalysisButton = document.getElementById("new-analysis");

analyzeButton.addEventListener("click", analyzeRepository);
input.addEventListener("keydown", (e) => e.key === "Enter" && analyzeRepository());
newAnalysisButton.addEventListener("click", reset);

async function analyzeRepository() {
  const url = input.value.trim();
  if (!url) return setStatus("Enter a GitHub repository URL.", true);
  if (!isGitHubUrl(url)) return setStatus("Enter a valid GitHub repository URL.", true);

  setLoading(true);

  try {
    const response = await fetch(`${API_URL}/api/tree`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Repository analysis failed.");
    }

    displayResults(data);
    setStatus("Repository analyzed successfully.");
  } catch (error) {
    console.error(error);
    setStatus(error.message || "Unable to connect to Repo Engine.", true);
  } finally {
    setLoading(false);
  }
}

function displayResults(data) {
  results.classList.remove("hidden");
  repoName.textContent = data.name || "Repository";
  treeOutput.textContent = formatTree(data.tree, data.name);
  language.textContent = data.language || "—";
  framework.textContent = data.framework || "—";

  const stats = countTreeNodes(data.tree);
  fileCount.textContent = stats.files;
  directoryCount.textContent = stats.directories;
  structureType.textContent = data.monorepo ? "Monorepo" : "Repository";

  results.scrollIntoView({ behavior: "smooth" });
}

function formatTree(tree, name) {
  const lines = [`${name || "repository"}/`];
  renderNode(tree, "", lines);
  return lines.join("\n");
}

function renderNode(node, prefix, lines) {
  if (!node) return;

  Object.entries(node).forEach(([name, value], index, entries) => {
    const last = index === entries.length - 1;
    const branch = last ? "└── " : "├── ";
    const nextPrefix = prefix + (last ? "    " : "│   ");

    if (Object.keys(value).length === 0) {
      lines.push(`${prefix}${branch}${name}`);
    } else {
      lines.push(`${prefix}${branch}${name}/`);
      renderNode(value, nextPrefix, lines);
    }
  });
}

function countTreeNodes(tree) {
  let files = 0;
  let directories = 0;

  function walk(node) {
    if (!node) return;

    Object.values(node).forEach((value) => {
      if (Object.keys(value).length === 0) {
        files++;
      } else {
        directories++;
        walk(value);
      }
    });
  }

  walk(tree);
  return { files, directories };
}

function isGitHubUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.hostname === "github.com" || parsed.hostname === "www.github.com";
  } catch {
    return false;
  }
}

function setLoading(loading) {
  analyzeButton.disabled = loading;
  analyzeButton.innerHTML = loading ? "Analyzing..." : 'Analyze <span>→</span>';

  if (loading) setStatus("Fetching repository structure...");
}

function setStatus(message, error = false) {
  status.textContent = message;
  status.style.color = error ? "var(--error)" : "var(--text-secondary)";
}

function reset() {
  input.value = "";
  results.classList.add("hidden");
  status.textContent = "";
  input.focus();
}
