import os
from src import create_app

app = create_app(
    os.getenv(
        "FLASK_CONFIG",
        "development"
    )
)

# EJECUTAR SERVIDOR

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    debug_mode = (
        os.getenv(
            "DEBUG","True"
        )
        .strip()
        .lower()
        in {
            "true", "1","yes", "y", "on", "t",
        }
    )

    print()
    print("=" * 60)
    print(" BilleterAPP API")
    print("=" * 60)
    print(f" Servidor : http://localhost:{port}")
    print(f" API      : http://localhost:{port}/api/v1")
    print(f" Debug    : {debug_mode}")
    print("=" * 60)
    print()

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode,
    )