{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "# Step 1: Install required packages\n",
        "!pip install datasets paho-mqtt pandas numpy scikit-learn plotly dash\n",
        "!sudo apt-get install -y mosquitto"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "collapsed": true,
        "id": "SkT6hE9h-p0q",
        "outputId": "11c16e1e-473e-416b-a17f-9c67fd178d77"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: datasets in /usr/local/lib/python3.11/dist-packages (3.2.0)\n",
            "Requirement already satisfied: paho-mqtt in /usr/local/lib/python3.11/dist-packages (2.1.0)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (2.2.2)\n",
            "Requirement already satisfied: numpy in /usr/local/lib/python3.11/dist-packages (1.26.4)\n",
            "Requirement already satisfied: scikit-learn in /usr/local/lib/python3.11/dist-packages (1.6.1)\n",
            "Requirement already satisfied: plotly in /usr/local/lib/python3.11/dist-packages (5.24.1)\n",
            "Requirement already satisfied: dash in /usr/local/lib/python3.11/dist-packages (2.18.2)\n",
            "Requirement already satisfied: filelock in /usr/local/lib/python3.11/dist-packages (from datasets) (3.17.0)\n",
            "Requirement already satisfied: pyarrow>=15.0.0 in /usr/local/lib/python3.11/dist-packages (from datasets) (17.0.0)\n",
            "Requirement already satisfied: dill<0.3.9,>=0.3.0 in /usr/local/lib/python3.11/dist-packages (from datasets) (0.3.8)\n",
            "Requirement already satisfied: requests>=2.32.2 in /usr/local/lib/python3.11/dist-packages (from datasets) (2.32.3)\n",
            "Requirement already satisfied: tqdm>=4.66.3 in /usr/local/lib/python3.11/dist-packages (from datasets) (4.67.1)\n",
            "Requirement already satisfied: xxhash in /usr/local/lib/python3.11/dist-packages (from datasets) (3.5.0)\n",
            "Requirement already satisfied: multiprocess<0.70.17 in /usr/local/lib/python3.11/dist-packages (from datasets) (0.70.16)\n",
            "Requirement already satisfied: fsspec<=2024.9.0,>=2023.1.0 in /usr/local/lib/python3.11/dist-packages (from fsspec[http]<=2024.9.0,>=2023.1.0->datasets) (2024.9.0)\n",
            "Requirement already satisfied: aiohttp in /usr/local/lib/python3.11/dist-packages (from datasets) (3.11.11)\n",
            "Requirement already satisfied: huggingface-hub>=0.23.0 in /usr/local/lib/python3.11/dist-packages (from datasets) (0.27.1)\n",
            "Requirement already satisfied: packaging in /usr/local/lib/python3.11/dist-packages (from datasets) (24.2)\n",
            "Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.11/dist-packages (from datasets) (6.0.2)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas) (2024.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.1)\n",
            "Requirement already satisfied: scipy>=1.6.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (1.13.1)\n",
            "Requirement already satisfied: joblib>=1.2.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (1.4.2)\n",
            "Requirement already satisfied: threadpoolctl>=3.1.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (3.5.0)\n",
            "Requirement already satisfied: tenacity>=6.2.0 in /usr/local/lib/python3.11/dist-packages (from plotly) (9.0.0)\n",
            "Requirement already satisfied: Flask<3.1,>=1.0.4 in /usr/local/lib/python3.11/dist-packages (from dash) (3.0.3)\n",
            "Requirement already satisfied: Werkzeug<3.1 in /usr/local/lib/python3.11/dist-packages (from dash) (3.0.6)\n",
            "Requirement already satisfied: dash-html-components==2.0.0 in /usr/local/lib/python3.11/dist-packages (from dash) (2.0.0)\n",
            "Requirement already satisfied: dash-core-components==2.0.0 in /usr/local/lib/python3.11/dist-packages (from dash) (2.0.0)\n",
            "Requirement already satisfied: dash-table==5.0.0 in /usr/local/lib/python3.11/dist-packages (from dash) (5.0.0)\n",
            "Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.11/dist-packages (from dash) (8.6.1)\n",
            "Requirement already satisfied: typing-extensions>=4.1.1 in /usr/local/lib/python3.11/dist-packages (from dash) (4.12.2)\n",
            "Requirement already satisfied: retrying in /usr/local/lib/python3.11/dist-packages (from dash) (1.3.4)\n",
            "Requirement already satisfied: nest-asyncio in /usr/local/lib/python3.11/dist-packages (from dash) (1.6.0)\n",
            "Requirement already satisfied: setuptools in /usr/local/lib/python3.11/dist-packages (from dash) (75.1.0)\n",
            "Requirement already satisfied: Jinja2>=3.1.2 in /usr/local/lib/python3.11/dist-packages (from Flask<3.1,>=1.0.4->dash) (3.1.5)\n",
            "Requirement already satisfied: itsdangerous>=2.1.2 in /usr/local/lib/python3.11/dist-packages (from Flask<3.1,>=1.0.4->dash) (2.2.0)\n",
            "Requirement already satisfied: click>=8.1.3 in /usr/local/lib/python3.11/dist-packages (from Flask<3.1,>=1.0.4->dash) (8.1.8)\n",
            "Requirement already satisfied: blinker>=1.6.2 in /usr/local/lib/python3.11/dist-packages (from Flask<3.1,>=1.0.4->dash) (1.9.0)\n",
            "Requirement already satisfied: aiohappyeyeballs>=2.3.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (2.4.4)\n",
            "Requirement already satisfied: aiosignal>=1.1.2 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (1.3.2)\n",
            "Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (25.1.0)\n",
            "Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (1.5.0)\n",
            "Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (6.1.0)\n",
            "Requirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (0.2.1)\n",
            "Requirement already satisfied: yarl<2.0,>=1.17.0 in /usr/local/lib/python3.11/dist-packages (from aiohttp->datasets) (1.18.3)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets) (3.4.1)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets) (2.3.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests>=2.32.2->datasets) (2024.12.14)\n",
            "Requirement already satisfied: MarkupSafe>=2.1.1 in /usr/local/lib/python3.11/dist-packages (from Werkzeug<3.1->dash) (3.0.2)\n",
            "Requirement already satisfied: zipp>=3.20 in /usr/local/lib/python3.11/dist-packages (from importlib-metadata->dash) (3.21.0)\n",
            "Reading package lists... Done\n",
            "Building dependency tree... Done\n",
            "Reading state information... Done\n",
            "mosquitto is already the newest version (2.0.11-1ubuntu1.1).\n",
            "0 upgraded, 0 newly installed, 0 to remove and 18 not upgraded.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!sudo apt-get install -y mosquitto\n",
        "!mosquitto -d"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "collapsed": true,
        "id": "e--N4RSu-0H4",
        "outputId": "b4004282-49a1-48a0-ce6b-4c3a298c4820"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Reading package lists... Done\n",
            "Building dependency tree... Done\n",
            "Reading state information... Done\n",
            "mosquitto is already the newest version (2.0.11-1ubuntu1.1).\n",
            "0 upgraded, 0 newly installed, 0 to remove and 18 not upgraded.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 845
        },
        "id": "v2AePJbT-d1A",
        "outputId": "878700ce-cce4-48bd-e864-6917e39b88b4"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-14-4b84f0868390>:28: DeprecationWarning:\n",
            "\n",
            "Callback API version 1 is deprecated, update to latest version\n",
            "\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Error loading dataset: Dataset 'mikael110/medical-device-timeseries' doesn't exist on the Hub or cannot be accessed., using synthetic data\n",
            "Connecting to MQTT broker at test.mosquitto.org:1883\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-14-4b84f0868390>:41: FutureWarning:\n",
            "\n",
            "'S' is deprecated and will be removed in a future version, please use 's' instead.\n",
            "\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ],
            "application/javascript": [
              "(async (port, path, width, height, cache, element) => {\n",
              "    if (!google.colab.kernel.accessAllowed && !cache) {\n",
              "      return;\n",
              "    }\n",
              "    element.appendChild(document.createTextNode(''));\n",
              "    const url = await google.colab.kernel.proxyPort(port, {cache});\n",
              "    const iframe = document.createElement('iframe');\n",
              "    iframe.src = new URL(path, url).toString();\n",
              "    iframe.height = height;\n",
              "    iframe.width = width;\n",
              "    iframe.style.border = 0;\n",
              "    iframe.allow = [\n",
              "        'accelerometer',\n",
              "        'autoplay',\n",
              "        'camera',\n",
              "        'clipboard-read',\n",
              "        'clipboard-write',\n",
              "        'gyroscope',\n",
              "        'magnetometer',\n",
              "        'microphone',\n",
              "        'serial',\n",
              "        'usb',\n",
              "        'xr-spatial-tracking',\n",
              "    ].join('; ');\n",
              "    element.appendChild(iframe);\n",
              "  })(8050, \"/\", \"100%\", 650, false, window.element)"
            ]
          },
          "metadata": {}
        }
      ],
      "source": [
        "# Step 2: Import libraries\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "from datasets import load_dataset\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "import paho.mqtt.client as mqtt\n",
        "import time\n",
        "import dash\n",
        "from dash import dcc, html\n",
        "from dash.dependencies import Input, Output\n",
        "import plotly.graph_objs as go\n",
        "import threading\n",
        "import socket\n",
        "import subprocess\n",
        "\n",
        "# Step 3: Configure MQTT (Using an External Broker)\n",
        "def get_colab_ip():\n",
        "    \"\"\"Get Colab instance's internal IP\"\"\"\n",
        "    return socket.gethostbyname(socket.gethostname())\n",
        "\n",
        "# Start MQTT Broker (Not supported in Colab, using external broker instead)\n",
        "EXTERNAL_BROKER = \"test.mosquitto.org\"  # Example external MQTT broker\n",
        "MQTT_PORT = 1883\n",
        "TOPIC_PUBLISH = \"medical/device/data\"\n",
        "TOPIC_SUBSCRIBE = \"medical/device/commands\"\n",
        "\n",
        "# Step 4: MQTT Client Setup\n",
        "client = mqtt.Client()\n",
        "try:\n",
        "    client.connect(EXTERNAL_BROKER, MQTT_PORT, 60)\n",
        "except Exception as e:\n",
        "    print(f\"Failed to connect to MQTT broker: {e}\")\n",
        "\n",
        "# Step 5: Load and preprocess data\n",
        "def load_medical_data():\n",
        "    try:\n",
        "        dataset = load_dataset('mikael110/medical-device-timeseries', split='train')\n",
        "        df = dataset.to_pandas()\n",
        "    except Exception as e:\n",
        "        print(f\"Error loading dataset: {e}, using synthetic data\")\n",
        "        dates = pd.date_range(start='2023-01-01', periods=1000, freq='S')\n",
        "        df = pd.DataFrame({\n",
        "            'timestamp': dates,\n",
        "            'heart_rate': np.random.normal(75, 10, 1000),\n",
        "            'blood_pressure': np.random.normal(120, 15, 1000),\n",
        "            'oxygen_saturation': np.random.normal(98, 2, 1000)\n",
        "        })\n",
        "\n",
        "    df['timestamp'] = pd.to_datetime(df['timestamp'])\n",
        "    df.set_index('timestamp', inplace=True)\n",
        "    return df\n",
        "\n",
        "# Step 6: Medical Device Integration\n",
        "class MedicalDeviceIntegration:\n",
        "    def __init__(self):\n",
        "        self.df = load_medical_data()\n",
        "        self.current_index = 0\n",
        "        self.latencies = []\n",
        "        self.lock = threading.Lock()\n",
        "\n",
        "    def publish_data(self):\n",
        "        while self.current_index < len(self.df):\n",
        "            with self.lock:\n",
        "                payload = self.df.iloc[self.current_index].to_json()\n",
        "                start_time = time.time()\n",
        "                client.publish(TOPIC_PUBLISH, payload, qos=1)\n",
        "                latency = (time.time() - start_time) * 1000\n",
        "                self.latencies.append(latency)\n",
        "                self.current_index += 1\n",
        "            time.sleep(0.05)  # Faster sampling\n",
        "\n",
        "    def on_message(self, client, userdata, msg):\n",
        "        print(f\"Received command: {msg.payload.decode()}\")\n",
        "\n",
        "# Initialize the medical device instance\n",
        "medical_device = MedicalDeviceIntegration()\n",
        "\n",
        "# Step 7: Dash Dashboard\n",
        "app = dash.Dash(__name__)\n",
        "app.layout = html.Div([\n",
        "    html.H1(\"Medical Device Monitoring\"),\n",
        "    dcc.Store(id='memory-store'),\n",
        "    dcc.Graph(id='live-graph'),\n",
        "    dcc.Interval(id='graph-update', interval=800, n_intervals=0),\n",
        "    html.Div(id='latency-metrics')\n",
        "])\n",
        "\n",
        "@app.callback(\n",
        "    [Output('live-graph', 'figure'),\n",
        "     Output('latency-metrics', 'children')],\n",
        "    [Input('graph-update', 'n_intervals')]\n",
        ")\n",
        "def update_graph(n):\n",
        "    with medical_device.lock:\n",
        "        data = medical_device.df.iloc[:medical_device.current_index]\n",
        "\n",
        "    fig = {\n",
        "        'data': [\n",
        "            go.Scatter(x=data.index, y=data[col], name=col)\n",
        "            for col in data.columns\n",
        "        ],\n",
        "        'layout': go.Layout(\n",
        "            title=\"Real-time Patient Vital Signs\",\n",
        "            uirevision='constant'\n",
        "        )\n",
        "    }\n",
        "\n",
        "    avg_latency = np.mean(medical_device.latencies[-100:]) if medical_device.latencies else 0\n",
        "    metrics = html.Div([\n",
        "        html.H3(f\"Average Latency (last 100 points): {avg_latency:.2f} ms\"),\n",
        "        html.P(f\"Total Data Points: {medical_device.current_index}\"),\n",
        "        html.P(f\"Connected Devices: 1\")\n",
        "    ])\n",
        "\n",
        "    return fig, metrics\n",
        "\n",
        "# Step 8: Run with proper threading\n",
        "if __name__ == \"__main__\":\n",
        "    print(f\"Connecting to MQTT broker at {EXTERNAL_BROKER}:{MQTT_PORT}\")\n",
        "    client.loop_start()\n",
        "\n",
        "    client.on_message = medical_device.on_message\n",
        "    client.subscribe(TOPIC_SUBSCRIBE)\n",
        "\n",
        "    publish_thread = threading.Thread(target=medical_device.publish_data, daemon=True)\n",
        "    publish_thread.start()\n",
        "\n",
        "    app.run_server(host='0.0.0.0', port=8050, debug=False)\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "JUe-odOfQTeJ"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}