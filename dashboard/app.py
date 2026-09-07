from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import textwrap
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from src.recommender.recommend import RecommendationEngine
# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"


st.set_page_config(
    page_title="Content Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(126, 87, 194, 0.12),
                transparent 32%
            ),
            #09090b;
        color: #f4f4f5;
    }

/* Streamlit chrome */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Keep header visible so sidebar can be reopened */
header {
    visibility: visible;
    background: transparent;
}

/* Keep sidebar collapse/reopen control visible */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    display: flex !important;
}

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d0d10;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* Typography */
    h1, h2, h3 {
        letter-spacing: -0.025em;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 18px;
        transition: 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(168,85,247,0.45);
        transform: translateY(-1px);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(168,85,247,0.45);
        background: linear-gradient(
            135deg,
            #7c3aed,
            #a855f7
        );
        color: white;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #c084fc;
        box-shadow:
            0 0 25px rgba(168,85,247,0.25);
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background: #121216;
        border-radius: 10px;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #a1a1aa;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #c084fc;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.07);
    }

    .brand {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .brand-mark {
        color: #a855f7;
        font-size: 1.5rem;
        margin-right: 7px;
    }

    .subtitle {
        color: #a1a1aa;
        font-size: 0.92rem;
    }

    .section-label {
        color: #71717a;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 1.4rem;
        margin-bottom: 0.4rem;
    }

    .live-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.25);
        color: #86efac;
        font-size: 0.75rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    users = pd.read_csv(
        DATA_DIR / "users_clean.csv"
    )

    creators = pd.read_csv(
        DATA_DIR / "creators_clean.csv"
    )

    content = pd.read_csv(
        DATA_DIR / "content_clean.csv"
    )

    interactions = pd.read_csv(
        DATA_DIR / "interactions_clean.csv"
    )

    # Date parsing
    users["signup_date"] = pd.to_datetime(
        users["signup_date"],
        errors="coerce"
    )

    creators["signup_date"] = pd.to_datetime(
        creators["signup_date"],
        errors="coerce"
    )

    content["created_at"] = pd.to_datetime(
        content["created_at"],
        errors="coerce"
    )

    interactions["timestamp"] = pd.to_datetime(
        interactions["timestamp"],
        errors="coerce"
    )

    return users, creators, content, interactions






# ============================================================
# LOAD
# ============================================================
@st.cache_resource
def load_recommendation_engine():
    return RecommendationEngine()

try:

    with st.status(
        "Initializing AI Content Intelligence Engine...",
        expanded=True
    ) as load_status:

        st.write("Loading users, creators and content data...")
        users, creators, content, interactions = load_data()

        st.write("Initializing recommendation engine...")

        recommendation_engine = load_recommendation_engine()

        feature_columns = recommendation_engine.feature_columns

        st.write("Validating model feature contract...")

        if len(feature_columns) != 53:
            raise ValueError(
                f"Expected 53 model features, found {len(feature_columns)}."
            )

        st.write("Recommendation engine ready.")

        load_status.update(
            label="AI Content Intelligence Engine ready",
            state="complete",
            expanded=False
        )

    data_loaded = True

