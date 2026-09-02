import streamlit as st


def apply_document_intelligence_styles() -> None:
    """
    Apply the global Enterprise Document Intelligence System UI styling.

    v1.0:
    Modern document intelligence workspace with
    a cleaner conversational interface.
    """

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
           ===================================================== */

        .stApp {
            background: #0b0f14;
            color: #e8edf3;
        }

        [data-testid="stAppViewContainer"] {
            background: #0b0f14;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1050px;
            padding-top: 1.25rem;
            padding-bottom: 8rem;
        }


        /* =====================================================
           TYPOGRAPHY
           ===================================================== */

        html,
        body,
        [class*="css"] {
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        h1 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.04em;
        }

        h2 {
            letter-spacing: -0.03em;
        }

        h3 {
            letter-spacing: -0.02em;
        }

        p {
            line-height: 1.65;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        [data-testid="stSidebar"] {
            background: #0f141b;
            border-right: 1px solid #222a34;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        [data-testid="stSidebar"] .block-container {
            padding-bottom: 1.5rem;
        }


        /* =====================================================
           SIDEBAR BUTTONS
           ===================================================== */

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 2.45rem;

            border-radius: 9px;
            border: 1px solid #29313c;

            background: #151b23;
            color: #e7edf5;

            font-size: 0.9rem;
            font-weight: 500;

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                transform 0.15s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #1b222c;
            border-color: #46515f;
            transform: translateY(-1px);
        }

        [data-testid="stSidebar"] .stButton > button:focus {
            box-shadow: none;
        }


        /* =====================================================
           MAIN BUTTONS
           ===================================================== */

        .stButton > button {
            border-radius: 9px;
            transition: all 0.15s ease;
        }


        /* =====================================================
           CHAT AREA
           ===================================================== */

        [data-testid="stChatMessage"] {
            padding-top: 1.15rem;
            padding-bottom: 1.15rem;
            border: none;
            background: transparent;
        }

        [data-testid="stChatMessageContent"] {
            max-width: 820px;
            font-size: 0.98rem;
            line-height: 1.72;
        }

        [data-testid="stChatMessageContent"] p {
            margin-bottom: 0.75rem;
        }

        [data-testid="stChatMessageContent"] p:last-child {
            margin-bottom: 0;
        }


        /* =====================================================
           CHAT INPUT
           ===================================================== */

        [data-testid="stChatInput"] {
            border-top: none;
            padding-top: 0.75rem;
            background: transparent;
        }

        [data-testid="stChatInput"] > div {
            border-radius: 17px;
            border: 1px solid #303946;
            background: #151b23;

            box-shadow:
                0 10px 35px rgba(0, 0, 0, 0.28);

            transition:
                border-color 0.15s ease,
                box-shadow 0.15s ease;
        }

        [data-testid="stChatInput"] > div:focus-within {
            border-color: #596579;

            box-shadow:
                0 10px 35px rgba(0, 0, 0, 0.28),
                0 0 0 1px #596579;
        }

        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            border: none !important;

            color: #edf2f7 !important;

            font-size: 0.98rem;
            line-height: 1.5;

            padding: 0.9rem 1rem;
        }

        [data-testid="stChatInput"] textarea:focus {
            border: none !important;
            box-shadow: none !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #737e8d;
        }


        /* =====================================================
           DOCUMENT HEADER
           ===================================================== */

        .nm-document-header {
            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0.8rem 1rem;
            margin-bottom: 1.5rem;

            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 12px;
        }

        .nm-document-title {
            color: #edf2f7;
            font-size: 0.92rem;
            font-weight: 600;
        }

        .nm-document-meta {
            color: #7f8a99;
            font-size: 0.78rem;
        }

        .nm-status {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;

            color: #aab6c5;
            font-size: 0.78rem;
        }

        .nm-status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #62c48a;
        }


        /* =====================================================
           DOCUMENT ACTIONS
           ===================================================== */

        .nm-action-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;

            margin-top: 0.25rem;
            margin-bottom: 0.65rem;

            color: #dce3eb;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .nm-action-hint {
            color: #687483;
            font-size: 0.72rem;
            font-weight: 400;
            letter-spacing: 0;
        }

        /*
           The action buttons are placed directly after
           the nm-action-heading element.
        */

        .nm-action-heading + div {
            margin-bottom: 1.4rem;
        }

        .nm-action-heading + div .stButton > button {
            width: 100%;
            min-height: 2.8rem;

            background: #11171f;
            border: 1px solid #29313c;
            border-radius: 11px;

            color: #dce3eb;

            font-size: 0.84rem;
            font-weight: 600;

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        .nm-action-heading + div .stButton > button:hover {
            background: #181f28;
            border-color: #46515f;

            transform: translateY(-1px);

            box-shadow:
                0 6px 18px rgba(0, 0, 0, 0.18);
        }

        .nm-action-heading + div .stButton > button:active {
            transform: translateY(0);
        }

        .nm-action-heading + div .stButton > button:focus {
            box-shadow: none;
        }


        /* =====================================================
           EMPTY STATE
           ===================================================== */

        .nm-empty {
            text-align: center;
            padding: 4rem 1rem 3rem;
        }

        .nm-empty-icon {
            width: 64px;
            height: 64px;

            margin: 0 auto 1.25rem;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 18px;

            background: #151c25;
            border: 1px solid #2a333f;

            font-size: 1.8rem;
        }

        .nm-empty-title {
            color: #edf2f7;
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.035em;
            margin-bottom: 0.45rem;
        }

        .nm-empty-subtitle {
            color: #7f8a99;
            font-size: 0.92rem;
            max-width: 520px;
            margin: 0 auto;
            line-height: 1.6;
        }


        /* =====================================================
           SUGGESTION CARDS
           ===================================================== */

        .nm-suggestion {
            padding: 0.9rem 1rem;

            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 11px;

            color: #aeb8c5;
            font-size: 0.84rem;

            text-align: left;
        }


        /* =====================================================
           SOURCE CARDS
           ===================================================== */

        .nm-sources {
            margin-top: 1rem;
            padding-top: 0.85rem;

            border-top: 1px solid #252d38;
        }

        .nm-sources-title {
            color: #aeb8c5;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.65rem;
        }

        .nm-source-card {
            margin-bottom: 0.6rem;
            padding: 0.75rem 0.85rem;

            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 10px;
        }

        .nm-source-header {
            display: flex;
            justify-content: space-between;
            align-items: center;

            margin-bottom: 0.35rem;
        }

        .nm-source-name {
            color: #dce3eb;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .nm-source-score {
            color: #7f8a99;
            font-size: 0.72rem;
        }

        .nm-source-text {
            color: #8995a4;
            font-size: 0.78rem;
            line-height: 1.55;
        }


        /* =====================================================
           SIDEBAR DOCUMENT CARD
           ===================================================== */

        .nm-sidebar-document {
            padding: 0.85rem;

            background: #151b23;
            border: 1px solid #29313c;
            border-radius: 11px;

            margin-bottom: 0.75rem;
        }

        .nm-sidebar-document-name {
            color: #e6ecf3;
            font-size: 0.84rem;
            font-weight: 600;

            word-break: break-word;
        }

        .nm-sidebar-document-meta {
            color: #7f8a99;
            font-size: 0.72rem;
            margin-top: 0.3rem;
        }


        /* =====================================================
           FILE UPLOADER
           ===================================================== */

        [data-testid="stFileUploader"] {
            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 13px;
            padding: 0.6rem;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: #151b23;
            border: 1px dashed #3a4553;
            border-radius: 10px;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #596579;
        }


        /* =====================================================
           EXPANDERS
           ===================================================== */

        [data-testid="stExpander"] {
            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 11px;
            overflow: hidden;
        }


        /* =====================================================
           METRICS
           ===================================================== */

        [data-testid="stMetric"] {
            background: #11171f;
            border: 1px solid #252d38;
            border-radius: 11px;
            padding: 0.9rem;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid #303946;
        }


        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {
            border: none;
            border-top: 1px solid #252d38;
            margin: 1rem 0;
        }


        /* =====================================================
           CAPTIONS
           ===================================================== */

        .stCaption {
            color: #7f8a99 !important;
        }


        /* =====================================================
           SCROLLBAR
           ===================================================== */

        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }

        ::-webkit-scrollbar-track {
            background: #0b0f14;
        }

        ::-webkit-scrollbar-thumb {
            background: #303946;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #465160;
        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .nm-empty {
                padding-top: 2.5rem;
            }

            .nm-document-header {
                align-items: flex-start;
                gap: 0.5rem;
                flex-direction: column;
            }

            .nm-action-heading {
                align-items: flex-start;
                gap: 0.25rem;
                flex-direction: column;
            }

            [data-testid="stChatMessage"] {
                padding: 0.9rem 0;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )
