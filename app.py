import os
from src.dashboard import dashboard

# Launch the dashboard on Render, won't work locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    dashboard.launch(server_name="0.0.0.0", server_port=port, share=False)
