import {
  ArrowDownLeft,
  ArrowUpRight,
  CalendarDays,
  ChevronDown,
  Download,
  Filter,
  Search,
  RefreshCw,
  ShoppingBag,
  Utensils,
  Car,
  Home,
  Smartphone,
  Briefcase,
  CreditCard,
  Wallet,
  IndianRupee,
  X,
} from "lucide-react";

import { useEffect, useMemo, useState } from "react";
import { getCustomerTransactions } from "../../services/api";
import "./Transactions.css";

const CUSTOMER_ID = 1;

const fallbackTransactions = [
  {
    id: 1,
    description: "Salary Credit",
    category: "Income",
    amount: 65000,
    type: "credit",
    date: "2026-09-01",
    status: "Completed",
  },
  {
    id: 2,
    description: "Amazon",
    category: "Shopping",
    amount: 2499,
    type: "debit",
    date: "2026-09-03",
    status: "Completed",
  },
  {
    id: 3,
    description: "Swiggy",
    category: "Food",
    amount: 620,
    type: "debit",
    date: "2026-09-04",
    status: "Completed",
  },
  {
    id: 4,
    description: "Uber",
    category: "Transport",
    amount: 380,
    type: "debit",
    date: "2026-09-05",
    status: "Completed",
  },
  {
    id: 5,
    description: "House Rent",
    category: "Housing",
    amount: 12000,
    type: "debit",
    date: "2026-09-06",
    status: "Completed",
  },
  {
    id: 6,
    description: "Jio Recharge",
    category: "Bills",
    amount: 799,
    type: "debit",
    date: "2026-09-07",
    status: "Completed",
  },
  {
    id: 7,
    description: "Flipkart",
    category: "Shopping",
    amount: 1899,
    type: "debit",
    date: "2026-09-08",
    status: "Completed",
  },
  {
    id: 8,
    description: "Restaurant",
    category: "Food",
    amount: 1250,
    type: "debit",
    date: "2026-09-09",
    status: "Completed",
  },
  {
    id: 9,
    description: "Metro",
    category: "Transport",
    amount: 500,
    type: "debit",
    date: "2026-09-10",
    status: "Completed",
  },
  {
    id: 10,
    description: "Freelance Payment",
    category: "Income",
    amount: 8500,
    type: "credit",
    date: "2026-09-11",
    status: "Completed",
  },
];

function normalizeTransaction(item, index) {
  const amount = Number(
    item?.amount ??
      item?.transaction_amount ??
      item?.value ??
      item?.total ??
      0
  );

  const rawType = String(
    item?.type ??
      item?.transaction_type ??
      item?.direction ??
      ""
  ).toLowerCase();

  const rawCategory = String(
    item?.category ??
      item?.transaction_category ??
      item?.classification ??
      "Other"
  );

  const description =
    item?.description ??
    item?.merchant ??
    item?.merchant_name ??
    item?.name ??
    item?.narration ??
    `Transaction ${index + 1}`;

  const date =
    item?.date ??
    item?.transaction_date ??
    item?.created_at ??
    item?.timestamp ??
    new Date().toISOString();

  let type = "debit";

  if (
    rawType.includes("credit") ||
    rawType.includes("income") ||
    rawType.includes("deposit") ||
    rawType.includes("received")
  ) {
    type = "credit";
  }

  if (
    item?.is_credit === true ||
    item?.credit === true
  ) {
    type = "credit";
  }

  if (
    item?.is_debit === true ||
    item?.debit === true
  ) {
    type = "debit";
  }

  return {
    id: item?.id ?? item?.transaction_id ?? index + 1,
    description: String(description),
    category: rawCategory,
    amount: Math.abs(amount),
    type,
    date,
    status: item?.status ?? "Completed",
  };
}

function getTransactionsArray(data) {
  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data?.transactions)) {
    return data.transactions;
  }

  if (Array.isArray(data?.items)) {
    return data.items;
  }

  if (Array.isArray(data?.data)) {
    return data.data;
  }

  return [];
}

function formatMoney(amount) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(amount) || 0);
}

