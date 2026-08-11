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
  renderTree(data.tree, data.name);
  language.textContent = data.language || "—";
  framework.textContent = data.framework || "—";

  const stats = countTreeNodes(data.tree);
  fileCount.textContent = stats.files;
  directoryCount.textContent = stats.directories;
  structureType.textContent = data.monorepo ? "Monorepo" : "Repository";

  results.scrollIntoView({ behavior: "smooth" });
}

function renderTree(tree, name) {
  treeOutput.innerHTML = "";

  const root = document.createElement("div");
  root.className = "tree-root";
  root.textContent = `${name || "repository"}/`;

  treeOutput.appendChild(root);
  renderNode(tree, treeOutput);
}

function renderNode(node, parent) {
  if (!node) return;

  Object.entries(node).forEach(([name, value]) => {
    const isFile = Object.keys(value).length === 0;

    const item = document.createElement("div");
    item.className = isFile ? "tree-file" : "tree-directory";

    const row = document.createElement("div");
    row.className = "tree-row";

    const icon = document.createElement("span");
    icon.className = "tree-icon";
    icon.textContent = isFile ? "·" : "▸";

    const label = document.createElement("span");
    label.textContent = name;

    row.appendChild(icon);
    row.appendChild(label);
    item.appendChild(row);

    if (!isFile) {
      const children = document.createElement("div");
      children.className = "tree-children";

      renderNode(value, children);

      row.addEventListener("click", () => {
        const collapsed = children.classList.toggle("collapsed");
        icon.textContent = collapsed ? "▸" : "▾";
      });

      item.appendChild(children);
    }

    parent.appendChild(item);
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
  treeOutput.innerHTML = "";
  input.focus();
}

