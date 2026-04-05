"""
Question Bank — categorized pre-defined interview questions
Each question has: id, text, category, difficulty, ideal_keywords, ideal_answer
"""
from typing import List, Dict
import uuid


class QuestionBank:
    """Database of categorized interview questions"""

    def __init__(self):
        self.questions = self._load_questions()

    def _load_questions(self) -> List[Dict]:
        return [
            # ===== Python =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between a list and a tuple in Python?",
                "category": "Python",
                "difficulty": "easy",
                "ideal_keywords": ["mutable", "immutable", "list", "tuple", "changeable", "parentheses", "bracket"],
                "ideal_answer": "Lists are mutable meaning they can be modified after creation, while tuples are immutable. Lists use square brackets [] and tuples use parentheses (). Due to mutability, lists have more overhead and tuples are slightly faster.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain the difference between '==' and 'is' in Python.",
                "category": "Python",
                "difficulty": "easy",
                "ideal_keywords": ["==", "is", "equality", "identity", "compare", "value", "object"],
                "ideal_answer": "== checks for value equality (whether the values are equal), while 'is' checks for identity (whether they are the same object in memory). 'is' returns True only if both variables point to the exact same object.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is a decorator in Python? Give an example.",
                "category": "Python",
                "difficulty": "medium",
                "ideal_keywords": ["decorator", "function", "wrapper", "@", "modify", "behavior", "higher-order"],
                "ideal_answer": "A decorator is a function that modifies the behavior of another function without changing its code. It takes a function as input and returns a new function. Decorators use the @ symbol followed by the decorator name above the function definition.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are Python generators? When would you use them?",
                "category": "Python",
                "difficulty": "medium",
                "ideal_keywords": ["generator", "yield", "iterator", "memory", "lazy", "efficient", "stream"],
                "ideal_answer": "Generators are functions that use yield to return values one at a time, creating an iterator. They are memory efficient because they generate values on-demand rather than storing them all in memory at once. Use generators when working with large datasets or infinite sequences.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the Global Interpreter Lock (GIL) in Python?",
                "category": "Python",
                "difficulty": "hard",
                "ideal_keywords": ["GIL", "Global Interpreter Lock", "threading", "CPU-bound", "multithreading", "mutex", "performance"],
                "ideal_answer": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously. This means threads cannot fully utilize multiple CPU cores for CPU-bound tasks. It affects multithreading in CPU-bound code but not in I/O-bound code.",
            },

            # ===== JavaScript =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between var, let, and const in JavaScript?",
                "category": "JavaScript",
                "difficulty": "easy",
                "ideal_keywords": ["var", "let", "const", "scope", "hoisting", "reassign", "block", "function"],
                "ideal_answer": "var is function-scoped and hoisted, let and const are block-scoped. const cannot be reassigned after declaration (though object properties can be modified), while let can be. var can be redeclared, let and const cannot.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain closures in JavaScript with an example.",
                "category": "JavaScript",
                "difficulty": "medium",
                "ideal_keywords": ["closure", "function", "scope", "lexical", "access", "variable", "inner", "outer"],
                "ideal_answer": "A closure is a function that has access to variables from its outer (enclosing) scope even after the outer function has returned. This happens because functions in JavaScript form closures, retaining their scope chain.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between == and === in JavaScript?",
                "category": "JavaScript",
                "difficulty": "easy",
                "ideal_keywords": ["==", "===", "equality", "type", "coercion", "loose", "strict", "compare"],
                "ideal_answer": "== is loose equality that performs type coercion before comparison (1 == '1' is true), while === is strict equality that checks both value and type without coercion (1 === '1' is false). Prefer === for predictable comparisons.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the event loop in JavaScript?",
                "category": "JavaScript",
                "difficulty": "hard",
                "ideal_keywords": ["event loop", "call stack", "callback queue", "asynchronous", "non-blocking", "execution", "Web APIs"],
                "ideal_answer": "The event loop continuously monitors the call stack and callback queue. If the call stack is empty, it pushes the next callback from the queue to the stack for execution. This enables non-blocking asynchronous operations in JavaScript despite being single-threaded.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are Promises and async/await in JavaScript?",
                "category": "JavaScript",
                "difficulty": "medium",
                "ideal_keywords": ["Promise", "async", "await", "asynchronous", "then", "resolve", "reject", "callback", "chaining"],
                "ideal_answer": "A Promise represents a value that may be available now, in the future, or never. It has three states: pending, fulfilled, and rejected. async/await is syntactic sugar over Promises that makes asynchronous code look and behave more like synchronous code, using the await keyword to pause execution.",
            },

            # ===== React =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between useEffect and useLayoutEffect?",
                "category": "React",
                "difficulty": "medium",
                "ideal_keywords": ["useEffect", "useLayoutEffect", "asynchronous", "synchronous", "DOM", "paint", "cleanup", "timing"],
                "ideal_answer": "useEffect runs asynchronously after the component renders and paints, while useLayoutEffect runs synchronously before the browser paints. Use useLayoutEffect when you need to measure or mutate the DOM before the user sees the update, otherwise prefer useEffect.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are React hooks? Name a few commonly used ones.",
                "category": "React",
                "difficulty": "easy",
                "ideal_keywords": ["hooks", "useState", "useEffect", "useContext", "useReducer", "useRef", "state", "side effect"],
                "ideal_answer": "Hooks are functions that let you use React state and lifecycle features in functional components. Common hooks include: useState for state management, useEffect for side effects, useContext for consuming context, useRef for mutable refs, and useReducer for complex state logic.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain the useState hook and when you would use it.",
                "category": "React",
                "difficulty": "easy",
                "ideal_keywords": ["useState", "state", "setState", "component", "re-render", "functional", "update"],
                "ideal_answer": "useState is a hook that lets you add state to functional components. It returns an array with the current state value and a function to update it. Call setState with a new value to trigger a re-render. Use it when a component needs to remember data that changes over time.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the Virtual DOM and how does React use it?",
                "category": "React",
                "difficulty": "medium",
                "ideal_keywords": ["Virtual DOM", "DOM", "reconciliation", "diffing", "update", "render", "performance", "batch"],
                "ideal_answer": "The Virtual DOM is a lightweight JavaScript representation of the actual DOM. When state changes, React creates a new Virtual DOM tree, compares it with the previous one (diffing), and only updates the changed elements in the real DOM (reconciliation). This minimizes expensive DOM operations.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are controlled and uncontrolled components in React?",
                "category": "React",
                "difficulty": "medium",
                "ideal_keywords": ["controlled", "uncontrolled", "form", "input", "state", "ref", "value", "onChange"],
                "ideal_answer": "A controlled component's form data is handled by React state, where the input value is set by state and changes are handled by setState. An uncontrolled component uses a ref to directly access the DOM element's value. Controlled components offer more predictability, uncontrolled offer better performance for simple forms.",
            },

            # ===== Node.js =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is Express.js and why is it popular?",
                "category": "Node.js",
                "difficulty": "easy",
                "ideal_keywords": ["Express", "framework", "middleware", "routing", "HTTP", "request", "response", "minimal"],
                "ideal_answer": "Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for building web and mobile applications. It's popular because it's unopinionated, easy to learn, highly extensible with middleware, and great for building RESTful APIs.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain middleware in Express.js. Give examples.",
                "category": "Node.js",
                "difficulty": "medium",
                "ideal_keywords": ["middleware", "request", "response", "next", "function", "error-handling", "logging", "authentication", "CORS"],
                "ideal_answer": "Middleware functions have access to the request object, response object, and the next function. They can execute code, modify the request/response, end the cycle, or call the next middleware. Examples include logging (morgan), authentication (passport), error handling, CORS, and body parsing.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between process.nextTick and setImmediate?",
                "category": "Node.js",
                "difficulty": "hard",
                "ideal_keywords": ["process.nextTick", "setImmediate", "callback", "queue", "event loop", "execute", "I/O"],
                "ideal_answer": "process.nextTick defers execution to after the current operation completes but before the event loop continues, with higher priority than other async operations. setImmediate defers execution to the next iteration of the event loop, after I/O callbacks. nextTick can starve I/O while setImmediate doesn't.",
            },

            # ===== SQL =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between INNER JOIN and LEFT JOIN?",
                "category": "SQL",
                "difficulty": "easy",
                "ideal_keywords": ["INNER JOIN", "LEFT JOIN", "join", "table", "match", "null", "rows", "outer", "inner"],
                "ideal_answer": "INNER JOIN returns only rows where there is a match in both tables. LEFT JOIN returns all rows from the left table and matched rows from the right table, with NULL values for non-matching columns. LEFT JOIN is useful when you want all records from one table regardless of matches.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are SQL indexes? How do they improve query performance?",
                "category": "SQL",
                "difficulty": "medium",
                "ideal_keywords": ["index", "performance", "query", "search", "B-tree", "lookup", "speed", "column"],
                "ideal_answer": "An index is a data structure that improves the speed of data retrieval operations on a database table. It works like a book index, allowing the database to find rows without scanning the entire table. Common types include B-tree, hash, and full-text indexes. However, indexes slow down write operations and use additional storage.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is normalization? Describe the first three normal forms.",
                "category": "SQL",
                "difficulty": "medium",
                "ideal_keywords": ["normalization", "1NF", "2NF", "3NF", "table", "redundancy", "dependency", "atomic", "primary key", "partial", "transitive"],
                "ideal_answer": "Normalization organizes data to reduce redundancy and improve data integrity. 1NF requires atomic values and a primary key. 2NF requires 1NF plus no partial dependencies (all non-key attributes depend on the whole primary key). 3NF requires 2NF plus no transitive dependencies (non-key attributes don't depend on other non-key attributes).",
            },

            # ===== Machine Learning =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between supervised and unsupervised learning?",
                "category": "Machine Learning",
                "difficulty": "easy",
                "ideal_keywords": ["supervised", "unsupervised", "labeled", "unlabeled", "training", "data", "classification", "regression", "clustering"],
                "ideal_answer": "Supervised learning uses labeled training data where the desired output is known, learning to map inputs to outputs. It's used for classification and regression. Unsupervised learning works with unlabeled data to find hidden patterns or groupings, used for clustering and dimensionality reduction.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is overfitting and how can you prevent it?",
                "category": "Machine Learning",
                "difficulty": "medium",
                "ideal_keywords": ["overfitting", "training", "test", "validation", "regularization", "cross-validation", "dropout", "generalize", "model"],
                "ideal_answer": "Overfitting occurs when a model learns the training data too well, including noise, and fails to generalize to new data. Prevention techniques include: using more training data, regularization (L1/L2), dropout for neural networks, cross-validation, reducing model complexity, and early stopping.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain the bias-variance tradeoff.",
                "category": "Machine Learning",
                "difficulty": "hard",
                "ideal_keywords": ["bias", "variance", "tradeoff", "underfitting", "overfitting", "model", "complexity", "error"],
                "ideal_answer": "Bias is error from oversimplified assumptions (underfitting), while variance is error from too much complexity (overfitting). As model complexity increases, bias decreases but variance increases. The goal is to find the sweet spot that minimizes total error. This balance is the bias-variance tradeoff.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is a confusion matrix and what metrics can be derived from it?",
                "category": "Machine Learning",
                "difficulty": "medium",
                "ideal_keywords": ["confusion matrix", "accuracy", "precision", "recall", "F1", "TP", "TN", "FP", "FN", "true", "false", "positive", "negative"],
                "ideal_answer": "A confusion matrix visualizes classification model performance showing true positives, true negatives, false positives, and false negatives. From these: Accuracy = (TP+TN)/(TP+TN+FP+FN), Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 = 2×(Precision×Recall)/(Precision+Recall).",
            },

            # ===== Data Structures =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between an array and a linked list?",
                "category": "Data Structures",
                "difficulty": "easy",
                "ideal_keywords": ["array", "linked list", "contiguous", "memory", "pointer", "access", "insert", "delete", "O(1)", "O(n)"],
                "ideal_answer": "Arrays store elements in contiguous memory locations allowing O(1) random access but O(n) insertions/deletions. Linked lists store elements in nodes with pointers to the next node, allowing O(1) insertion/deletion at known positions but O(n) random access. Linked lists use more memory due to pointers.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is a hash table and how does it handle collisions?",
                "category": "Data Structures",
                "difficulty": "medium",
                "ideal_keywords": ["hash table", "collision", "chaining", "open addressing", "hash function", "load factor", "rehashing", "linked list"],
                "ideal_answer": "A hash table uses a hash function to compute an index into an array of buckets. Collisions occur when two keys hash to the same index. Two common handling strategies: chaining (each bucket is a linked list of entries) and open addressing (probe for next empty slot using linear, quadratic, or double hashing).",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Explain the time complexity of common operations on a binary search tree.",
                "category": "Data Structures",
                "difficulty": "medium",
                "ideal_keywords": ["BST", "binary search tree", "time complexity", "O(log n)", "O(n)", "insert", "search", "delete", "balanced", "worst case"],
                "ideal_answer": "On a balanced BST: search, insert, and delete are all O(log n). On an unbalanced BST (worst case, e.g., sorted input): all operations degrade to O(n). Keeping the tree balanced (using AVL or Red-Black trees) ensures O(log n) performance.",
            },

            # ===== HR / Behavioral =====
            {
                "id": str(uuid.uuid4()),
                "text": "Tell me about yourself.",
                "category": "HR",
                "difficulty": "easy",
                "ideal_keywords": ["background", "experience", "skills", "career", "goals", "passion", "relevant", "concise", "professional"],
                "ideal_answer": "I am a [your role] with [X years] of experience in [your field]. I specialize in [key skills]. In my previous role at [company], I [achievement]. I am passionate about [relevant topic] and excited about this opportunity because [reason]. My career goal is to [goal].",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are your greatest strengths and weaknesses?",
                "category": "HR",
                "difficulty": "easy",
                "ideal_keywords": ["strength", "weakness", "honest", "improve", "skill", "challenge", "manage", "delegate"],
                "ideal_answer": "My greatest strength is [specific skill] which I've applied to [achievement]. My weakness is [honest weakness] and I've been working on it by [improvement steps]. I recognize it's important to [how it affects work] and I'm actively improving.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Where do you see yourself in 5 years?",
                "category": "HR",
                "difficulty": "easy",
                "ideal_keywords": ["career", "growth", "skills", "contribute", "leadership", "expert", "team", "goals", "company"],
                "ideal_answer": "In 5 years, I see myself as an expert in [field] with deep technical and leadership skills. I want to have led successful projects and grown into a senior role where I can mentor others and contribute strategically to the company's goals while continuing to learn new technologies.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "Why should we hire you?",
                "category": "HR",
                "difficulty": "easy",
                "ideal_keywords": ["hire", "value", "skills", "experience", "culture", "fit", "contribute", "unique", "passion"],
                "ideal_answer": "You should hire me because I bring [specific skills] and [X years] of relevant experience that directly applies to this role. I have a proven track record of [achievement]. I'm passionate about [field] and would bring [positive quality] to your team. My combination of technical skills and [soft skill] makes me a strong fit.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "How do you handle tight deadlines and pressure?",
                "category": "HR",
                "difficulty": "medium",
                "ideal_keywords": ["deadline", "pressure", "stress", "priority", "organize", "time management", "calm", "communicate", "delegate"],
                "ideal_answer": "When facing tight deadlines, I first prioritize tasks by impact and urgency. I break large tasks into smaller chunks and focus on critical paths first. I communicate proactively with stakeholders about progress and any blockers. I stay calm under pressure and believe in working smart rather than just working hard.",
            },

            # ===== Java =====
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between JDK, JRE, and JVM?",
                "category": "Java",
                "difficulty": "easy",
                "ideal_keywords": ["JDK", "JRE", "JVM", "Java", "development", "runtime", "virtual machine", "compiler", "bytecode"],
                "ideal_answer": "JVM (Java Virtual Machine) executes Java bytecode. JRE (Java Runtime Environment) provides the JVM and libraries needed to run Java programs. JDK (Java Development Kit) includes the JRE plus development tools like the compiler and debugger for creating Java applications.",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What are the main principles of Object-Oriented Programming?",
                "category": "Java",
                "difficulty": "easy",
                "ideal_keywords": ["OOP", "object-oriented", "encapsulation", "inheritance", "polymorphism", "abstraction", "class", "object"],
                "ideal_answer": "The four main OOP principles are: Encapsulation (hiding internal details behind a public interface), Inheritance (a class deriving properties from another class), Polymorphism (the ability to take multiple forms), and Abstraction (hiding complex implementation details).",
            },
            {
                "id": str(uuid.uuid4()),
                "text": "What is the difference between abstract class and interface in Java?",
                "category": "Java",
                "difficulty": "medium",
                "ideal_keywords": ["abstract class", "interface", "implements", "extends", "multiple inheritance", "concrete", "method", "field"],
                "ideal_answer": "An abstract class can have both abstract and concrete methods, can have instance variables, and a class can extend only one abstract class. An interface can only have abstract methods (until Java 8+) and a class can implement multiple interfaces. Use abstract class for shared state, interface for behaviors.",
            },
        ]

    def get_by_category(self, category: str) -> List[Dict]:
        """Get all questions in a category"""
        return [q for q in self.questions if q["category"].lower() == category.lower()]

    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        return list(set(q["category"] for q in self.questions))

    def get_random_questions(self, categories: List[str], count: int = 5, difficulty: str = "medium") -> List[Dict]:
        """Get random questions from specified categories, filtered by difficulty"""
        filtered = [
            q for q in self.questions
            if q["category"].lower() in [c.lower() for c in categories]
            and (difficulty == "all" or q["difficulty"] == difficulty)
        ]
        import random
        return random.sample(filtered, min(count, len(filtered)))

    def get_all(self) -> List[Dict]:
        """Get all questions"""
        return self.questions
