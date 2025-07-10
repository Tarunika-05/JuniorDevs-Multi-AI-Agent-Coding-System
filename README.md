# 👩‍💻 JuniorDevs: Autonomous Code Generation Agent using LangGraph

> An LLM-powered multi-agent system that writes, runs, critiques, and verifies code — simulating a junior developer’s workflow.

---

## 🚀 What is JuniorDevs?

**JuniorDevs** is an **autonomous coding agent** built with **LangGraph**, inspired by how real developers think, debug, and improve.

It takes a natural language coding task and intelligently cycles through:

- 🔧 Engineering the solution
- 🧪 Executing and testing it
- 🧐 Critiquing the result
- ✅ Verifying the logic
- 🔁 Retrying, revising, and improving — just like a junior dev would on the job

---

## 🧠 How It Works

Given a coding prompt, the agent system activates the following:

### ✍️ Engineer Agent

Writes the initial code based on the task.

### ⚙️ Executor Agent

Runs the code safely in a sandboxed environment.

### 🔍 Critic Agent

Analyzes if the output is correct or if any runtime issues occurred.

### 🧠 Verifier Agent

Validates correctness, edge cases, and logical soundness.

---

## 🔁 Retry Strategy

- ❌ If output is **errored** → the **Critic** finds reason for error -> **Engineer** rewrites the code.
- ⚠️ If logic is **flawed** → the **Verifier** requests improvements -> **Engineer** rewrites the code.
- ⛔ After **3 attempts** → the user is prompted to clarify the input.

---

## 📦 Key Features

- ✅ Fully autonomous code generation & feedback loop
- 🧩 Modular and reusable LangGraph agent nodes
- 🔁 Adaptive retry logic with a cap on max attempts
- 📊 Integrated **LangSmith** tracing for observability
- 🔐 Secured with `.env` and Azure OpenAI integration

---

## 🧱 Tech Stack

- **LangGraph** – Graph-based multi-agent orchestration
- **Python** – Execution environment & orchestration logic
- **LangChain + LangSmith** – LLM orchestration & traceability
- **Azure OpenAI** – Secure, scalable LLM backend
- **Stream** – Frontend/UI to input natural language prompts

---

## 🧪 Example Use Case

> 🗣️ _"Write a Python function to calculate the longest increasing subsequence in a list."_

**Agent Flow:**

- 🔄 Agent pipeline activates
- ✍️ Engineer writes the function
- ⚙️ Executor runs test inputs
- 🔍 Critic checks for bugs
- 🧠 Verifier inspects logic
- ✅ Final working code is returned — or retried up to 3 times

---