except Exception as e:

    data_loaded = False

    st.error(
        f"Unable to load project assets: {e}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">◈</span>
            CONTENT INTELLIGENCE
        </div>
        <div class="subtitle">
            Personalized discovery platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="section-label">Discover</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Dashboard section",
        [
            "Overview",
            "Content Intelligence",
            "Creator Intelligence",
            "Recommendations",
        ],
        label_visibility="visible",
    )

    st.markdown(
        '<div class="section-label">Experiment</div>',
        unsafe_allow_html=True
    )

    experiment_page = st.radio(
        "Experiment section",
        [
            "Experiments",
            "Model",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color:#71717a;
            font-size:0.72rem;
            line-height:1.6;
        ">
            AI Content Intelligence Engine<br>
            Data Science Portfolio Project
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [8, 1]
)

with header_left:

    st.markdown(
        '<h1 style="margin-bottom:0;">AI Content Intelligence</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Personalized discovery · Engagement intelligence · '
        'Creator analytics'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div style="text-align:right; padding-top:12px;">'
        '<span class="live-pill">● LIVE DATA</span>'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown("### Platform overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Users",
            f"{len(users):,}"
        )

    with col2:
        st.metric(
            "Content",
            f"{len(content):,}"
        )

    with col3:
        st.metric(
            "Creators",
            f"{len(creators):,}"
        )

    with col4:
        st.metric(
            "Interactions",
            f"{len(interactions):,}"
        )

    st.markdown("")

    # Engagement
    engagement_rate = interactions[
        "meaningful_engagement"
    ].mean()

    avg_watch = interactions[
        "watch_time"
    ].mean()

    avg_completion = interactions[
        "completion_rate"
    ].mean()

    ctr = interactions[
        "clicked"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Engagement rate",
            f"{engagement_rate:.1%}"
        )

    with col2:
        st.metric(
            "CTR",
            f"{ctr:.1%}"
        )

    with col3:
        st.metric(
            "Avg watch time",
            f"{avg_watch:.1f}s"
        )

    with col4:
        st.metric(
            "Avg completion",
            f"{avg_completion:.1%}"
        )

    st.markdown("")

    # --------------------------------------------------------
    # DAILY ENGAGEMENT
    # --------------------------------------------------------

    daily = (
        interactions
        .assign(
            date=interactions["timestamp"].dt.date
        )
        .groupby("date")
        .agg(
            interactions=("user_id", "size"),
            engagement_rate=(
                "meaningful_engagement",
                "mean"
            )
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Engagement trend")

        fig = px.line(
            daily,
            x="date",
            y="engagement_rate",
            template="plotly_dark",
        )

        fig.update_layout(
            height=340,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            yaxis_tickformat=".0%",
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("### Content mix")

        content_mix = (
            content["content_type"]
            .value_counts()
            .reset_index()
        )

        content_mix.columns = [
            "content_type",
            "count"
        ]

        fig = px.pie(
            content_mix,
            names="content_type",
            values="count",
            hole=0.62,
            template="plotly_dark",
        )

        fig.update_layout(
            height=340,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            showlegend=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # GENRE
    # --------------------------------------------------------

    st.markdown("### Engagement by genre")

    genre_stats = (
        interactions
        .groupby("genre")
        .agg(
            interactions=("user_id", "size"),
            engagement_rate=(
                "meaningful_engagement",
                "mean"
            ),
            avg_watch_time=(
                "watch_time",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "engagement_rate",
            ascending=False
        )
    )

    fig = px.bar(
        genre_stats,
        x="genre",
        y="engagement_rate",
        hover_data=[
            "interactions",
            "avg_watch_time"
        ],
        template="plotly_dark",
    )

    fig.update_layout(
        height=360,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        yaxis_tickformat=".0%",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CONTENT INTELLIGENCE
# ============================================================

elif page == "Content Intelligence":

    st.markdown("### Content Intelligence")

    st.caption(
        "Understand what characteristics are associated "
        "with stronger content performance."
    )

    # Join content metadata to interactions
    content_perf = (
        interactions
        .groupby("content_id")
        .agg(
            interactions=("user_id", "size"),
            engagement_rate=(
                "meaningful_engagement",
                "mean"
            ),
            avg_watch_time=(
                "watch_time",
                "mean"
            ),
            avg_completion=(
                "completion_rate",
                "mean"
            )
        )
        .reset_index()
        .merge(
            content[
                [
                    "content_id",
                    "genre",
                    "content_type",
                    "duration"
                ]
            ],
            on="content_id",
            how="left"
        )
    )

    top_content = (
        content_perf
        .query("interactions >= 10")
        .sort_values(
            "engagement_rate",
            ascending=False
        )
        .head(15)
    )

    st.markdown("### Top-performing content")

    st.dataframe(
        top_content[
            [
                "content_id",
                "genre",
                "content_type",
                "duration",
                "interactions",
                "engagement_rate",
                "avg_watch_time",
                "avg_completion"
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Duration vs engagement")

    fig = px.scatter(
        content_perf.query("interactions >= 5"),
        x="duration",
        y="engagement_rate",
        size="interactions",
        hover_name="content_id",
        template="plotly_dark",
    )

    fig.update_layout(
        height=450,
        yaxis_tickformat=".0%",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CREATOR INTELLIGENCE
# ============================================================

elif page == "Creator Intelligence":

    st.markdown("### Creator Intelligence")

    creator_perf = (
        interactions
        .groupby("creator_id")
        .agg(
            interactions=("user_id", "size"),
            engagement_rate=(
                "meaningful_engagement",
                "mean"
            ),
            avg_watch_time=(
                "watch_time",
                "mean"
            ),
            avg_completion=(
                "completion_rate",
                "mean"
            ),
            unique_users=(
                "user_id",
                "nunique"
            )
        )
        .reset_index()
        .merge(
            creators[
                [
                    "creator_id",
                    "followers",
                    "creator_type"
                ]
            ],
            on="creator_id",
            how="left"
        )
    )

    creator_perf["engagement_per_reach"] = (
        creator_perf["engagement_rate"]
    )

    top_creators = (
        creator_perf
        .query("interactions >= 20")
        .sort_values(
            "engagement_rate",
            ascending=False
        )
        .head(20)
    )

    st.markdown("### Creator leaderboard")

    st.dataframe(
        top_creators[
            [
                "creator_id",
                "creator_type",
                "followers",
                "interactions",
                "unique_users",
                "engagement_rate",
                "avg_watch_time",
                "avg_completion"
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Creator size vs engagement")

    fig = px.scatter(
        creator_perf.query("interactions >= 20"),
        x="followers",
        y="engagement_rate",
        size="unique_users",
        hover_name="creator_id",
        log_x=True,
        template="plotly_dark",
    )

    fig.update_layout(
        height=450,
        yaxis_tickformat=".0%",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.markdown("### Personalized Discovery")

    st.caption(
        "Interactive serving layer for the Notebook 07 "
        "personalized recommendation pipeline."
    )

    user_options = sorted(
        users["user_id"]
        .astype(str)
        .tolist()
    )

    selected_user = st.selectbox(
        "Select a user",
        user_options
    )

    selected_history = interactions[
        interactions["user_id"].astype(str)
        == selected_user
    ]

    history_count = len(selected_history)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Historical interactions",
            f"{history_count:,}"
        )

    with col2:
        st.metric(
            "Past engagement rate",
            f"{selected_history['meaningful_engagement'].mean():.1%}"
            if history_count > 0
            else "—"
        )

    with col3:
        st.metric(
            "Past CTR",
            f"{selected_history['clicked'].mean():.1%}"
            if history_count > 0
            else "—"
        )

    st.markdown("")

    if st.button(
        "Generate personalized feed",
        type="primary",
        use_container_width=False
    ):

        with st.status(
            "Running Notebook 07 recommendation pipeline...",
            expanded=True
        ) as recommendation_status:

            try:

                st.write(
                    "Loading user interaction history..."
                )

                if history_count == 0:

                    st.write(
                        "New user detected — activating "
                        "cold-start strategy."
                    )

                else:

                    st.write(
                        f"Found {history_count:,} historical interactions."
                    )

                st.write(
                    "Running candidate generation, filtering, "
                    "feature construction and model scoring..."
                )

                result = recommendation_engine.recommendation_details(
                    selected_user,
                    k=10
                )

                recommendations = result.details

                recommendation_type = (
                    "cold_start"
                    if history_count == 0
                    else "personalized_ml"
                )

                st.write(
                    f"Generated {len(recommendations)} recommendations."
                )

                recommendation_status.update(
                    label="Recommendation pipeline completed",
                    state="complete",
                    expanded=False
                )

            except Exception as e:

                recommendation_status.update(
                    label="Recommendation pipeline failed",
                    state="error",
                    expanded=True
                )

                st.error(
                    f"Recommendation error: {e}"
                )

                st.stop()

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.markdown("---")

        st.markdown("### Recommended for you")

        if recommendation_type == "cold_start":

            st.info(
                "Cold-start strategy: this user has no historical "
                "interactions, so the system recommends recent unseen content."
            )

        else:

            st.success(
                "Personalized ML ranking generated from the user's "
                "historical engagement behavior."
            )

        # ----------------------------------------------------
        # RECOMMENDATION CARDS
        # ----------------------------------------------------

        if len(recommendations) == 0:

            st.warning(
                "No eligible recommendations were generated."
            )

        else:

            for _, row in recommendations.iterrows():

                creator_row = creators[
                    creators["creator_id"].astype(str)
                    == str(row["creator_id"])
                ]

                if len(creator_row) > 0:
                    creator_type = creator_row.iloc[0]["creator_type"]
                    followers = creator_row.iloc[0]["followers"]
                else:
                    creator_type = "Creator"
                    followers = 0

                score = float(row["base_feed_score"])

                card_html = f"""
                <div style="
                    background:rgba(255,255,255,0.035);
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:16px;
                    padding:18px;
                    margin-bottom:12px;
                ">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <div>

                            <div style="
                                font-size:1.05rem;
                                font-weight:700;
                            ">
                                #{int(row["feed_rank"])} &nbsp;
                                {row["content_id"]}
                            </div>

                            <div style="
                                color:#a1a1aa;
                                margin-top:6px;
                            ">
                                {row["genre"]}
                                · {row["content_type"]}
                                · {float(row["duration"]):.1f}s
                            </div>

                        </div>

                        <div style="
                            text-align:right;
                        ">

                            <div style="
                                color:#c084fc;
                                font-size:1.15rem;
                                font-weight:700;
                            ">
                                {score:.3f}
                            </div>

                            <div style="
                                color:#71717a;
                                font-size:0.72rem;
                            ">
                                feed score
                            </div>

                        </div>

                    </div>

                    <div style="
                        margin-top:12px;
                        color:#a1a1aa;
                        font-size:0.82rem;
                    ">
                        Creator: {row["creator_id"]}
                        · {creator_type}
                        · {int(followers):,} followers
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#d4d4d8;
                        font-size:0.82rem;
                    ">
                        <strong>Why this was recommended:</strong>
                        {row["explanation"]}
                    </div>

                </div>
                """

                st.html(card_html)

        # ----------------------------------------------------
        # ARCHITECTURE
        # ----------------------------------------------------

        st.markdown("### Recommendation pipeline")

        st.markdown(
            """
            **User history**
            → **Candidate generation**
            → **Seen-item filtering**
            → **Feature construction**
            → **Engagement scoring**
            → **Freshness**
            → **Diversity**
            → **Final ranking**
            """
        )

        st.caption(
            "The underlying recommendation architecture and offline "
            "evaluation were developed and validated in Notebook 07."
        )


# ============================================================
# EXPERIMENTS
# ============================================================

elif experiment_page == "Experiments":

    st.markdown("### Recommendation experiments")

    st.caption(
        "Offline evaluation of recommendation strategies "
        "on temporally held-out interactions."
    )

    results = pd.DataFrame(
        [
            [
                "Global Popularity",
                0.0002,
                0.0007,
                0.0002,
                0.0005
            ],
            [
                "Recent Popularity",
                0.0014,
                0.0047,
                0.0018,
                0.0032
            ],
            [
                "Content-Based",
                0.0005,
                0.0016,
                0.0005,
                0.0010
            ],
            [
                "Personalized ML",
                0.0014,
                0.0055,
                0.0019,
                0.0035
            ],
        ],
        columns=[
            "Strategy",
            "Precision@10",
            "Recall@10",
            "MAP@10",
            "NDCG@10"
        ]
    )

    st.dataframe(
        results.style.format(
            {
                "Precision@10": "{:.4f}",
                "Recall@10": "{:.4f}",
                "MAP@10": "{:.4f}",
                "NDCG@10": "{:.4f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    fig = px.bar(
        results,
        x="Strategy",
        y="NDCG@10",
        template="plotly_dark",
    )

    fig.update_layout(
        height=400,
        yaxis_tickformat=".4f",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "These are offline evaluation results from the "
        "temporally held-out evaluation performed in Notebook 07. "
        "They should not be interpreted as causal online lift."
    )


# ============================================================
# MODEL
# ============================================================

elif experiment_page == "Model":

    st.markdown("### Engagement model")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Model",
            "Random Forest"
        )

    with col2:
        st.metric(
            "ROC-AUC",
            "0.5840"
        )

    with col3:
        st.metric(
            "PR-AUC",
            "0.4419"
        )

    with col4:
        st.metric(
            "Features",
            len(feature_columns)
        )

    st.markdown("")

    st.markdown("### Model configuration")

    st.write(
        {
            "Model": "Random Forest Classifier",
            "Features": len(feature_columns),
            "Split": "70 / 15 / 15 chronological",
            "Primary selection metric": "PR-AUC",
            "Secondary metric": "ROC-AUC",
            "Ranking use": "Recommendation scoring",
            "Model artifact": "random_forest_engagement.joblib",
        }
    )

    st.markdown("### Feature contract")

    st.dataframe(
        pd.DataFrame(
            {
                "feature": feature_columns
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
