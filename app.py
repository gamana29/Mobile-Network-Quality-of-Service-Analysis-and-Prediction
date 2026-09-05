import streamlit as st
import pandas as pd
import joblib

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="5G Mobile Network QoS Prediction",
    page_icon="📡",
    layout="wide"
)

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------

@st.cache_resource
def load_models():

    throughput_model = joblib.load(
        "best_throughput_prediction_model.pkl"
    )

    anomaly_model = joblib.load(
        "best_anomaly_detection_model.pkl"
    )

    return throughput_model, anomaly_model


throughput_model, anomaly_model = load_models()


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📡 5G Mobile Network QoS Analysis and Prediction")

st.write(
    "Machine Learning Based System for Predicting "
    "Downlink Throughput and Detecting Network Anomalies"
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("Enter 5G Network Parameters")


# -------------------------------------------------
# USER INPUTS
# -------------------------------------------------

rsrp = st.sidebar.slider(
    "RSRP (dBm)",
    min_value=-140.0,
    max_value=-40.0,
    value=-90.0
)


rsrq = st.sidebar.slider(
    "RSRQ (dB)",
    min_value=-30.0,
    max_value=0.0,
    value=-10.0
)


sinr = st.sidebar.slider(
    "SINR (dB)",
    min_value=-10.0,
    max_value=40.0,
    value=10.0
)


pdsch_mcs = st.sidebar.slider(
    "PDSCH MCS",
    min_value=0.0,
    max_value=30.0,
    value=15.0
)


pusch_mcs = st.sidebar.slider(
    "PUSCH MCS",
    min_value=0.0,
    max_value=30.0,
    value=15.0
)


pdsch_prbs = st.sidebar.slider(
    "PDSCH PRBs",
    min_value=0.0,
    max_value=300.0,
    value=100.0
)


pusch_prbs = st.sidebar.slider(
    "PUSCH PRBs",
    min_value=0.0,
    max_value=300.0,
    value=100.0
)


# -------------------------------------------------
# CREATE INPUT DATA
# -------------------------------------------------

input_regression = pd.DataFrame([{

    "RSRP": rsrp,

    "RSRQ": rsrq,

    "SINR": sinr,

    "PDSCH_MCS": pdsch_mcs,

    "PUSCH_MCS": pusch_mcs,

    "PDSCH PRBs": pdsch_prbs,

    "PUSCH PRBs": pusch_prbs

}])


# -------------------------------------------------
# PREDICTION BUTTON
# -------------------------------------------------

if st.button("Predict Network Performance"):

    # Throughput Prediction

    predicted_throughput = throughput_model.predict(
        input_regression
    )[0]


    # Classification needs throughput also

    input_classification = input_regression.copy()

    input_classification["throughput_DL"] = predicted_throughput


    anomaly_prediction = anomaly_model.predict(
        input_classification
    )[0]


    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    st.divider()

    st.subheader("Prediction Results")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Predicted Downlink Throughput",
            f"{predicted_throughput:.2f}"
        )


    with col2:

        if anomaly_prediction == 1:

            st.error(
                "⚠️ Network Anomaly Detected"
            )

        else:

            st.success(
                "✅ Normal Network Condition"
            )


# -------------------------------------------------
# PARAMETER INFORMATION
# -------------------------------------------------

st.divider()

st.subheader("5G Network Parameter Information")


info_data = {

    "Parameter": [

        "RSRP",
        "RSRQ",
        "SINR",
        "PDSCH MCS",
        "PUSCH MCS",
        "PDSCH PRBs",
        "PUSCH PRBs"

    ],

    "Description": [

        "Reference Signal Received Power",

        "Reference Signal Received Quality",

        "Signal to Interference and Noise Ratio",

        "Downlink Modulation and Coding Scheme",

        "Uplink Modulation and Coding Scheme",

        "Downlink Physical Resource Blocks",

        "Uplink Physical Resource Blocks"

    ]

}


st.table(
    pd.DataFrame(info_data)
)