# 🚀 FinGuru

# AI-Powered Hyper-Personalized Banking for Bharat

> **FinGuru doesn't ask what product we can sell the customer; it asks what the customer needs next.**

FinGuru is an **event-driven AI financial copilot** that sits on top of an API-driven banking core. It builds a real-time financial profile of each customer, analyzes financial health and security risks, predicts financial needs, simulates future financial outcomes, and recommends the safest **Next Best Action** through an explainable and vernacular AI interface.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [The Gap in Existing Banking](#-the-gap-in-existing-banking)
- [Our Solution](#-our-solution)
- [Core Innovation](#-core-innovation)
- [Key Features](#-key-features)
- [System Architecture](#️-system-architecture)
- [End-to-End Data Flow](#-end-to-end-data-flow)
- [Customer 360](#-customer-360)
- [Financial Intelligence](#-financial-intelligence)
- [Financial Health Engine](#-financial-health-engine)
- [Financial Stress Engine](#-financial-stress-engine)
- [Customer Segmentation](#-customer-segmentation)
- [Life-Event Detection](#-life-event-detection)
- [Loan Risk and Suitability](#-loan-risk-and-suitability)
- [Financial Digital Twin](#-financial-digital-twin)
- [Security Intelligence](#-security-intelligence)
- [Fraud Detection](#-fraud-detection)
- [UEBA](#-ueba)
- [Identity Risk](#-identity-risk)
- [Transaction Anomaly Detection](#-transaction-anomaly-detection)
- [Threat Correlation](#-threat-correlation)
- [Incident Response](#-incident-response)
- [Prescriptive Engine](#-prescriptive-engine)
- [Recommendation Engine](#-recommendation-engine)
- [Next Best Action](#-next-best-action)
- [Multi-Agent AI](#-multi-agent-ai)
- [LLM Decision-Safety Architecture](#-llm-decision-safety-architecture)
- [RAG](#-retrieval-augmented-generation-rag)
- [Vernacular AI](#-vernacular-ai)
- [Event-Driven Architecture](#-event-driven-architecture)
- [Privacy Architecture](#-privacy-architecture)
- [Consent Management](#-consent-management)
- [Data Minimization](#-data-minimization)
- [PII Detection](#-pii-detection)
- [Tokenization and Masking](#-tokenization-and-masking)
- [Security Architecture](#-security-architecture)
- [AI Governance](#-ai-governance)
- [Database Architecture](#-database-architecture)
- [API Architecture](#-api-architecture)
- [API Reference](#-api-reference)
- [Main AI Orchestration API](#-main-ai-orchestration-api)
- [Loan Simulation](#-loan-simulation)
- [Project Structure](#-project-structure)
- [Technology Stack](#️-technology-stack)
- [Installation](#-installation)
- [Environment Configuration](#-environment-configuration)
- [Database Setup](#-database-setup)
- [Data Generation](#-data-generation)
- [Feature Engineering](#-feature-engineering)
- [Running the Backend](#-running-the-backend)
- [Running the Frontend](#-running-the-frontend)
- [Testing](#-testing)
- [Demo Journey](#-demo-journey)
- [Hackathon Demo Scenario](#-hackathon-demo-scenario)
- [48-Hour Architecture](#-48-hour-hackathon-architecture)
- [Production Architecture](#-production-architecture)
- [Current Implementation Status](#-current-implementation-status)
- [Known Limitations](#-known-limitations)
- [Future Scope](#-future-scope)
- [Responsible AI](#-responsible-ai)
- [Why FinGuru Is Different](#-why-finguru-is-different)
- [Key Innovation Statements](#-key-innovation-statements)
- [Conclusion](#-conclusion)

---

# 📌 Project Overview

Traditional banking systems are excellent at processing transactions, maintaining accounts, managing loans, and executing payments.

However, most banking experiences remain **transaction-centric and product-centric**.

FinGuru introduces an intelligence layer above banking infrastructure.

Instead of asking:

> "Which product should we sell?"

FinGuru asks:

> **"What does this customer need next?"**

The system combines:

- Customer 360
- Financial intelligence
- Security intelligence
- Machine learning
- Prescriptive analytics
- Digital twin simulation
- Multi-agent AI
- RAG
- Policy guardrails
- Privacy controls
- Event-driven processing
- Explainable AI
- Vernacular interaction

---

# 🎯 Problem Statement

The banking ecosystem has access to large amounts of customer information:

- Transactions
- Salary information
- EMI history
- Spending behaviour
- Savings behaviour
- Loan history
- Account balances
- Device activity
- Location information

Yet customers frequently receive generic financial recommendations.

FinGuru addresses three major problems.

## Problem 1 — Generic Banking

Traditional banking systems often focus on:

```text
Customer
   ↓
Transaction
   ↓
Product Eligibility
   ↓
Product Recommendation
```

FinGuru changes this to:

```text
Customer
   ↓
Customer 360
   ↓
Financial State
   ↓
Need Prediction
   ↓
Risk Evaluation
   ↓
Affordability
   ↓
Simulation
   ↓
Next Best Action
```

## Problem 2 — Complex Banking Journeys

Customers may struggle with:

- Loan applications
- EMI decisions
- Understanding financial products
- Banking terminology
- Financial planning
- KYC processes
- English-centric banking interfaces

FinGuru provides conversational and explainable assistance.

## Problem 3 — Financial Stress and Fraud Are Detected Too Late

Financial stress can emerge from:

```text
Income ↓
   +
Spending ↑
   +
Balance ↓
   +
EMI Missed
   ↓
Financial Stress
```

Security threats can emerge from:

```text
New Device
     +
New Location
     +
New Beneficiary
     +
Large Transaction
     ↓
Possible Account Takeover
```

FinGuru attempts to detect these signals early and recommend appropriate intervention.

---

# 💡 The Gap in Existing Banking

| Traditional Banking | FinGuru |
|---|---|
| Transaction-centric | Customer-state-centric |
| Product-centric | Need-centric |
| Reactive | Proactive |
| Generic offers | Personalized next-best action |
| Eligibility-focused | Suitability-focused |
| Loan calculator | Financial Digital Twin |
| Fraud after event | Behavioral early detection |
| Chatbot | Financial Copilot |
| English-heavy | Vernacular-ready |
| Black-box recommendation | Explainable recommendation |
| Product pushing | Can recommend WAIT |
| Data collected silently | Customer Data Control |
| Financial security separated | Financial + Security Intelligence |

---

# 💡 Our Solution

FinGuru follows the following intelligence pipeline:

```text
                    BANKING DATA
                         ↓
                   CUSTOMER 360
                         ↓
                  FINANCIAL STATE
                         ↓
               NEED / RISK PREDICTION
                         ↓
                 PRESCRIPTIVE ENGINE
                         ↓
                  NEXT BEST ACTION
                         ↓
              EXPLAINABLE AI COPILOT
```

The system combines financial and security intelligence before making important recommendations.

---

# ⭐ Core Innovation

FinGuru is **not**:

- A banking app with a chatbot
- A simple loan calculator
- A product recommendation engine
- A fraud detection system
- An LLM wrapper

FinGuru is:

> **An AI-powered, event-driven financial intelligence layer over modern banking infrastructure.**

---

# 🚀 Key Features

## Financial Intelligence

- Financial Health Score
- Financial Stress Prediction
- Customer Segmentation
- Life-Event Detection
- Loan Risk Evaluation
- Loan Suitability
- Financial Digital Twin
- Financial forecasting foundation

## Security Intelligence

- Fraud Detection
- Transaction Anomaly Detection
- UEBA
- Identity Risk
- Threat Correlation
- Account Takeover Detection
- Security Incident Response
- Audit Logging

## AI

- Multi-Agent AI
- Financial Agent
- Risk & Security Agent
- Recommendation Agent
- Communication Agent
- RAG
- Explainable AI
- Vernacular AI

## Privacy

- Consent Management
- Purpose Limitation
- PII Detection
- Data Minimization
- Tokenization
- Data Masking
- Audit Logging

## Event Processing

- Salary Events
- EMI Events
- Large Transaction Events
- Device Events
- Beneficiary Events
- Spending Events
- Balance Events

---

# 🏗️ System Architecture

```text
                         CUSTOMER
                  Web / Mobile / Voice
                           │
                           ▼
                ┌──────────────────────┐
                │   SECURE API GATEWAY │
                │                      │
                │ HTTPS / TLS          │
                │ JWT / OAuth          │
                │ MFA / RBAC           │
                │ Rate Limiting        │
                │ Authorization        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     BANKING CORE     │
                │                      │
                │ Customer             │
                │ Accounts             │
                │ Transactions         │
                │ Loans                │
                │ Payments             │
                └──────────┬───────────┘
                           │
                      APIs + EVENTS
                           │
                           ▼
                ┌──────────────────────┐
                │     CUSTOMER 360     │
                │                      │
                │ Income               │
                │ Spending             │
                │ Savings              │
                │ Loans                │
                │ EMI                  │
                │ Behaviour            │
                └──────────┬───────────┘
                           │
                ┌──────────┴───────────┐
                │                      │
                ▼                      ▼
       FINANCIAL INTELLIGENCE    SECURITY INTELLIGENCE
                │                      │
        ┌───────┼────────┐     ┌───────┼────────┐
        │       │        │     │       │        │
      Health  Stress  Segmentation Fraud  UEBA  Identity
        │       │        │     │       │        │
      Loan   Digital  Life Events  Anomaly  Threat
      Risk    Twin                  Detection Correlation
        │       │                       │
        └───────┴──────────────┬────────┘
                               │
                               ▼
                     PRESCRIPTIVE ENGINE
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
               Predict      Evaluate      Simulate
                 │             │             │
                 └─────────────┬─────────────┘
                               │
                               ▼
                       MULTI-AGENT AI
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         Financial       Risk & Security   Recommendation
           Agent             Agent             Agent
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                      Communication Agent
                               │
                               ▼
                   POLICY + PRIVACY GUARDRAIL
                               │
                               ▼
                          RAG + LLM
                               │
                               ▼
                        AI COPILOT
                               │
                               ▼
                      NEXT BEST ACTION
                               │
              ┌────────┬───────┼───────┬────────┐
              ▼        ▼       ▼       ▼        ▼
             SAVE     WAIT    WARN    APPLY   SEEK HELP
```

---

# 🔄 End-to-End Data Flow

```text
Banking Data
     ↓
Data Ingestion
     ↓
Customer 360
     ↓
Feature Engineering
     ↓
Financial Intelligence
     ↓
Security Intelligence
     ↓
Need + Risk Prediction
     ↓
Prescriptive Engine
     ↓
Multi-Agent Reasoning
     ↓
Policy & Privacy Guardrails
     ↓
RAG / LLM
     ↓
Explainable Response
     ↓
Next Best Action
```

---

# 👤 Customer 360

Customer 360 creates a unified view of the customer.

It combines:

- Customer profile
- Accounts
- Balances
- Transactions
- Spending
- Income
- Loans
- EMI history
- Missed EMIs
- Financial features
- Financial health
- Financial stress

Example:

```text
Customer 360
│
├── Customer Profile
│   ├── Name
│   ├── Email
│   ├── Phone
│   ├── City
│   └── Occupation
│
├── Accounts
│   ├── Account Count
│   └── Total Balance
│
├── Transactions
│   ├── Transaction Count
│   ├── Total Spending
│   └── Categories
│
├── Loans
│   ├── Active Loans
│   ├── Outstanding Amount
│   └── EMI
│
├── Features
│   ├── Savings Rate
│   ├── EMI Ratio
│   ├── Spending Growth
│   └── Income Stability
│
└── Intelligence
    ├── Financial Health
    └── Financial Stress
```

---

# 🧠 Financial Intelligence

FinGuru's financial intelligence layer contains:

```text
Financial Health
Financial Stress
Customer Segmentation
Life Events
Loan Suitability
Digital Twin
Recommendation Signals
```

---

# 💚 Financial Health Engine

The Financial Health Engine produces a score between:

```text
0 – 100
```

It evaluates:

- Monthly income
- Monthly spending
- Savings rate
- EMI ratio
- Balance volatility
- Spending growth
- Transaction frequency
- Credit utilization
- Missed EMI count
- Income stability
- Cash buffer

The scoring framework combines:

```text
Income
   +
Spending Stability
   +
Savings
   +
Debt Health
   +
Income Stability
   +
Emergency Buffer
```

### Health Levels

```text
80+     EXCELLENT
65–79   GOOD
50–64   MODERATE
35–49   AT_RISK
<35     CRITICAL
```

The system also provides explainability.

Example:

```text
Financial Health: 78

Strengths:
+ Stable salary
+ Healthy savings
+ Low debt

Weaknesses:
- Spending increased
- EMI ratio elevated
```

---

# 😰 Financial Stress Engine

Financial stress is calculated using multiple signals:

- Spending pressure
- Debt pressure
- Savings pressure
- Income instability
- Spending growth
- Cash buffer
- Payment behaviour
- Balance volatility

Output:

```text
Stress Score
Stress Level
Stress Factors
```

Levels:

```text
0–20      LOW
21–40     MODERATE
41–60     HIGH
61–80     VERY_HIGH
81–100    CRITICAL
```

The important design principle is:

> Financial stress should lead to support-oriented intervention rather than automatically punitive action.

---

# 👥 Customer Segmentation

FinGuru uses customer behavioural and financial features for segmentation.

The prototype uses:

```text
StandardScaler
      ↓
K-Means
      ↓
5 Customer Segments
```

Potential segments include:

```text
Young Salaried
High Savers
Credit Dependent
Financially Stressed
High-Value Stable
```

Segmentation is treated as **one input** to recommendations rather than the sole decision factor.

---

# 📅 Life-Event Detection

FinGuru detects meaningful financial events such as:

```text
SALARY_CREDITED
INCOME_DECREASE
INCOME_INCREASE
SPENDING_SPIKE
LARGE_PURCHASE
BALANCE_DROP
NEW_BENEFICIARY
```

Example:

```text
Salary credited
       ↓
Income event
       ↓
Financial state updated
       ↓
Recommendation recalculated
```

---

# 💳 Loan Risk and Suitability

FinGuru goes beyond traditional loan eligibility.

It evaluates:

- Proposed EMI
- Existing EMI
- EMI-to-income ratio
- Projected surplus
- Savings rate
- Income stability
- Missed EMI count
- Cash buffer
- Existing outstanding loans

Example:

```text
Loan Amount       ₹3,00,000
Tenure            36 months
Interest Rate     12%

Proposed EMI      ₹9,964
Projected EMI     41%
Projected Surplus Negative

Risk              VERY HIGH
Suitability       NOT SUITABLE
Recommendation     WAIT
```

The objective is:

```text
Eligibility ≠ Suitability
```

---

# 🔮 Financial Digital Twin

The Digital Twin is one of FinGuru's headline features.

A customer asks:

> "Can I take ₹3 lakh loan?"

Traditional systems may answer whether the customer qualifies.

FinGuru asks:

> "What happens to your financial health if you take the loan?"

### Current State

```text
Income
Expenses
Existing EMI
Savings
Health Score
Stress Score
Cash Buffer
```

### Simulation

```text
New Loan
   ↓
New EMI
   ↓
Total EMI
   ↓
Projected Surplus
   ↓
Projected Cash Buffer
   ↓
Projected Health
   ↓
Projected Stress
```

Example:

```text
CURRENT

Health Score       78
Monthly Surplus    ₹25,000
Cash Buffer        ₹1,80,000

            ↓

NEW LOAN

New EMI            ₹14,500
Total EMI          ₹22,500

            ↓

PROJECTED

Health Score       68
Surplus            ₹10,500
Stress Risk        HIGH

            ↓

RECOMMENDATION

WAIT
```

Example explanation:

> "You may qualify, but we recommend waiting because the loan would significantly reduce your monthly financial buffer."

---

# 🔐 Security Intelligence

FinGuru treats security as a first-class intelligence layer.

```text
Fraud
UEBA
Identity Risk
Transaction Anomaly
Threat Correlation
Incident Response
Audit
```

---

# 🚨 Fraud Detection

The prototype combines statistical analysis and behavioural rules.

Features include:

- Transaction amount
- Transaction frequency
- Merchant
- Location
- Device
- Beneficiary
- Historical average
- Behavioural deviation
- Security rules

Example:

```text
Normal Transaction
₹2,000 – ₹5,000

Current Transaction
₹85,000

+

New Device

+

New Location

+

New Beneficiary

+

Unusual Time

↓

High Fraud Risk
```

Possible actions:

```text
ALLOW_TRANSACTION
REVIEW_TRANSACTION
STEP_UP_AUTHENTICATION
BLOCK_TRANSACTION
BLOCK_AND_ESCALATE
```

---

# 🔍 UEBA

UEBA means:

> **User and Entity Behaviour Analytics**

FinGuru compares current activity against the customer's historical behaviour.

Signals include:

- Amount deviation
- Frequency deviation
- Location behaviour
- Device behaviour
- Beneficiary behaviour

The goal is to detect behaviour that is unusual for **that specific customer**.

---

# 🪪 Identity Risk

Identity Risk evaluates signals related to possible account takeover.

Examples:

```text
New Device
New Location
Failed Login Pattern
New Beneficiary
Unusual Transaction
```

These signals are combined with transaction and behavioural intelligence.

---

# 📊 Transaction Anomaly Detection

Transaction anomaly detection compares a transaction against the customer's historical transaction behaviour.

Example:

```text
Historical Average
₹8,697

Current Transaction
₹9,500

↓

Low Anomaly
```

versus:

```text
Historical Average
₹8,697

Current Transaction
₹85,000

+

New Device

+

New Location

↓

High Anomaly
```

---

# 🔗 Threat Correlation

Individual security signals are not always sufficient.

FinGuru correlates multiple signals.

Example:

```text
New Device
      +
New Location
      +
New Beneficiary
      +
Large Transfer
      +
Unusual Behaviour
      ↓
CRITICAL ACCOUNT TAKEOVER RISK
```

This provides a more complete security assessment.

---

# 🚑 Incident Response

When security risk crosses the configured threshold:

```text
Detection
    ↓
Risk Score
    ↓
Incident Created
    ↓
Evidence Timeline
    ↓
Customer Verification
    ↓
Human Escalation
    ↓
Resolution
    ↓
Audit Log
```

Example:

```text
INCIDENT

02:21  New device
02:23  Failed logins
02:26  Successful login
02:27  New beneficiary
02:30  ₹85,000 transfer
02:30  Risk = HIGH / CRITICAL
02:31  Transaction restricted
02:32  Customer notified
```

---

# 🧮 Prescriptive Engine

The Prescriptive Engine is responsible for:

```text
Predict
Evaluate
Simulate
Recommend
```

It transforms predictions into actions.

```text
Financial State
       +
Risk
       +
Need
       +
Affordability
       +
Suitability
       +
Timing
       +
Policy
       ↓
Recommendation
```

---

# 🎯 Recommendation Engine

FinGuru does not use simplistic rules such as:

```text
IF income > ₹50,000
THEN recommend loan
```

Instead:

```text
Customer State
       +
Need Prediction
       +
Affordability
       +
Risk
       +
Customer Segment
       +
Product Suitability
       +
Timing
       +
Policy
       ↓
Recommendation Score
```

Recommendation signals include:

- Need score
- Affordability
- Suitability
- Timing
- Customer preference
- Financial health
- Risk
- Financial stress

---

# 🎯 Next Best Action

The final action can be:

```text
SAVE
WAIT
WARN
APPLY
SEEK_HELP
NO_ACTION
```

This is one of FinGuru's most important design decisions.

The system is allowed to tell a customer:

> **WAIT**

or:

> **NO ACTION**

instead of always recommending a banking product.

---

# 🤖 Multi-Agent AI

FinGuru uses four primary agents.

```text
                  AI ORCHESTRATOR
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
 Financial Agent   Risk Agent   Recommendation Agent
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼
                Communication Agent
```

## Agent 1 — Financial Analyst

Understands:

- Income
- Spending
- Savings
- Debt
- Financial health
- Financial stress
- Life events
- Loan simulation

## Agent 2 — Risk & Security

Understands:

- Fraud
- Transaction anomalies
- UEBA
- Identity risk
- Account takeover
- Threat correlation
- Security incidents

## Agent 3 — Recommendation

Combines financial and security information and determines the appropriate action.

Possible outputs:

```text
SAVE
WAIT
WARN
APPLY
HELP
NO ACTION
```

## Agent 4 — Communication

Converts decisions into:

- Simple explanations
- Conversational responses
- Vernacular responses
- Voice-ready responses

---

# 🛡️ LLM Decision-Safety Architecture

The LLM is **not the final banking decision maker**.

FinGuru follows:

```text
ML MODELS
     ↓
NUMERICAL SIGNALS
     ↓
AI AGENTS
     ↓
POLICY ENGINE
     ↓
FINAL DECISION
     ↓
LLM
     ↓
HUMAN-FRIENDLY EXPLANATION
```

### Core Safety Principle

> **ML decides the numbers. Agents reason over the numbers. Rules enforce policy. LLM communicates the decision.**

This separation reduces the risk of allowing a generative model to directly control financial actions.

---

# 📚 Retrieval-Augmented Generation (RAG)

FinGuru uses RAG for trusted financial information.

Knowledge sources include:

- Banking FAQs
- Loan documents
- KYC information
- Financial literacy
- Banking products
- Policies

Pipeline:

```text
Banking Documents
       ↓
Document Loader
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
Retriever
       ↓
LLM
       ↓
Grounded Answer
```

The prototype uses:

```text
ChromaDB
Sentence Transformers
all-MiniLM-L6-v2
```

---

# 🌐 Vernacular AI

FinGuru is designed for multilingual interaction.

Initial languages:

```text
English
Hindi
Gujarati
```

Conceptual pipeline:

```text
Voice
  ↓
Speech-to-Text
  ↓
Intent Detection
  ↓
Financial Agent
  ↓
Policy / RAG
  ↓
LLM
  ↓
Translation
  ↓
Text-to-Speech
```

Example:

> "Mera EMI next week hai, kya main ₹3 lakh ka loan le sakta hoon?"

The system should evaluate the customer's actual financial state rather than returning a generic loan answer.

---

# ⚡ Event-Driven Architecture

FinGuru supports event-driven financial and security processing.

Supported events include:

```text
SALARY_CREDITED
EMI_DUE
EMI_MISSED
LARGE_TRANSACTION
NEW_DEVICE
NEW_BENEFICIARY
SPENDING_SPIKE
BALANCE_DROP
```

Instead of continuously polling banking data:

```text
GET /transactions
GET /transactions
GET /transactions
```

the system can respond to events:

```text
Transaction
    ↓
Event
    ↓
Intelligence
    ↓
Risk
    ↓
Policy
    ↓
Action
```

### Prototype

The prototype uses Python-based event processing with optional Redis Streams support.

### Production

A production architecture can use:

```text
Kafka
or
Managed Event Streaming
```

---

# 🔒 Privacy Architecture

Privacy is implemented as a processing layer rather than only a documentation statement.

```text
Raw Data
   ↓
PII Detection
   ↓
Classification
   ↓
Consent Check
   ↓
Purpose Check
   ↓
Data Minimization
   ↓
Mask / Tokenize
   ↓
ML / AI
```

---

# ✅ Consent Management

FinGuru supports purpose-based consent.

Current purposes include:

```text
financial_analysis
financial_advice
loan_recommendation
fraud_detection
```

A customer can:

- Grant consent
- Revoke consent
- Check consent status

The recommendation pipeline can be restricted when consent is not available.

---

# 📉 Data Minimization

Only data necessary for the requested purpose should be passed to downstream intelligence systems.

Example:

```text
Raw Customer Data
       ↓
Purpose Check
       ↓
Required Fields Only
       ↓
ML / AI
```

---

# 🔎 PII Detection

FinGuru includes PII detection for sensitive information.

Potential categories include:

- Phone numbers
- Email addresses
- Account numbers
- Customer identifiers

PII should not be unnecessarily exposed to AI components.

---

# 🔑 Tokenization and Masking

Sensitive values can be transformed before processing.

Example:

```text
Original:

9876543210

↓

Tokenized:

TKN_A1B2C3D4E5F6...
```

This allows downstream systems to work with references rather than unnecessarily exposing raw sensitive values.

---

# 🛡️ Security Architecture

Security is divided into multiple layers.

## Identity

```text
JWT
MFA
RBAC
Zero Trust
```

## Data

```text
Encryption
PII Masking
DLP
DSPM
Database Security
```

## Behavioural Security

```text
Fraud ML
UEBA
Identity Risk
Transaction Anomaly
```

## Detection

```text
Threat Correlation
SIEM-inspired correlation
Threat Intelligence
```

## Response

```text
SOAR-inspired playbooks
Incident Response
Evidence Timeline
Human Escalation
```

## Infrastructure

```text
WAF
Rate Limiting
DDoS Protection
Cloud Security
```

---

# 🧾 Audit Logging

Important security and policy actions should be auditable.

Audit records can capture:

```text
User
Customer
Action
Resource
IP Address
Details
Timestamp
```

Example:

```text
Customer requested loan simulation
        ↓
Loan evaluated
        ↓
Recommendation generated
        ↓
Policy evaluated
        ↓
Decision recorded
```

---

# ⚖️ AI Governance

FinGuru is designed with responsible AI principles.

Governance metrics include:

```text
Model Version
Accuracy
Precision
Recall
F1
False Positive Rate
Drift
Bias Check
Confidence Threshold
Human Escalation
```

Important:

> Actual model metrics should be reported from the models trained and tested for FinGuru. Published research metrics should not be presented as FinGuru's own results.

---

# 🗄️ Database Architecture

The current prototype uses SQLite for local development.

The production target is PostgreSQL.

Core entities include:

```text
users
customers
accounts
transactions
loans
emi_records
customer_features
financial_health
financial_stress
fraud_events
recommendations
consents
audit_logs
incidents
products
```

### Customer

```text
id
user_id
customer_code
full_name
email
phone
date_of_birth
city
occupation
monthly_income
created_at
```

### Account

```text
id
customer_id
account_number
account_type
balance
currency
status
created_at
```

### Transaction

```text
id
customer_id
account_id
transaction_type
amount
merchant
category
location
device_id
beneficiary
description
timestamp
```

### Loan

```text
id
customer_id
principal
interest_rate
tenure
emi
status
```

---

# 🔌 API Architecture

The backend follows:

```text
Frontend
   ↓
FastAPI
   ↓
API Routers
   ↓
Services
   ↓
ML / AI
   ↓
Database
```

---

# 📡 API Reference

## Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
GET  /auth/admin-check
```

## Customer

```http
GET /customers/{customer_id}
```

## Accounts

```http
GET /accounts/{account_id}
GET /accounts/customer/{customer_id}
GET /accounts/{account_id}/balance
GET /accounts/customer/{customer_id}/balance
```

## Transactions

```http
GET  /transactions/customer/{customer_id}
GET  /transactions/{transaction_id}
POST /transactions
```

## Financial Health

```http
GET /customers/{customer_id}/financial-health
GET /customers/{customer_id}/financial-health/latest
```

## Financial Stress

```http
GET /customers/{customer_id}/financial-stress
GET /customers/{customer_id}/financial-stress/latest
```

## Recommendations

```http
GET /recommendations/{customer_id}
```

## Personalized Offers

```http
GET /offers/{customer_id}
```

## Loans

```http
POST /loan/simulate
```

## Fraud

```http
POST /fraud/analyze
POST /fraud/analyze-batch
GET  /fraud/transaction/{transaction_id}
```

## Events

```http
GET  /events/types
POST /events
POST /events/publish
POST /events/process
```

## Incidents

```http
GET /incidents
GET /incidents/{incident_id}
```

## Consent

```http
GET  /customers/{customer_id}/data-consent
POST /customers/{customer_id}/consent
```

## AI Orchestrator

```http
POST /ai/orchestrate
```

## Copilot

```http
POST /copilot/chat
```

---

# 🤖 Main AI Orchestration API

The most important AI endpoint is:

```http
POST /ai/orchestrate
```

Example request:

```json
{
  "customer_id": 1,
  "loan_requested": true,
  "loan_amount": 300000,
  "tenure_months": 36,
  "interest_rate": 12,
  "language": "English"
}
```

The orchestration flow is:

```text
Customer
    ↓
Financial Agent
    ↓
Risk & Security Agent
    ↓
Recommendation Agent
    ↓
Policy Engine
    ↓
Communication Agent
```

The response contains:

```text
Customer
Financial Analysis
Security Analysis
Recommendation
Policy
Communication
Final Decision
```

---

# 💳 Loan Simulation

Endpoint:

```http
POST /loan/simulate
```

Example:

```json
{
  "customer_id": 1,
  "loan_amount": 300000,
  "tenure_months": 24,
  "interest_rate": 12
}
```

Conceptual response:

```json
{
  "current_health_score": 78,
  "projected_health_score": 68,
  "current_monthly_surplus": 25000,
  "projected_monthly_surplus": 10500,
  "stress_risk": "HIGH",
  "recommendation": "WAIT",
  "reason": [
    "EMI ratio becomes high",
    "Emergency buffer decreases"
  ]
}
```

---

# 📁 Project Structure

```text
FinGuru/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── ai.py
│   │   │   ├── customers.py
│   │   │   ├── accounts.py
│   │   │   ├── transactions.py
│   │   │   ├── financial_health.py
│   │   │   ├── financial_stress.py
│   │   │   ├── fraud.py
│   │   │   ├── recommendations.py
│   │   │   ├── offers.py
│   │   │   ├── loans.py
│   │   │   ├── incidents.py
│   │   │   ├── consent.py
│   │   │   ├── events.py
│   │   │   └── copilot.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   ├── agents/
│   │   │   ├── financial_agent.py
│   │   │   ├── risk_agent.py
│   │   │   ├── recommendation_agent.py
│   │   │   ├── communication_agent.py
│   │   │   └── orchestrator.py
│   │   ├── rag/
│   │   ├── llm/
│   │   ├── policy/
│   │   ├── privacy/
│   │   ├── events/
│   │   ├── security/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   ├── .env
│   └── finguru.db
│
├── data/
│   ├── customers.csv
│   ├── transactions.csv
│   ├── accounts.csv
│   ├── loans.csv
│   ├── emi_records.csv
│   ├── fraud_events.csv
│   ├── events.json
│   └── products.json
│
├── ml_models/
│
├── rag_data/
│   ├── banking_faqs/
│   ├── loan_documents/
│   ├── kyc_documents/
│   ├── financial_literacy/
│   └── products/
│
├── vector_store/
│   └── chroma/
│
├── frontend/
│
├── tests/
│
├── scripts/
│   ├── seed_database.py
│   ├── generate_data.py
│   ├── train_models.py
│   ├── calculate_features.py
│   ├── calculate_health.py
│   ├── calculate_stress.py
│   ├── build_vector_store.py
│   └── simulate_events.py
│
└── README.md
```

---

# 🛠️ Technology Stack

## Frontend

```text
Next.js
React
Tailwind CSS
Recharts
Lucide Icons
```

## Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
Uvicorn
JWT
```

## Database

```text
SQLite
PostgreSQL (production target)
```

## Machine Learning

```text
Pandas
NumPy
Scikit-learn
XGBoost
Joblib
```

## AI

```text
LangGraph
LangChain
LLM
RAG
```

## Vector Database

```text
ChromaDB
Sentence Transformers
```

## Security

```text
JWT
RBAC
PII Detection
PII Masking
Tokenization
Consent
Audit Logging
Fraud Detection
UEBA
Identity Risk
Threat Correlation
```

## Deployment

```text
Docker
GitHub
Cloud
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd FinGuru
```

## 2. Create Virtual Environment

```bash
python3 -m venv backend/venv
```

Activate:

### macOS / Linux

```bash
source backend/venv/bin/activate
```

### Windows

```bash
backend\venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# ⚙️ Environment Configuration

Create:

```text
backend/.env
```

Example:

```env
FINGURU_JWT_SECRET=change-this-secret
FINGURU_TOKEN_SECRET=change-this-token-secret

OPENAI_API_KEY=your-api-key

FINGURU_LLM_MODEL=gpt-5.6-luna

DATABASE_URL=sqlite:///./finguru.db
```

Do not commit secrets to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# 🗄️ Database Setup

Initialize the database:

```bash
cd backend
python -m app.init_db
```

The current prototype uses:

```text
SQLite
```

Production architecture can use:

```text
PostgreSQL
```

---

# 📊 Data Generation

Synthetic banking data can be generated using:

```bash
python scripts/generate_data.py
```

The project uses synthetic customer and transaction data for development and demonstration.

---

# 🌱 Seed Database

Seed the database:

```bash
python scripts/seed_database.py
```

The development dataset contains customer banking information such as:

```text
Customers
Accounts
Transactions
Loans
EMI Records
Fraud Events
Products
```

---

# ⚙️ Feature Engineering

Run:

```bash
python scripts/calculate_features.py
```

This calculates:

```text
avg_monthly_income
avg_monthly_spending
savings_rate
cash_buffer
emi_ratio
credit_utilization
missed_emi_count
transaction_frequency
spending_growth
balance_volatility
income_stability
```

---

# 💚 Calculate Financial Health

Run:

```bash
python scripts/calculate_health.py
```

---

# 😰 Calculate Financial Stress

Run:

```bash
python scripts/calculate_stress.py
```

---

# 📚 Build RAG Vector Store

Build the ChromaDB vector store:

```bash
python scripts/build_vector_store.py
```

The pipeline is:

```text
Documents
    ↓
Loader
    ↓
Chunker
    ↓
Embeddings
    ↓
ChromaDB
```

---

# ▶️ Running the Backend

From the project root:

```bash
cd ~/Desktop/FinGuru
source backend/venv/bin/activate
cd backend
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🖥️ Running the Frontend

Once the frontend is configured:

```bash
cd frontend
npm install
npm run dev
```

The frontend communicates with the FastAPI backend.

Conceptually:

```text
Next.js
   ↓
FastAPI
   ↓
FinGuru Intelligence
```

---

# 🧪 Testing

The project includes tests for major intelligence components.

Examples:

```text
Financial Health
Financial Stress
Fraud Detection
Loan Risk
Digital Twin
Recommendations
Privacy
Events
RAG
UEBA
Identity Risk
Threat Correlation
Incident Response
Policy Engine
Multi-Agent Orchestrator
```

Run the Python test suite:

```bash
pytest
```

For API testing, use:

```text
http://127.0.0.1:8000/docs
```

---

# 🎬 Demo Journey

The primary customer journey is:

```text
LOGIN
   ↓
CUSTOMER DASHBOARD
   ↓
Financial Health
   ↓
Customer asks:
"Can I take ₹3 lakh loan?"
   ↓
DIGITAL TWIN
   ↓
Future Financial State
   ↓
Health / Stress Impact
   ↓
AI Recommendation
   ↓
WAIT
   ↓
Customer asks:
"WHY?"
   ↓
Explainability
   ↓
Gujarati / Hindi
   ↓
Suspicious Transaction
   ↓
Fraud Alert
   ↓
Threat Correlation
   ↓
Security Response
   ↓
Incident
```

---

# 🏆 Hackathon Demo Scenario

## Scenario 1 — Financial Health

Dashboard displays:

```text
Financial Health
78 / 100
```

With explanations:

```text
+ Stable income
+ Healthy savings
+ Low debt

- Spending increased
```

## Scenario 2 — Loan Question

Customer asks:

> "Can I take ₹3 lakh loan?"

FinGuru runs:

```text
Customer 360
      ↓
Financial Health
      ↓
Financial Stress
      ↓
Loan Risk
      ↓
Digital Twin
      ↓
Projected State
      ↓
Recommendation
```

Output:

```text
Recommendation: WAIT
```

Reason:

```text
EMI burden becomes high
Monthly surplus decreases
Emergency buffer decreases
Financial stress increases
```

## Scenario 3 — Explainability

Customer asks:

> "Why should I wait?"

The Communication Agent generates a simple explanation based on the actual calculated financial signals.

## Scenario 4 — Vernacular

Customer switches to:

```text
Hindi
```

or:

```text
Gujarati
```

The system provides a localized explanation.

## Scenario 5 — Suspicious Transaction

Simulate:

```text
₹85,000 transfer
+
New device
+
New location
+
New beneficiary
+
Unusual behaviour
```

The security layer calculates a high security risk.

## Scenario 6 — Security Response

```text
Transaction
     ↓
Fraud Detection
     ↓
Anomaly Detection
     ↓
UEBA
     ↓
Identity Risk
     ↓
Threat Correlation
     ↓
Policy
     ↓
Transaction Restriction
     ↓
Incident
     ↓
Customer Verification
```

---

# ⏱️ 48-Hour Hackathon Architecture

For the hackathon, the architecture is intentionally simplified.

```text
Next.js
    ↓
FastAPI
    ↓
SQLite
    ↓
Python ML
    ↓
AI Orchestrator
    ↓
RAG
    ↓
LLM
```

Simulated components can represent:

```text
Bank APIs
Event Streaming
Security Infrastructure
KMS
SIEM
SOAR
```

The goal is to demonstrate the intelligence architecture rather than build an entire production banking infrastructure in 48 hours.

---

# 🏭 Production Architecture

A production deployment can evolve into:

```text
Customer
   ↓
Mobile / Web
   ↓
API Gateway
   ↓
Core Banking / BaaS
   ↓
Kafka / Webhooks
   ↓
Customer 360
   ↓
Feature Store
   ↓
Model Serving
   ↓
AI Orchestration
   ↓
Policy Engine
   ↓
Private / Controlled LLM
   ↓
Banking APIs
```

Additional production infrastructure can include:

```text
PostgreSQL
Redis
Kafka
KMS / HSM
WAF
SIEM
SOAR
DLP
DSPM
Cloud Security
```

---

# 📈 Current Implementation Status

The project is being developed in phases.

## Completed / Implemented

```text
Database Models                 ✅
Synthetic Banking Data          ✅
Feature Engineering             ✅
Customer 360                    ✅
Financial Health                ✅
Financial Stress                ✅
Loan Risk                       ✅
Digital Twin                    ✅
Customer Segmentation            ✅
Life-Event Detection             ✅
Fraud Detection                 ✅
Transaction Anomaly             ✅
UEBA                            ✅
Identity Risk                   ✅
Threat Correlation              ✅
Incident Response               ✅
Privacy Layer                   ✅
Consent Management              ✅
PII Detection                   ✅
Tokenization                    ✅
Audit Logging                   🟡
Event Architecture              ✅
RAG                             ✅
Offer Engine                    ✅
Recommendation Engine           ✅
Policy Engine                   ✅
Financial Agent                 ✅
Risk & Security Agent           ✅
Recommendation Agent            ✅
Communication Agent             ✅
AI Orchestrator                 ✅
FastAPI APIs                    🟢
```

## In Progress

```text
JWT Authentication              🟡
RBAC Hardening                  🟡
MFA                             🟡
Rate Limiting                   🟡
Production ML Models            🟡
LangGraph Integration           🟡
Real LLM Integration            🟡
Frontend                        🔴
Frontend/API Integration        🔴
End-to-End Testing              🟡
Deployment                      🔴
```

---

# ⚠️ Known Limitations

FinGuru is currently a prototype/hackathon system.

### Synthetic Data

The demonstration uses synthetic banking data rather than production customer data.

### SQLite

The current local development database uses SQLite.

Production deployment should use PostgreSQL or another enterprise-grade database.

### ML Models

Some current intelligence components use statistical, rule-based, or hybrid approaches.

Production deployments should use properly trained, validated, monitored ML models where appropriate.

### LLM

LLM functionality depends on the configured provider and API credentials.

### Event Infrastructure

The prototype uses lightweight event processing.

Production deployments should use Kafka or managed event infrastructure.

### Security Infrastructure

Enterprise infrastructure such as:

```text
SIEM
SOAR
KMS
HSM
DLP
DSPM
WAF
```

is represented at the architecture level or through prototype equivalents.

---

# 🔮 Future Scope

Potential future enhancements include:

## Advanced Machine Learning

- XGBoost financial stress models
- Isolation Forest fraud detection
- Loan risk classification
- Forecasting models
- Deep behavioural models

## Real-Time Banking

- Kafka
- Streaming feature computation
- Real-time model inference
- Event-driven recommendations

## Advanced AI

- Full LangGraph implementation
- Tool-using agents
- Agent memory
- Financial planning agent
- Automated financial coaching

## Voice Banking

- Speech-to-text
- Text-to-speech
- Multilingual voice conversations
- Regional language support

## Security

- SIEM integration
- SOAR automation
- Threat intelligence
- Advanced account takeover detection
- Continuous authentication

## Privacy

- Differential privacy
- Federated learning
- Advanced data governance
- Enterprise DLP
- Data lineage

## Banking Integration

- Open Banking
- Account Aggregation
- Payment APIs
- Core banking APIs
- Real-time notifications

---

# 🤝 Responsible AI

FinGuru is designed around customer financial well-being.

The system should not optimize solely for:

```text
Product Sales
```

Instead it optimizes for:

```text
Customer Financial Well-Being
```

Therefore, the best recommendation may be:

```text
SAVE
WAIT
WARN
APPLY
SEEK HELP
NO ACTION
```

---

# 🧠 Why FinGuru Is Different

## 1. Customer-State-Centric

Traditional:

```text
Transaction → Product
```

FinGuru:

```text
Transactions
    ↓
Customer State
    ↓
Financial Intelligence
    ↓
Recommendation
```

## 2. Need-Centric

FinGuru does not start with:

> "What product can we sell?"

It starts with:

> "What does this customer need?"

## 3. Predictive + Prescriptive

Traditional analytics:

```text
What happened?
```

Predictive analytics:

```text
What will happen?
```

FinGuru:

```text
What should we do?
```

## 4. Loan Suitability

FinGuru distinguishes:

```text
Can the customer get the loan?
```

from:

```text
Should the customer take the loan?
```

## 5. Digital Twin

The customer can simulate the impact of financial decisions before making them.

## 6. Financial + Security Intelligence

Financial decisions and security risks are evaluated together.

## 7. Explainable AI

FinGuru explains why a recommendation was generated.

## 8. Vernacular Banking

The system is designed for English, Hindi and Gujarati interaction.

## 9. Privacy by Design

Consent and purpose limitation are part of the intelligence pipeline.

## 10. Responsible Recommendations

FinGuru can recommend:

```text
WAIT
```

or:

```text
NO ACTION
```

even when a product exists.

---

# 🗣️ Key Innovation Statements

## Product Statement

> **FinGuru doesn't ask what product we can sell the customer; it asks what the customer needs next.**

## Technical Statement

> **FinGuru separates intelligence from execution: ML generates measurable financial and security signals, agents reason over those signals, policy engines enforce safety and compliance, RAG grounds financial answers, and GenAI communicates the final decision.**

## Responsible AI Statement

> **Our AI is not optimized to maximize product conversion. It is optimized for customer financial well-being.**

---

# 🧩 Complete Architecture in One Diagram

```text
                         FINGURU AI
               "Your Personal Financial Copilot"

                              │
                              ▼
                       ┌─────────────┐
                       │  CUSTOMER   │
                       │ Web/Mobile  │
                       │ Voice       │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   FASTAPI   │
                       │ Auth + API  │
                       │ Consent     │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   BANKING   │
                       │    CORE     │
                       │ APIs/Events │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ CUSTOMER    │
                       │    360      │
                       └──────┬──────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
       FINANCIAL INTELLIGENCE       SECURITY INTELLIGENCE
                │                           │
        ┌───────┼───────┐           ┌───────┼───────┐
        ▼       ▼       ▼           ▼       ▼       ▼
      Health  Stress  Loan        Fraud   UEBA  Identity
        │       │      Risk         │       │       │
        └───────┴───────┘           └───────┴───────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                     PRESCRIPTIVE ENGINE
                              │
                              ▼
                       MULTI-AGENT AI
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             Financial      Risk       Recommendation
               Agent        Agent           Agent
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                     Communication Agent
                              │
                              ▼
                   POLICY + PRIVACY GUARDRAIL
                              │
                              ▼
                         RAG + LLM
                              │
                              ▼
                       AI COPILOT
                              │
                              ▼
                      NEXT BEST ACTION
                              │
              ┌────────┬─────┼─────┬────────┐
              ▼        ▼     ▼     ▼        ▼
             SAVE     WAIT  WARN  APPLY   HELP
```

---

# 🎯 Final Positioning

FinGuru is:

> **An AI-powered, event-driven financial intelligence layer over modern banking infrastructure.**

It combines:

```text
Customer 360
      +
Financial Intelligence
      +
Security Intelligence
      +
Prescriptive AI
      +
Multi-Agent Reasoning
      +
Policy Guardrails
      +
Privacy
      +
RAG
      +
Explainable GenAI
      +
Vernacular Interaction
      ↓
NEXT BEST ACTION
```

---

# 🏁 Conclusion

FinGuru transforms traditional banking from a:

```text
Transaction Processing System
```

into a:

```text
Customer Intelligence System
```

The system continuously builds an understanding of the customer's financial state, detects emerging risks, evaluates future scenarios, and recommends an appropriate next action.

The fundamental philosophy is:

```text
Understand the customer
        ↓
Predict what may happen
        ↓
Evaluate risk
        ↓
Simulate possible decisions
        ↓
Apply policy
        ↓
Explain the decision
        ↓
Recommend the safest next action
```

---

# 👥 Team

**Project:** FinGuru  
**Theme:** AI-Powered Hyper-Personalized Banking for Bharat

Add your team information here:

```text
Team Name: BeyondPixels
Team Lead: Neeraj Gupta
Team Members: Himani Choudary , Ritika Kumari , Bharath Kumar MP
Institution: IIIT VADODARA
 
```

---

# 📄 License

This project is developed as a prototype/hackathon project.

Add the appropriate license before public production use.

---

# ⭐ Final Statement

> ## "FinGuru doesn't ask what product we can sell the customer; it asks what the customer needs next."
