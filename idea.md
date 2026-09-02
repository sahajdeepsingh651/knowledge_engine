I want you to help me design a general-purpose personal Knowledge Engine. Please treat the following as the current product vision and reason from it rather than assuming I want a generic RAG, note-taking app, or AI tutor.

## 1. What I already have

I already have an existing knowledge base.

It is currently a collection of files/notes that are interconnected with links.

For example:

```text
networking/
├── ip.md
├── routing.md
├── ovs.md
├── ovn.md
└── openstack.md
```

and the files may link to one another.

This existing file-based KB is the starting corpus.

It is NOT yet the conceptual knowledge graph I want.

I want to build a Knowledge Engine on top of this existing KB.

---

## 2. What I ultimately want

When I am trying to understand a topic, I want the system to help me:

- rediscover what I already know
- identify relevant concepts
- identify prerequisites
- discover missing concepts
- discover missing/weak relationships
- retrieve authoritative source material
- point to the specific important parts of that source
- explain the topic
- add/refine concepts and relationships in the knowledge graph
- test whether I actually understand the concepts
- track what I genuinely know over time

I will not primarily use the knowledge base as something I manually read.

The knowledge base is primarily an **AI-readable persistent knowledge substrate**.

My main interaction with the knowledge system will be through agents, especially a Recall Agent and learning agents.

---

# 3. There are three distinct layers

I want to clearly separate these.

### A. Existing Knowledge Base

My current files and their links.

This is raw accumulated knowledge/content.

```text
files
notes
documents
links
metadata
```

### B. Knowledge Graph

A structured conceptual model derived from the KB and external evidence.

For example:

```text
OVN ──uses──> OVS
OVN ──stores state in──> SB DB
OVN ──related_to──> Neutron
```

The original files remain intact.

The graph is a derived structure on top of them.

### C. Learning State

A representation of what I actually understand.

For example:

```text
OVN
├── definition: strong
├── OVS relationship: strong
├── SB DB relationship: weak
└── logical flows: weak
```

Learning state must not be confused with graph state.

The graph answers:

> What concepts and relationships exist?

Learning state answers:

> How well does the user understand them?

---

# 4. Concept identity / node naming

The canonical node name should NOT simply be copied from whichever book or source first mentioned it.

The system should identify concepts by meaning.

For example:

```text
Canonical concept:
Virtual Memory

Aliases:
virtual memory
VM
virtual-memory abstraction
```

Different books, papers, and documentation may use different terminology for the same concept.

The system should preserve source terminology as aliases/provenance rather than treating every wording as a different node.

It should also recognize that the same word can mean different things in different domains.

---

# 5. Evidence and source truth

The Knowledge Graph should not itself be treated as the ultimate source of truth.

There should be a separate evidence/provenance layer.

For example:

```text
Concept: IP routing

supported_by
    ↓
RFC
    ↓
specific section/paragraph
```

or:

```text
Concept: Kubernetes controller

supported_by
    ↓
Kubernetes documentation
    ↓
specific section
```

The system should be able to answer:

> Why does the Knowledge Engine believe this concept or relationship?

and trace it back to the original source.

The graph is a structured model.

The source material is the evidence.

---

# 6. Bootstrap problem

An important constraint:

At the beginning, the conceptual graph may be empty or incomplete.

I cannot assume that graph traversal, embeddings, or vector search already exist.

Initially the system may rely on:

- existing file structure
- links between files
- metadata
- keyword/full-text search
- web/source search
- Claude's reasoning over retrieved material

Then the system gradually builds the conceptual graph.

Later it can add:

- embeddings
- vector search
- semantic retrieval
- richer graph traversal

These should be evolutionary improvements, not foundational assumptions.

---

# 7. When I ask to learn a topic

Suppose I ask:

> "Help me understand OVN."

The system should roughly do:

```text
User goal
    ↓
find relevant material in existing KB
    ↓
retrieve relevant files/topics
    ↓
identify candidate concepts
    ↓
identify candidate relationships
    ↓
check learning state if available
    ↓
identify gaps
    ↓
retrieve external authoritative sources when necessary
    ↓
retrieve relevant sections/passages
    ↓
Claude reasons over the material
    ↓
explain / teach
    ↓
propose graph updates
    ↓
Knowledge Engine stores validated/provenanced knowledge
```

The system should be able to improve the graph as I learn.

---

# 8. How should "what I already know" be decided?

This should NOT be inferred only from the fact that a concept exists in my files.

A concept being present in my KB means:

> It exists in my accumulated knowledge corpus.

It does NOT prove:

> I understand it.