function formatDate(dateValue) {
  if (!dateValue) return "Unknown date";

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return String(dateValue);
  }

  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function getCategoryIcon(category) {
  const value = String(category).toLowerCase();

  if (value.includes("food") || value.includes("restaurant")) {
    return <Utensils size={18} />;
  }

  if (value.includes("shopping") || value.includes("retail")) {
    return <ShoppingBag size={18} />;
  }

  if (
    value.includes("transport") ||
    value.includes("travel") ||
    value.includes("uber") ||
    value.includes("metro")
  ) {
    return <Car size={18} />;
  }

  if (
    value.includes("housing") ||
    value.includes("rent") ||
    value.includes("home")
  ) {
    return <Home size={18} />;
  }

  if (
    value.includes("bill") ||
    value.includes("recharge") ||
    value.includes("utility")
  ) {
    return <Smartphone size={18} />;
  }

  if (
    value.includes("income") ||
    value.includes("salary") ||
    value.includes("freelance")
  ) {
    return <Briefcase size={18} />;
  }

  if (value.includes("credit")) {
    return <CreditCard size={18} />;
  }

  return <Wallet size={18} />;
}

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [usingFallback, setUsingFallback] = useState(false);

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("all");

  async function loadTransactions(showRefresh = false) {
    try {
      if (showRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      const data = await getCustomerTransactions(CUSTOMER_ID);

      const backendTransactions = getTransactionsArray(data)
        .map(normalizeTransaction);

      if (backendTransactions.length > 0) {
        setTransactions(backendTransactions);
        setUsingFallback(false);
      } else {
        setTransactions(fallbackTransactions);
        setUsingFallback(true);
      }
    } catch (error) {
      console.error("Transaction loading error:", error);

      setTransactions(fallbackTransactions);
      setUsingFallback(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadTransactions();
  }, []);

  const summary = useMemo(() => {
    const income = transactions
      .filter((transaction) => transaction.type === "credit")
      .reduce((total, transaction) => total + transaction.amount, 0);

    const expenses = transactions
      .filter((transaction) => transaction.type === "debit")
      .reduce((total, transaction) => total + transaction.amount, 0);

    return {
      income,
      expenses,
      balance: income - expenses,
      count: transactions.length,
    };
  }, [transactions]);

  const filteredTransactions = useMemo(() => {
    const query = search.trim().toLowerCase();

    return transactions.filter((transaction) => {
      const matchesSearch =
        !query ||
        transaction.description.toLowerCase().includes(query) ||
        transaction.category.toLowerCase().includes(query);

      const matchesType =
        filter === "all" ||
        transaction.type === filter;

      let matchesDate = true;

      if (dateFilter !== "all") {
        const transactionDate = new Date(transaction.date);
        const now = new Date();

        if (!Number.isNaN(transactionDate.getTime())) {
          const diff =
            now.getTime() - transactionDate.getTime();

          const days = diff / (1000 * 60 * 60 * 24);

          if (dateFilter === "7") {
            matchesDate = days <= 7;
          }

          if (dateFilter === "30") {
            matchesDate = days <= 30;
          }

          if (dateFilter === "90") {
            matchesDate = days <= 90;
          }
        }
      }

      return matchesSearch && matchesType && matchesDate;
    });
  }, [transactions, search, filter, dateFilter]);

  function clearSearch() {
    setSearch("");
  }

  function exportTransactions() {
    const rows = [
      ["Date", "Description", "Category", "Type", "Amount", "Status"],
      ...filteredTransactions.map((transaction) => [
        formatDate(transaction.date),
        transaction.description,
        transaction.category,
        transaction.type,
        transaction.amount,
        transaction.status,
      ]),
    ];

    const csv = rows
      .map((row) =>
        row
          .map((cell) =>
            `"${String(cell).replace(/"/g, '""')}"`
          )
          .join(",")
      )
      .join("\n");

    const blob = new Blob([csv], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "finguru-transactions.csv";
    link.click();

    URL.revokeObjectURL(url);
  }

  return (
    <div className="transactions-page">
      {/* HEADER */}
      <header className="transactions-header">
        <div>
          <div className="transactions-breadcrumb">
            FinGuru <span>/</span> Transactions
          </div>

          <h1>Transaction Center</h1>

          <p>
            Understand where your money is going and where
            it is coming from.
          </p>
        </div>

        <div className="transactions-header-actions">
          <button
            className="transaction-refresh"
            onClick={() => loadTransactions(true)}
            disabled={refreshing}
          >
            <RefreshCw
              size={17}
              className={refreshing ? "spin" : ""}
            />
            {refreshing ? "Refreshing..." : "Refresh"}
          </button>

          <button
            className="transaction-export"
            onClick={exportTransactions}
          >
            <Download size={17} />
            Export
          </button>
        </div>
      </header>

      {/* BACKEND STATUS */}
      {usingFallback && (
        <div className="transaction-warning">
          <span>⚡</span>
          <div>
            <strong>Demo transaction data</strong>
            <p>
              FinGuru could not retrieve transaction records
              from the backend, so demo data is being displayed.
            </p>
          </div>
        </div>
      )}

      {/* SUMMARY */}
      <section className="transaction-summary">
        <div className="summary-card balance-summary">
          <div className="summary-icon">
            <IndianRupee size={22} />
          </div>

          <div>
            <span>Net Cash Flow</span>
            <strong>
              {formatMoney(summary.balance)}
            </strong>
            <small>
              Income minus expenses
            </small>
          </div>
        </div>

        <div className="summary-card income-summary">
          <div className="summary-icon">
            <ArrowDownLeft size={22} />
          </div>

          <div>
            <span>Total Income</span>
            <strong>
              {formatMoney(summary.income)}
            </strong>
            <small>
              Money received
            </small>
          </div>
        </div>

        <div className="summary-card expense-summary">
          <div className="summary-icon">
            <ArrowUpRight size={22} />
          </div>

          <div>
            <span>Total Expenses</span>
            <strong>
              {formatMoney(summary.expenses)}
            </strong>
            <small>
              Money spent
            </small>
          </div>
        </div>

        <div className="summary-card count-summary">
          <div className="summary-icon">
            <Wallet size={22} />
          </div>

          <div>
            <span>Transactions</span>
            <strong>{summary.count}</strong>
            <small>
              Records available
            </small>
          </div>
        </div>
      </section>

      {/* SEARCH + FILTER */}
      <section className="transaction-toolbar">
        <div className="transaction-search">
          <Search size={19} />

          <input
            type="text"
            placeholder="Search merchant, category..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
          />

          {search && (
            <button
              className="clear-search"
              onClick={clearSearch}
            >
              <X size={16} />
            </button>
          )}
        </div>

        <div className="transaction-filters">
          <div className="filter-control">
            <Filter size={17} />

            <select
              value={filter}
              onChange={(event) =>
                setFilter(event.target.value)
              }
            >
              <option value="all">All transactions</option>
              <option value="credit">Income</option>
              <option value="debit">Expenses</option>
            </select>

            <ChevronDown size={15} />
          </div>

          <div className="filter-control">
            <CalendarDays size={17} />

            <select
              value={dateFilter}
              onChange={(event) =>
                setDateFilter(event.target.value)
              }
            >
              <option value="all">All dates</option>
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>

            <ChevronDown size={15} />
          </div>
        </div>
      </section>

      {/* TRANSACTION TABLE */}
      <section className="transactions-card">
        <div className="transactions-card-header">
          <div>
            <h2>Recent Transactions</h2>

            <p>
              {filteredTransactions.length} transaction
              {filteredTransactions.length !== 1 ? "s" : ""} found
            </p>
          </div>

          <div className="secure-label">
            <span className="secure-dot"></span>
            Secure & encrypted
          </div>
        </div>

        {loading ? (
          <div className="transactions-loading">
            <div className="loading-spinner"></div>
            <p>Loading your transactions...</p>
          </div>
        ) : filteredTransactions.length === 0 ? (
          <div className="empty-transactions">
            <div className="empty-icon">
              <Search size={28} />
            </div>

            <h3>No transactions found</h3>

            <p>
              Try changing your search or filters.
            </p>

            <button
              onClick={() => {
                setSearch("");
                setFilter("all");
                setDateFilter("all");
              }}
            >
              Clear filters
            </button>
          </div>
        ) : (
          <div className="transactions-list">
            {filteredTransactions.map((transaction) => (
              <div
                className="transaction-row"
                key={transaction.id}
              >
                <div
                  className={`transaction-icon ${
                    transaction.type === "credit"
                      ? "credit-icon"
                      : "debit-icon"
                  }`}
                >
                  {getCategoryIcon(transaction.category)}
                </div>

                <div className="transaction-main">
                  <strong>
                    {transaction.description}
                  </strong>

                  <span>
                    {transaction.category}
                  </span>
                </div>

                <div className="transaction-date">
                  {formatDate(transaction.date)}
                </div>

                <div
                  className={`transaction-status ${
                    transaction.status
                      .toLowerCase()
                      .includes("pending")
                      ? "pending"
                      : ""
                  }`}
                >
                  {transaction.status}
                </div>

                <div
                  className={`transaction-amount ${
                    transaction.type === "credit"
                      ? "credit-amount"
                      : "debit-amount"
                  }`}
                >
                  <span>
                    {transaction.type === "credit"
                      ? "+"
                      : "-"}
                  </span>

                  {formatMoney(transaction.amount)}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* AI INSIGHT */}
      <section className="transaction-ai">
        <div className="ai-symbol">✦</div>

        <div className="ai-content">
          <span>FIN-GURU AI INSIGHT</span>

          <h3>
            Your money activity at a glance
          </h3>

          <p>
            {summary.expenses > 0
              ? `You have recorded ${formatMoney(
                  summary.expenses
                )} in expenses across ${
                  summary.count
                } transactions. Review your spending categories regularly to identify opportunities to save.`
              : "Start tracking transactions to receive personalized financial insights."}
          </p>
        </div>
      </section>
    </div>
  );
}

export default Transactions;