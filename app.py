"""
app.py

Flask web application for the Music Royalty Split Calculator.

This file handles:
  - Serving the web page (GET /)
  - Receiving form data and calculating splits (POST /calculate)

The actual royalty math lives in royalty_logic.py — this file is just the
"plumbing" that connects a web form to that logic and renders the result.
"""

from flask import Flask, render_template, request
from royalty_logic import Contributor, calculate_splits

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Show the empty calculator form."""
    return render_template("index.html", results=None, error=None)


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Read the submitted form data, run the royalty split calculation,
    and re-render the page with results (or an error message).
    """
    try:
        total_amount = float(request.form.get("total_amount", 0))
        writer_share_percent = float(request.form.get("writer_share_percent", 50))
        publisher_share_percent = float(request.form.get("publisher_share_percent", 50))

        # Writers: names and percentages come in as parallel lists from the form
        writer_names = request.form.getlist("writer_name")
        writer_percentages = request.form.getlist("writer_percentage")
        writers = [
            Contributor(name=name.strip(), percentage=float(pct))
            for name, pct in zip(writer_names, writer_percentages)
            if name.strip() != ""
        ]

        publisher_names = request.form.getlist("publisher_name")
        publisher_percentages = request.form.getlist("publisher_percentage")
        publishers = [
            Contributor(name=name.strip(), percentage=float(pct))
            for name, pct in zip(publisher_names, publisher_percentages)
            if name.strip() != ""
        ]

        if not writers:
            raise ValueError("Please add at least one writer.")
        if not publishers:
            raise ValueError("Please add at least one publisher.")

        results = calculate_splits(
            total_royalty_amount=total_amount,
            writers=writers,
            publishers=publishers,
            writer_share_percent=writer_share_percent,
            publisher_share_percent=publisher_share_percent,
        )

        return render_template(
            "index.html",
            results=results,
            error=None,
            total_amount=total_amount,
            writer_share_percent=writer_share_percent,
            publisher_share_percent=publisher_share_percent,
            writers=writers,
            publishers=publishers,
        )

    except (ValueError, TypeError) as e:
        return render_template("index.html", results=None, error=str(e))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