The actual learning state should primarily be established through interaction and recall.

For example:

```text
Concept: OVN

exposure: high
definition recall: strong
OVN → OVS relationship: strong
OVN → SB DB relationship: weak
```

The Knowledge Engine should maintain this learning state.

The Recall Agent should generate evidence for it.

---

# 9. Related concepts

There may be two stages.

Before a rich graph exists:

- keyword search
- file links
- source structure
- Claude reasoning
- later embeddings/vector search

After the graph exists:

- graph relationships
- prerequisites
- related concepts
- semantic/vector retrieval
- source relationships

The Knowledge Engine can retrieve candidate related concepts.

Claude can reason about which are relevant to the user's current goal.

---

# 10. Prerequisites

Prerequisites may initially be inferred from:

- existing file relationships
- source structure
- authoritative material
- Claude's reasoning

Once a graph exists, prerequisites can become explicit graph edges.

For example:

```text
Routing
    requires → IP
    requires → subnet
```

The Knowledge Engine can identify structural prerequisites.

Claude can determine which of those prerequisites are actually important for the user's current learning goal.

---

# 11. Weak or missing connections

This is an important distinction.

A graph relationship can exist even when I do not understand it.

Example:

```text
OVN ──uses──> OVS
```

That means:

> The system believes the relationship is true.

It does NOT mean:

> I understand why the relationship exists.

The Recall Agent should primarily determine this.

For example, it asks:

> Why does OVN use OVS?

My answer reveals whether I actually understand the relationship.

So:

```text
Knowledge Graph
    = what the system believes exists

Recall Agent
    = tests whether I understand it

Learning State
    = stores the result
```

A weak connection should therefore be a **learning-state observation**, not automatically a graph change.

---

# 12. Recall Agent

The Recall Agent is a core part of the system.

Its job is to test genuine understanding.

It should test things such as:

- definitions
- mechanisms
- relationships
- prerequisites
- comparisons
- application
- causal reasoning
- explanation ability

Example:

Instead of:

> What is routing?

ask:

> A packet arrives at a Linux machine. How does the machine determine which interface the packet should leave through?

The Recall Agent evaluates the answer and updates Learning State.

A failed recall should normally update:

```text
learning_state
```

not rewrite the concept itself.

If the answer suggests that the graph or source representation is wrong, that can be handled as a separate proposed knowledge correction.

---

# 13. Source selection

The system should not randomly search for books.

It needs a concept of **source policy by domain**.

For example:

### Networking

```text
RFCs
standards
academic papers
authoritative textbooks
official documentation
```

### Programming languages

```text
language specification
official documentation
implementation documentation
academic papers
```

### Kubernetes

```text
official documentation
KEPs/design documents
source code
authoritative technical material
```

The source policy should determine what kinds of sources are considered authoritative for a domain.

Initially I may configure these policies manually.

Later, Claude can propose changes.

---

# 14. Which specific book/paper/document should be used?

This should be a collaboration between the Knowledge Engine and Claude.

The Knowledge Engine should retrieve candidate sources based on:

- domain
- topic
- source policy
- metadata
- keyword search
- later vector search
- existing evidence
- source quality

Then Claude can reason about which candidate is most useful for the current learning goal.

For example:

```text
Topic: Virtual Memory

Candidate sources:
- textbook
- operating systems notes
- academic paper
- Linux documentation
```

Claude can decide:

> The textbook is best for conceptual understanding.

while the Knowledge Engine remains responsible for finding and retrieving the candidates.

---

# 15. Which part of a source should be retrieved?

The system should not blindly ingest entire books.

It should retrieve relevant units such as:

- chapter
- section
- paragraph
- page
- figure/table where applicable

Initially this can use:

- document hierarchy
- keywords
- metadata
- full-text search
- Claude reasoning

Later:

- embeddings
- vector search
- semantic retrieval

The result should preserve provenance:

```text
Concept
    ↓
Source
    ↓
Chapter
    ↓
Section
    ↓
Paragraph/page
```

---

# 16. Source relationships

Initially there may be no explicit source graph.

These relationships should be created as knowledge is extracted.

For example:

```text
Concept: OVN
    supported_by → source A, section 3
    supported_by → source B, page 42

Relationship:
OVN → uses → OVS
    supported_by → source C, section 5
```

Source relationships therefore become part of the persistent evidence/provenance layer.

---

# 17. Candidate vs confirmed knowledge

Claude should be allowed to propose:

```text
OVN → uses → OVS
```

but the Knowledge Engine should distinguish:

```text
proposed
supported
confirmed
contradicted
```

