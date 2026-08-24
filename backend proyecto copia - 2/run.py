import os
from src import create_app


app = create_app("development")


if __name__ == "__main__":

    port = int(
        os.getenv("PORT", 5000)
    )

    debug_mode = os.getenv(
        "DEBUG",
        "True"
    ).lower() in [
        "true","1", "t"
    ]

    print()
    print("=" * 50)
    print(" BilleterAPP API")
    print("=" * 50)
    print(f" Servidor: http://localhost:{port}")
    print(f" API:      http://localhost:{port}/api/v1")
    print(f" Debug:    {debug_mode}")
    print("=" * 50)
    print()

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )