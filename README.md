IndiBots — Codeless AI Chatbot Builder (Django)

IndiBots is a Django-powered chatbot platform that allows anyone to create AI chatbots without writing code.
Users can:

Sign up / log in

Create projects

Add custom Q&A pairs

Upload optional images

Test their chatbot live

Embed the chatbot on any website using a unique script key

The chatbot uses Mistral AI (via OpenRouter) to generate intelligent responses using the user’s saved Q&A.

 Features
 User Authentication (Django Auth)

Register, login, logout

User-specific chatbot projects

Project Management

Each user can:

Create multiple chatbot projects

Edit existing chatbot configurations

Delete or update Q&A pairs

Codeless Q&A Builder

Add unlimited questions

Add answers

Upload related images

Q&A stored in database

Unique bot key auto-generated

AI Response Engine (Mistral via OpenRouter)

When a user tests or embeds the chatbot:

Question + Q&A context is sent to Mistral AI

AI replies using user-specific data

Frontend displays clean, formatted response
 Chatbot Testing Panel

Users can test:

Actual responses

Flow accuracy

Context understanding

One-Line Website Integration

Every project has a unique API key.

Embed the chatbot anywhere using:

<script src="https://yourdomain.com/indibots/embed.js?bot_key=YOUR_UNIQUE_KEY"></script>


Works on:

HTML websites

Django

WordPress

Shopify

Wix / Webflow

Any CMS

🏗️ Architecture (Django Version)
                ┌──────────────────────────┐
                │       Django Auth        │
                │   Signup / Login / JWT   │
                └───────────────┬──────────┘
                                │
                ┌───────────────▼──────────────┐
                │        User Dashboard         │
                │  • Create Project             │
                │  • Edit Project               │
                └───────────────┬──────────────┘
                                │
                ┌───────────────▼─────────────┐
                │     Q&A Builder (Django)     │
                │ • Add Q&A pairs              │
                │ • Upload images              │
                │ • Save to DB                 │
                └───────────────┬─────────────┘
                                │
                ┌───────────────▼─────────────┐
                │   Unique Bot Key Generator   │
                │   • UUID stored in DB        │
                └───────────────┬─────────────┘
                                │
                ┌───────────────▼─────────────────┐
                │       Test Chatbot (HTML/JS)     │
                │  ✔ Q&A + user question → API     │
                │  ✔ Mistral via OpenRouter        │
                │  ✔ Response returned             │
                └─────────────────┬────────────────┘
                                  │
                ┌─────────────────▼─────────────────┐
                │     Embed Script (JS Widget)       │
                │ • Loads chatbot UI                 │
                │ • Uses bot_key                     │
                │ • Sends requests to Django API     │
                └────────────────────────────────────┘