An LLM statement should not automatically become trusted knowledge.

Persistent knowledge needs provenance.

---

# 18. Torch passing between Claude and Knowledge Engine

This is the architectural boundary I care about most.

I do NOT want Claude to become the database.

Claude should be a reasoning/interaction layer on top of the Knowledge Engine.

### Knowledge Engine should own persistent/system responsibilities

- existing KB
- file/document storage
- knowledge graph
- concept identity
- aliases
- relationships
- prerequisites
- provenance
- source/evidence store
- retrieval
- search
- source policies
- learning state
- recall history
- persistence
- validation/state transitions
- MCP/API interface

### Claude should own reasoning/interpretation responsibilities

- understand my current goal
- interpret retrieved information
- decide what is relevant right now
- reason over candidate concepts
- choose how to explain something
- generate questions
- evaluate nuanced answers
- propose concepts/relationships
- decide how to teach/reframe
- decide what additional information is needed

The Knowledge Engine should not simply become:

> "an LLM without a chat UI."

It should primarily maintain and query persistent state.

Claude should think with that state.

---

# 19. Example torch-passing loop

A typical interaction should look like:

```text
User:
"Help me understand OVN."

        ↓

Claude:
Understands the learning goal.

        ↓

Knowledge Engine:
Searches existing KB.

Returns:
- relevant files
- existing concepts
- evidence
- learning state
- candidate related concepts

        ↓

Claude:
Reasons about what is relevant/missing.

        ↓

Knowledge Engine:
Retrieves additional material if requested.

        ↓

External Research:
Find authoritative sources if current KB is insufficient.

        ↓

Knowledge Engine:
Returns relevant source passages with provenance.

        ↓

Claude:
Explains the topic.

        ↓

Claude:
Proposes concepts/relationships or asks questions.

        ↓

Knowledge Engine:
Stores/validates/persists the resulting knowledge and state.

        ↓

Recall Agent:
Tests whether I actually understand it.

        ↓

Knowledge Engine:
Updates Learning State.

        ↓

Next learning gap is selected.
```

---

# 20. MCP

MCP should be treated as an interface between agents and the Knowledge Engine, not as the Knowledge Engine itself.

Possible tools could eventually include:

```text
search_kb()
get_concept()
get_related_concepts()
get_prerequisites()
get_learning_state()
get_evidence()
get_source_passages()
find_learning_gaps()
propose_concept()
propose_relationship()
record_recall_attempt()
update_learning_state()
```

I want the underlying Knowledge Engine to remain independent of Claude.

Claude could eventually be replaced by another LLM or agent.

---

# 21. Coding protocol

The same Knowledge Engine should later support coding.

Coding should be a protocol/plugin on top of the general Knowledge Engine.

The coding pipeline should be:

```text
Concept
    ↓
Generalized pseudocode
    ↓
Refined pseudocode
    ↓
Language-aware pseudocode
    ↓
Language constructs / keywords
    ↓
Actual code
```

The underlying knowledge should remain language/domain independent where possible.

The coding protocol determines how that knowledge is transformed into implementation.

---

# 22. The architecture I currently imagine

```text
                     Claude / Other Agents
                              │
                             MCP
                              │
                    ┌─────────▼─────────┐
                    │  Knowledge Engine │
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
   Existing KB          Knowledge Graph      Learning State
   files/links           concepts/edges       user understanding
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                       Evidence Store
                              │
                    external/primary sources
                              │
                       Retrieval Layer
                              │
                 keyword → later vector/semantic
```

And on top of the same engine:

```text
Learning Protocol
Recall Protocol
Coding Protocol
Research Protocol
```

---

# 23. Core design principle

The system should continuously evolve through:

```text
Existing KB
    ↓
retrieve
    ↓
reason
    ↓
extract concepts
    ↓
build/refine graph
    ↓
attach evidence
    ↓
teach
    ↓
recall
    ↓
measure understanding
    ↓
update learning state
    ↓
find next gap
    ↓
retrieve more evidence
    ↓
repeat
```

The ultimate goal is to build a persistent knowledge substrate that an AI can use to understand:

1. what knowledge exists,
2. where that knowledge came from,
3. how concepts relate,
4. what I actually understand,
5. what I am weak at,
6. what I should learn next,
7. and what authoritative evidence should be used to support the learning.

Please do NOT jump directly to implementation.

First help me determine the **correct responsibility boundaries, data model, state transitions, and torch-passing protocol between the Knowledge Engine, Claude, Research/Retrieval components, and Recall Agent**.

I want the architecture to be general enough that Claude is only one possible client of the Knowledge Engine.
