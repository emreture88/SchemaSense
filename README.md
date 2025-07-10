# 🧠 SchemaSense

**Natural Language → SQL using MySQL, Qdrant, and Ollama**

SchemaSense is an intelligent interface between your MySQL schema and your questions in natural language. It semantically embeds your schema into a vector database, matches user queries using embeddings, and generates SQL statements with a local LLM — all without needing external APIs.

---

## 🚀 Features

- 🔍 Extracts your MySQL database schema and foreign key relationships
- 🧬 Converts schema definitions into semantic vector embeddings
- 🧠 Finds the most relevant table(s) for your natural language query
- ✨ Uses a local LLM (via Ollama) to generate SQL code
- 🛠 Works fully offline and is model-agnostic

---

## 📌 Use Case Example

> **User Query:**  
> “Show me all orders from the last 30 days.”

✅ Best matching table: `orders`  
✅ SQL Output:

```sql
SELECT * FROM orders
WHERE order_date >= NOW() - INTERVAL 30 DAY;
```
```css

[ MySQL ]
   ↓  extract_schema.py
[ JSON Schema ]
   ↓  embed_and_store.py
[ Qdrant (Vector DB) ]
   ↑  query_semantic.py
[ User Query ]
   ↓
[ Ollama (LLM) → generate_sql.py ]
   ↓
[ Generated SQL ]

```
Setup
# ⚙️  Setup
**1. Install Ollama and Pull Models**
```code
ollama pull nomic-embed-text   # For vector embedding
ollama pull llama3             # For SQL generation (or use mistral, codellama, etc.)
```
**2. Run Qdrant (Vector DB)**
 ```code
docker run -p 6333:6333 qdrant/qdrant
```
**3. Extract and Embed Schema**
Update your database credentials inside extract_schema.py, then:
 

 ```code
python embed_and_store.py
python generate_sql.py
```
**4. Ask a Question in Natural Language**
```code
python generate_sql.py

 ```


You are a SQL expert. Given the following schema and user question, write an appropriate SQL query.

Schema:
Table `orders` with columns: id, user_id, total. Foreign keys: user_id → users.id.

User question:
List all orders made in the last month.

Output only SQL.


