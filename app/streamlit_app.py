from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "outputs" / "data"
TABLE_DIR = ROOT / "outputs" / "tables"

st.set_page_config(
    page_title="Instacart Rule Recommender",
    page_icon="IC",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@700;800&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #20231f;
        --muted: #697268;
        --paper: #f6f3ea;
        --panel: #ffffff;
        --line: #ded8c9;
        --leaf: #7f9f68;
        --mint: #e7efe2;
        --citrus: #d9a441;
        --tomato: #b8654b;
        --plum: #5d5574;
    }

    .stApp {
        background:
            linear-gradient(135deg, rgba(82, 120, 83, 0.10), transparent 30%),
            linear-gradient(315deg, rgba(184, 101, 75, 0.08), transparent 26%),
            var(--paper);
        color: var(--ink);
        font-family: "Manrope", sans-serif;
    }

    .main .block-container {
        max-width: 1180px;
        padding: 28px 34px 56px;
    }

    h1, h2, h3, .hero-title, .section-title {
        font-family: "Fraunces", serif;
        letter-spacing: -0.02em;
    }

    .hero {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 22px 26px;
        background:
            linear-gradient(120deg, rgba(217, 164, 65, 0.14), transparent 42%),
            linear-gradient(180deg, #ffffff 0%, #fbf7ed 100%);
        box-shadow: 0 18px 44px rgba(23, 33, 27, 0.08);
        margin-bottom: 18px;
    }

    .hero-kicker {
        color: var(--leaf);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .hero-title {
        color: var(--ink);
        font-size: 34px;
        font-weight: 800;
        line-height: 1.03;
        margin-bottom: 0;
    }

    .hero-subtitle {
        display: none;
    }

    .stat-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0 24px;
    }

    .stat-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 16px 18px;
        text-align: center;
        box-shadow: 0 12px 28px rgba(23, 33, 27, 0.05);
    }

    .stat-label {
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .stat-value {
        color: var(--ink);
        font-size: 30px;
        font-weight: 850;
        margin-top: 4px;
    }

    .section-title {
        font-size: 32px;
        font-weight: 800;
        margin: 12px 0 10px;
    }

    .empty-state {
        border: 1px dashed #d6c7ad;
        border-radius: 8px;
        padding: 18px;
        color: #7b6040;
        background: #fff8e8;
        font-size: 16px;
        font-weight: 800;
    }

    div[class*="st-key-rec-card-"],
    div[class*="st-key-cart-card-"] {
        position: relative;
        overflow: visible !important;
        border: 0 !important;
        border-radius: 22px !important;
        padding: 24px 26px 24px 34px !important;
        background:
            linear-gradient(#fffdf7, #fffdf7) padding-box,
            linear-gradient(135deg, #ff4b4b 0%, #f2c66d 48%, #7f9f68 100%) border-box !important;
        box-shadow:
            0 0 0 3px #d7c4a4,
            0 0 0 9px rgba(255, 244, 222, 0.86),
            0 18px 38px rgba(57, 45, 29, 0.12),
            inset 0 0 0 1px rgba(255, 255, 255, 0.95) !important;
        margin: 20px 0 24px !important;
    }

    div[class*="st-key-rec-card-"] > div,
    div[class*="st-key-cart-card-"] > div {
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    div[class*="st-key-rec-card-"]::before,
    div[class*="st-key-cart-card-"]::before {
        content: "";
        position: absolute;
        left: 14px;
        top: 16px;
        bottom: 16px;
        width: 7px;
        height: auto;
        border-radius: 999px;
        background: linear-gradient(180deg, #ff4b4b, #f2c66d);
        pointer-events: none;
        z-index: 0;
    }

    div[class*="st-key-rec-card-"] > div,
    div[class*="st-key-cart-card-"] > div {
        position: relative;
        z-index: 1;
    }

    .rec-marker,
    .cart-page-marker {
        display: none;
    }

    .rec-title {
        color: var(--ink);
        font-size: 23px;
        font-weight: 850;
        line-height: 1.18;
        margin-bottom: 6px;
    }

    .rec-context {
        color: var(--muted);
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 0;
        align-items: center;
    }

    .rec-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
        margin-top: 12px;
    }

    .metric {
        border-radius: 999px;
        background: #f7f1e5;
        border: 1px solid #e8dcc7;
        color: var(--ink);
        padding: 9px 13px;
        font-size: 15px;
        font-weight: 850;
    }

    .metric strong {
        color: var(--plum);
    }

    .sidebar-brand {
        border-radius: 9px;
        padding: 14px 13px;
        background:
            linear-gradient(180deg, #ffffff 0%, #fff7f4 100%);
        border: 1px solid #e1d7c8;
        border-left: 7px solid #ff4b4b;
        margin: 6px 0 18px;
        box-shadow: 0 10px 24px rgba(38, 53, 42, 0.06);
    }

    .sidebar-title {
        color: #26352a;
        font-family: "Fraunces", serif;
        font-size: clamp(22px, 4.8vw, 28px);
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
    }

    .sidebar-subtitle {
        color: #ff4b4b;
        font-size: 15px;
        font-weight: 850;
        margin-top: 6px;
    }

    .cart-item {
        color: #26352a;
        padding: 0;
        font-size: 20px;
        font-weight: 850;
        line-height: 1.3;
    }

    .cart-context {
        color: var(--muted);
        font-size: 15px;
        font-weight: 800;
        margin-top: 6px;
    }

    div[data-testid="stSidebar"] {
        background: #f3eee4;
    }

    div[data-testid="stSidebar"] * {
        font-family: "Manrope", sans-serif;
    }

    div[data-testid="stSidebar"] label,
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] div,
    div[data-testid="stSidebar"] .stMarkdown {
        color: #26352a !important;
        font-weight: 700;
    }

    div[data-testid="stSidebar"] [role="radiogroup"] label {
        display: flex;
        align-items: center;
        background: #ffffff;
        border: 1px solid #ded8c9;
        border-radius: 8px;
        padding: 10px 9px;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    div[data-testid="stSidebar"] [role="radiogroup"] label * {
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: clamp(13px, 3.4vw, 16px) !important;
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #d6c0a4;
        background: linear-gradient(180deg, #fff7df 0%, #f3dba9 100%);
        color: #2d261c;
        min-height: 44px;
        font-size: 15px;
        font-weight: 850;
        box-shadow: 0 8px 18px rgba(130, 99, 50, 0.12);
    }

    div[class*="st-key-rec-card-"] .stButton > button,
    div[class*="st-key-cart-card-"] .stButton > button {
        min-width: 110px;
        min-height: 50px;
    }

    .stButton > button:hover {
        border-color: #c99841;
        color: #201a12;
        background: linear-gradient(180deg, #ffe9ab 0%, #edc872 100%);
    }

    .stButton > button:disabled,
    .stButton > button:disabled:hover {
        background: #ede6d8;
        border-color: #d5cbbb;
        color: #766c5d !important;
        opacity: 1;
        box-shadow: none;
    }

    div[data-testid="stSidebar"] .stButton > button {
        background: #fffaf0;
        color: #26352a;
        border: 1px solid #d4ccb9;
        box-shadow: none;
    }

    div[data-testid="stSidebar"] .stButton > button:hover {
        background: #e9dfcf;
        color: #26352a;
    }

    div[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        font-size: 13px;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: #ff4b4b !important;
        color: #ffffff !important;
        border: 1px solid #e94343 !important;
        border-radius: 999px !important;
        min-height: 30px !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 14px !important;
    }

    div[data-baseweb="select"] input {
        color: #26352a !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #d6cbb8 !important;
        min-height: 50px !important;
    }

    div[data-baseweb="select"] input::placeholder {
        color: #8a8173 !important;
        opacity: 1 !important;
    }

    label, .stMarkdown, .stCaption, .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
    }

    div[data-testid="stMultiSelect"] label {
        display: none !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="slider"] {
        border-radius: 8px !important;
    }

    @media (max-width: 800px) {
        .main .block-container { padding: 18px 16px 44px; }
        .hero-title { font-size: 34px; }
        .stat-row { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig")


def clean_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return " ".join(str(value).replace("\xa0", " ").split()).strip()


def split_rule(rule: object) -> tuple[str, str]:
    text = clean_text(rule)
    if "→" in text:
        left, right = text.split("→", 1)
        return clean_text(left), clean_text(right)
    if "->" in text:
        left, right = text.split("->", 1)
        return clean_text(left), clean_text(right)
    return "", ""


def normalize_columns(data: pd.DataFrame) -> pd.DataFrame:
    return data.rename(
        columns={
            "Luật": "Rule",
            "Sản phẩm trong giỏ": "Basket item",
            "Sản phẩm nên gợi ý": "Recommendation",
            "Sản phẩm": "Product",
            "Nhóm hàng chi tiết": "Aisle",
            "Nhóm hàng lớn": "Department",
            "Số giỏ chứa sản phẩm": "Basket count",
            "Điểm tổng hợp": "Score",
            "support": "Support",
            "confidence": "Confidence",
            "lift": "Lift",
            "weighted_score": "Score",
            "Giờ mua": "Hour",
            "Support theo giờ": "Hourly support",
            "Confidence theo giờ": "Hourly confidence",
            "Lift theo giờ": "Hourly lift",
            "Số đơn có vế điều kiện": "Antecedent orders",
            "Số đơn mua kèm": "Paired orders",
        }
    )


def prepare_rules(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return data

    data = normalize_columns(data.copy())

    if {"Basket item", "Recommendation"}.issubset(data.columns):
        data["Basket item"] = data["Basket item"].apply(clean_text)
        data["Recommendation"] = data["Recommendation"].apply(clean_text)
        return data

    if "Rule" in data.columns:
        pairs = data["Rule"].apply(split_rule)
        data["Basket item"] = pairs.apply(lambda pair: pair[0])
        data["Recommendation"] = pairs.apply(lambda pair: pair[1])
        return data

    return pd.DataFrame()


def load_products() -> list[str]:
    frequent = normalize_columns(read_csv(TABLE_DIR / "frequent_products.csv"))
    if not frequent.empty and "Product" in frequent.columns:
        products = frequent["Product"].dropna().apply(clean_text)
        return sorted(products[products != ""].unique())

    catalog = normalize_columns(read_csv(DATA_DIR / "product_catalog.csv"))
    if not catalog.empty and "Product" in catalog.columns:
        products = catalog["Product"].dropna().apply(clean_text)
        return sorted(products[products != ""].unique())

    return []


def load_product_options() -> pd.DataFrame:
    frequent = normalize_columns(read_csv(TABLE_DIR / "frequent_products.csv"))
    catalog = normalize_columns(read_csv(DATA_DIR / "product_catalog.csv"))
    data = frequent if not frequent.empty else catalog

    if data.empty or "Product" not in data.columns:
        return pd.DataFrame(columns=["Product", "Aisle", "Department"])

    data = data.copy()
    for column in ["Product", "Aisle", "Department"]:
        if column not in data.columns:
            data[column] = "Unknown"
        data[column] = data[column].fillna("Unknown").apply(clean_text)

    data = data[data["Product"] != ""]
    return data[["Product", "Aisle", "Department"]].drop_duplicates().sort_values("Product")


def fmt(value: object, integer: bool = False) -> str:
    if value is None or value == "" or pd.isna(value):
        return "-"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return clean_text(value)
    if integer:
        return f"{int(round(number)):,}"
    return f"{number:.4f}"


def add_products(items: list[str]) -> None:
    for item in items:
        if item not in st.session_state.cart:
            st.session_state.cart.append(item)


def remove_product(product: str) -> None:
    st.session_state.cart = [item for item in st.session_state.cart if item != product]


def match_rules(rules: pd.DataFrame, cart: list[str]) -> pd.DataFrame:
    if rules.empty or not cart:
        return pd.DataFrame()

    data = rules.copy()
    basket_text = data["Basket item"].astype(str).str.lower()
    matches = pd.Series(0, index=data.index)

    for product in cart:
        matches += basket_text.str.contains(product.lower(), regex=False, na=False).astype(int)

    data = data[matches > 0].copy()
    data["Matched products"] = matches[matches > 0]

    sort_columns = [
        column
        for column in ["Matched products", "Score", "Confidence", "Lift", "Support"]
        if column in data.columns
    ]
    if sort_columns:
        data = data.sort_values(sort_columns, ascending=False)

    return data


def match_time_rules(rules: pd.DataFrame, cart: list[str], hour: int) -> pd.DataFrame:
    data = match_rules(rules, cart)
    if data.empty:
        return data

    if "Hour" in data.columns:
        hours = pd.to_numeric(data["Hour"], errors="coerce")
        data = data[hours == hour]

    sort_columns = [
        column
        for column in ["Matched products", "Hourly confidence", "Hourly lift", "Hourly support"]
        if column in data.columns
    ]
    if sort_columns:
        data = data.sort_values(sort_columns, ascending=False)

    return data


def metric_chip(label: str, value: str) -> str:
    return f'<span class="metric">{escape(label)}: <strong>{escape(value)}</strong></span>'


def recommendation_card(title: str, based_on: str, metrics: list[tuple[str, str]], key: str) -> None:
    metric_html = "".join(metric_chip(label, value) for label, value in metrics if value != "-")
    recommendation = clean_text(title)
    with st.container(border=False, key=f"rec-card-{key}"):
        st.markdown('<div class="rec-marker"></div>', unsafe_allow_html=True)
        content_col, action_col = st.columns([5, 1.25], vertical_alignment="center")
        with content_col:
            st.markdown(
                f"""
                <div class="rec-title">{escape(recommendation)}</div>
                <div class="rec-context">Triggered by: {escape(clean_text(based_on))}</div>
                <div class="metric-row">{metric_html}</div>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            if st.button("Add", key=key, use_container_width=True):
                add_products([recommendation])
                st.rerun()


def render_recommendations(data: pd.DataFrame, mode: str, limit: int = 8) -> None:
    if data.empty:
        st.markdown(
            '<div class="empty-state">No matching recommendations for the current basket.</div>',
            unsafe_allow_html=True,
        )
        return

    for position, (_, row) in enumerate(data.head(limit).iterrows()):
        if mode == "time":
            metrics = [
                ("Hour", fmt(row.get("Hour"), integer=True)),
                ("Support", fmt(row.get("Hourly support"))),
                ("Confidence", fmt(row.get("Hourly confidence"))),
                ("Lift", fmt(row.get("Hourly lift"))),
            ]
        else:
            metrics = [
                ("Support", fmt(row.get("Support"))),
                ("Confidence", fmt(row.get("Confidence"))),
                ("Lift", fmt(row.get("Lift"))),
                ("Score", fmt(row.get("Score"))),
            ]

        recommendation = clean_text(row.get("Recommendation", ""))
        recommendation_card(
            recommendation,
            row.get("Basket item", ""),
            metrics,
            key=f"{mode}_add_{position}_{data.index[position]}",
        )


def render_cart_page() -> None:
    st.markdown('<div class="section-title">Cart</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown(
            '<div class="empty-state">The cart is empty. Add products before opening recommendations.</div>',
            unsafe_allow_html=True,
        )
        return

    for position, product in enumerate(st.session_state.cart, start=1):
        with st.container(border=False, key=f"cart-card-{position}"):
            st.markdown('<div class="cart-page-marker"></div>', unsafe_allow_html=True)
            item_col, action_col = st.columns([5, 1.25], vertical_alignment="center")
            with item_col:
                st.markdown(
                    f"""
                    <div class="cart-item">{escape(product)}</div>
                    <div class="cart-context">Item {position} in the current basket</div>
                    """,
                    unsafe_allow_html=True,
                )
            with action_col:
                if st.button("Remove", key=f"remove_{position}_{product}", use_container_width=True):
                    remove_product(product)
                    st.rerun()

    _, clear_col, _ = st.columns([1.5, 2, 1.5])
    with clear_col:
        if st.button("Clear cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()


if "cart" not in st.session_state:
    st.session_state.cart = []

product_options = load_product_options()
products = sorted(product_options["Product"].dropna().unique()) if not product_options.empty else load_products()
weighted_rules = prepare_rules(read_csv(TABLE_DIR / "weighted_rules.csv"))
time_rules = prepare_rules(read_csv(TABLE_DIR / "time_aware_rules.csv"))
top_rules = prepare_rules(read_csv(TABLE_DIR / "top_rules.csv"))
rules = weighted_rules if not weighted_rules.empty else top_rules

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">Instacart</div>
            <div class="sidebar-subtitle">Basket assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio("Navigation", ["Products", "Cart", "Recommend"], label_visibility="collapsed")

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Market Basket Analysis</div>
        <div class="hero-title">Instacart Rule Recommender</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
        <div class="stat-row">
            <div class="stat-card">
            <div class="stat-label">Unique products</div>
            <div class="stat-value">{len(products):,}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Cart items</div>
            <div class="stat-value">{len(st.session_state.cart):,}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "Products":
    st.markdown('<div class="section-title">Products</div>', unsafe_allow_html=True)

    if not product_options.empty:
        dept_col, aisle_col = st.columns(2)
        with dept_col:
            department_options = ["All departments"] + sorted(
                item for item in product_options["Department"].dropna().unique() if item
            )
            department = st.selectbox("Department", department_options)

        filtered_products = product_options.copy()
        if department != "All departments":
            filtered_products = filtered_products[filtered_products["Department"] == department]

        with aisle_col:
            aisle_options = ["All aisles"] + sorted(
                item for item in filtered_products["Aisle"].dropna().unique() if item
            )
            aisle = st.selectbox("Aisle", aisle_options)

        if aisle != "All aisles":
            filtered_products = filtered_products[filtered_products["Aisle"] == aisle]

        selected = st.multiselect(
            "Product",
            options=sorted(filtered_products["Product"].dropna().unique()),
            placeholder="Type a product name...",
        )
    else:
        selected = st.multiselect(
            "Product",
            options=products,
            placeholder="Type a product name...",
        )

    _, add_col, _ = st.columns([1.5, 2, 1.5])
    with add_col:
        if st.button("Add selected products", disabled=not selected, use_container_width=True):
            add_products(selected)
            st.rerun()

elif page == "Cart":
    render_cart_page()

else:
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown(
            '<div class="empty-state">Add at least one product to generate recommendations.</div>',
            unsafe_allow_html=True,
        )
    else:
        tab_basket, tab_time = st.tabs(["Basket-based", "Time-aware"])

        with tab_basket:
            basket_result = match_rules(rules, st.session_state.cart)
            render_recommendations(basket_result, mode="basket")

        with tab_time:
            hour = st.slider("Shopping hour", 0, 23, 10)
            time_result = match_time_rules(time_rules, st.session_state.cart, hour)
            render_recommendations(time_result, mode="time")
