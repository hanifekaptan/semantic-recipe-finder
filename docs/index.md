# Semantic Recipe Finder Documentation

!!! tip "Welcome!"
    This application uses natural language semantic search to help you discover recipes intelligently.

## 📚 Documentation Sections

=== "🏗️ Architecture"
    [**System Architecture**](architecture.md)
    
    Learn about the system architecture, data flow, and core technologies powering the semantic search.
    
=== "📖 API Reference"
    [**API Documentation**](api.md)
    
    Complete API documentation with request/response examples and endpoint specifications.


## 🚀 Quick Links

!!! example "Live Resources"
    - 🌐 **Live Demo**: [HuggingFace Spaces](https://huggingface.co/spaces/hanifekaptan/semantic-recipe-finder)
    - 💻 **GitHub Repository**: [semantic-recipe-finder](https://github.com/hanifekaptan/semantic-recipe-finder)
    - 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/hanifekaptan/semantic-recipe-finder/issues)

## ✨ Key Features

=== "🔍 Natural Language"
    Query recipes using everyday language
    
=== "⚡ Fast Vector Search"
    Powered by ChromaDB and sentence-transformers
    
=== "🏗️ Modern Stack"
    FastAPI backend + Streamlit frontend
    
=== "📦 Production Ready"
    Docker support with comprehensive testing
    
=== "✅ Well Documented"
    61 tests with 100% passing rate

## 🎯 Use Cases

!!! success "Recipe Discovery"
    Find recipes based on ingredients, cuisine, or cooking style

!!! success "Dietary Filtering"
    Search for recipes matching specific dietary requirements

!!! success "Time-Based Search"
    Discover quick meals or elaborate dishes

!!! success "Semantic Understanding"
    Natural queries like "healthy vegetarian dinner under 30 minutes"

## 🛠️ Technology Overview

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI 0.115.6 |
| **Frontend** | Streamlit 1.41.1 |
| **ML Model** | sentence-transformers (all-MiniLM-L6-v2) |
| **Vector DB** | ChromaDB 0.5.23 |
| **Testing** | pytest 9.0.2 (61 tests) |
| **Deployment** | Docker, docker-compose |

## 📊 Dataset

???+ info "Dataset Details"
    - 📚 **10000 recipes** from Food.com dataset
    - 🔢 **384-dimensional embeddings** for semantic search
    - 📝 **Rich metadata**: ingredients, instructions, nutrition, ratings
    - 💾 **Persistent storage** with ChromaDB

## 🤝 Getting Help

!!! question "Need Support?"
    - 🐛 **Found a bug?** [Open an issue](https://github.com/hanifekaptan/semantic-recipe-finder/issues)
    - 📧 **Contact**: [hanifekaptan.dev@gmail.com](mailto:hanifekaptan.dev@gmail.com)

## 📄 License

!!! note "License"
    This project is open source and available under the Apache Licence.

---

**Navigation**: [Home](index.md) | [Architecture](architecture.md) | [API](api.md)
